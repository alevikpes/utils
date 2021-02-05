
# Using Docker for Odoo environments

With this project we use **Docker** for automation of the setup
process of Odoo development environments. This must allow any developer
to setup environment for any project in very little time. It can also
significantly speed up the deployment process and can be further used
during the *continuous integration* process, but it is not implemented in
this particular project.

Current process was implemented and tested on Ubuntu 18.04.


### Table of Contents
[**Setup Docker Environment**](#setup-docker-environment)<br>
[**Introduction**](#introduction)<br>
[**Step by Step Guide**](#step-by-step-guide)<br>
[**Implementation Details**](#implementation-details)<br>
[**Docker Storage**](#docker-storage)<br>
[**Todo**](#todo)<br>
[**Sources**](#sources)


### Setup Docker environment

For this automation to work properly, a developer must have
[**Docker**](https://www.docker.com/) and
[**docker-compose**](https://docs.docker.com/compose/) on his local machine.
It is not clear, if **Docker Machine** is also required but it was
installed on the tested environment.

There are multiple sources on internet about installation of this software.
`docker-setup-guide.md` in this repo contains all the instructions for Ubuntu.

[The complete docker guide](https://docs.docker.com/get-started/) from
installation to deployment.


### Setup Private Docker Registry

There is a [great step-by-step guide on setting up a private Docker registry
on a private server](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-private-docker-registry-on-ubuntu-14-04). 

It was tested successfully for all step except 8 and 9 on Ubuntu 18.04.
It must work fine for the other Debian distributions. For the most of the
other Linux distributions it should work with minor differences.

Step 8 may have different approach on different Linux distributions.
Search for the corresponding instructions specific to your Linux flavour
and to the **init** system used.

Step 9 requires a second server, which did not exist at the moment of testing.

**Note**: It is not necessary to copy any file from the `registry` dir,
since they all will be created during the setup process.


### Introduction

The main idea of this implementation is:
- to generate a **custom Odoo** image of a specific version and use it
    for multiple projects
- to generate a **project Odoo** image, so every developer can easily create
    an identical environment for the same project

##### Custom Odoo image
Every **custom Odoo** image is based on one of the official Odoo images,
which can be found in the
[official *Docker* store](https://hub.docker.com/_/odoo/).

Every docker image has a, so-called, **digest**, which is unique.
So, it is also possible to use the digest of the official Odoo image
in our custom **Dockerfile** to create our **custom Odoo** image.

The custom Dockerfile sits in the
[current repository]().

##### Project Odoo image
The **custom Odoo** image will be used for creation of the final
**project Odoo** image using other **Dockerfile** and a
**docker-compose.yml** file, which reside in the
[**project-docker-content repository**](),
and must be copied into the project root directory.
Those files include most of the required tools and modules.

##### Storing and transfering images
When a docker image is created or pulled from a docker repository,
it is stored locally in a **registry**.
All locally stored images can be seen via:
```bash
docker images
```

**One** of the options is to create a
[**private docker registry**](https://docs.docker.com/registry/)
on a private server and store all the required images there.
They can be pulled from the registry by the developers,
who have access to it.

For me details see
[Setup Private Docker Registry](#setup-private-docker-registry).

**Another** option is to archive and transfer images to another registry.
For this it must be archived first:
```bash
docker save -o <path to image tar file> <image name>
```
This new file can be copied as a normal file and then loaded
to another docker registry:
```bash
docker load -i <path to image tar file>
```

##### Database integration
An instance of the PostgreSQL database is created in a separate docker
container when a project starts with the `docker-compose.yml` file.
The current default setup allows to connect to the db automatically.
If any changes required, then the setup in the `docker-compose.yml`,
`entrypoint.sh` and project's `Dockerfile` must also be changed accordingly.
In this case the images must be rebuilt.

**Note**: Any newly created container will not be able to connect to the
existing db container. It is necessary to create both containers together
with the `create-project` script. The new database container will be
successfully using the existing data volume.


### Step by Step Guide

Before starting, clone the
[`docker-odoo` repo]()
to your local or to the server, where the project is located.

##### Step 1
`cd` to `docker-odoo` dir and run:
```bash
./create-odoo-image <odoo version> <desired name for new image>
```
- the Odoo version is a tag as specified in
[the official Odoo docker store](https://store.docker.com/images/odoo)
(ex.: `11`, `11.0`).
- the desired image name has certain limitations in the syntax.
If `:` is used in the name, the text after it will be
interpreted as a tag and usually used to specify version.
The `:` can only appear once in the name.
An example of the correct name is *custom-image-11:v2018.11.30*.
- a slash `/` is used to specify a user of the docker registry. This is
used during the deployment process using docker registry.
This topic is still under investigation.

**Result**: image with the desired name is created and can be observed with:
```bash
docker images
```

**Note**: This step should not be repeated for every project,
it is only done once for every new Odoo version.

##### Step 2
Initiate your project by executing `project-init` script:
```bash
/path/to/project-init \
    <project name> \
    <enterprise branch> \
    <list of directories (optional)>
```

**Note**: This step only needs to be executed once per project.

**Result**: This script creates a project directory of a given name,
changes to it, clones the specified branch of Odoo Enterprise and
creates other directories, if specified.

##### Step 3
Copy the content of the `docker-odoo/copy-to-project` dir into the
project root dir.

**Note**: Odoo source code **MUST NOT** be in the project dir, since it will
be installed in the container from the image.

**Note**: `odoo-data-dir` is **NOT REQUIRED** any more. Odoo data will
be saved into the docker named volume and can be reused by different
containers until the volume exists. This also solves the permission problem.

**Note**: This step only needs to be executed once per project.

**Result**: Project dir with the required content.

##### Step 4
`cd` to the project dir and modify the content of the `Dockerfile`
file accordingly to the project specs.

In `Dockerfile`:
- add or remove linux packages, if necessary
- add or remove python packages, if necessary
- modify the command in the last line, if necessary:
```Dockerfile
CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]
```
This command will be executed inside the container, when container starts.

**Result**: Correct Dockerfile configuration

##### Step 5
`cd` to the project dir and modify the content of `odoo.conf`:
- make sure `/mnt/extra-addons` is added to the `addons_path`, it is related
to the original Odoo image and must alwayse be specified in the config
- make sure the `data-dir` has value `/var/lib/odoo` - this container dir
will be mounted to the external `odoo-data` volume
- add all required addons paths of your project

**Note**: The `odoo.conf` file was copied from the official odoo
repository as recommended by the Odoo developers. It was not tested with
other specs.

##### Step 6
`cd` to the project dir and create the **project Odoo** image with
`create-project-image` script:
```bash
./create-project-image \
    <odoo image name> \
    <project image name>
```
- `<odoo image name>` must be an existing odoo image
- `<project image name>` must be either a new name (creates new image)
    or an existing one (updates existing image)

**Note**: This step only needs to be executed once per project. If project's
`Dockerfile` is modified, the image must be rebuilt with the same command.

**Result**: Image with the desired name is created and can be observed with:
```bash
docker images
```

##### Step 7 (optional)
`cd` to the project dir and make changes to `docker-compose.yml`, if necessary:
- database integration

**Result** correct configuration of the project.

##### Step 8
Create containers and start the project with `run-project` script:
```bash
./run-project \
    <project image name> \
    <project container name> \
    <database container name (optional)>
```
- `<project image name>` must be of an existing project image
- `<project container name>` can be either a new name (creates new container)
    or an existing one (updates existing container)
- `<database container name (optional)>` recommended new db container
    for every new project container

This command executes the `docker-compose.yml` script and creates a database
container and a project container with the names specified.

The list of the running containers can be observed with
```bash
docker ps
```
With the `-a` flag, the list of all containers can be observed.

**Result**: Containers are created and started, as specified in the *services*
section of the `docker-compose.yml` file.

##### Step 9
Go to *http://localhost:8069/web?debug=1#home* in your browser.

**Result**: Running Odoo instance.

##### Troubleshooting
If Odoo instance is not accessible, check if both containers are running:
```bash
docker ps
```
It may happen, that the project container has exited after the creation.
Then use the following command to start it again.
```bash
docker start <container name or id>
```
With the `-a` flag, added to the previouse command, the container will start
in the attached mode. In this case the log of the currently running
process will be visible in your current terminal window.

**Note**: It is not possible to detach from a container without stopping it
and the process execution. It can be easily started again with the `start`
command.


### Implementation Details

##### Creating a custom Odoo image
The *bash* script `create-odoo-image` in the *docker-odoo* repository
pulls the latest official image of the specified Odoo version from the
[public Odoo docker store](https://hub.docker.com/_/odoo/),
extracts the **digest** and builds the **custom Odoo** image.

The script must be executed from the `docker-odoo` dir, since it uses the
`Dockerfile` located there.
The script requires an Odoo version and a name for the new image
as command line arguments.

This script can be modified, if at some point older release is required.

Do not forget to set the appropriate permissions for the script
to become executable.

##### Creating a project Odoo image
The content of the `copy-to-project` dir must be copied to the project root.
The **custom Odoo** image is used for creation of the final
**project Odoo** image using another **Dockerfile** file and must be
executed from the project dir.

##### Running a project
Every time it is necessary to run the project, execute `run-project` script
in the project dir with the appropriate arguments.

##### Working with the project containers
The previously created **project Odoo** image is used to create the
project-specific development environment by running `docker-compose.yml` file.

Current version of the `docker-compose.yml` file has a default configuration,
recommended by the Odoo developers. It creates two containers, which must
be running at the same time, when the project is live.

Containers can be started and stopped, when necessary. It is possible
to connect to the containers and run commands in their shells.
Check `docker exec` command in the
[docker documentaion](https://docs.docker.com/engine/reference/commandline/exec/)

##### Dockerfile
There are two **Dockerfiles** used in this project.

One is in the `docker-odoo` repository, which is used to create
a general **custom Odoo** image. This file already contains most
of the required configuration and hardly requires any change.
It is used in the `create-odoo-image` script.

The **Dockerfile**s for different official Odoo versions can be found in the
[official Odoo repo](https://github.com/docker-library/docs/tree/master/odoo)

Another **Dockerfile** must be in the root of each project repo and
must contain all the project related configuration, excluding those in the
first `Dockerfile`.  This file must be modified
according to the project specs before creating the image of the project.
After the image is built, all the developers can use it to create their
local development environments.

Any changes to the **Dockerfile**s only take effect on the new images.
If the changes must be applied to the already existing image,
the image must be recreated, and also the containers created from that
image must be updated. For this jsut repeat the guide starting from step 5.

See [this answer](https://stackoverflow.com/a/25555322) and the
[docker docs](https://docs.docker.com/engine/reference/commandline/update/)
for more information.

##### entrypoint.sh
This file contains the configuration of the environment and must be included
into the first **Dockerfile** in order to setup the containers environment.

The default is good enough at the moment, but it can be cofigured as well.
Ask Google how.

##### docker-compose.yml
It is used to create and start all specified containers. This file can also
be used to create images *on the fly*, if necessary. If running with the
existing containers, they will be updated.

The image can be built on the fly with the following syntax:
```yaml
build:
    context: /path/to/context
    dockerfile: /path/to/Dockerfile
```

If not using the default environment, setup the correct variables in
*odoo* service:
- **HOST** must be the same as database container name
- **USER** must be the same as **POSTGRES\_USER**
- **PASWORD** must be the same as **POSTGRES\_PASSWORD**
```yaml
environment:
   - HOST=db
   - USER=odoo
   - PASSWORD=odoo
```

See for more info
[here](https://github.com/docker-library/docs/tree/master/odoo)


### Control the project
Running containers can be stopped with command
```bash
docker stop <container name or id>
```
started with
```bash
docker start <container name or id>
```
and restarted with
```bash
docker restart <container name or id>
```
The container will start detached by default. The `-a` flag to the `start`
command will attach your shell to the container after start.

It is possible to execute commands inside the running container using
`docker exec` command and specifying the application,
which executes the command:
```bash
docker exec -it \
    <container name or id> \
    <application> \
    <command to execute by the application>
```
For example, it is possible to run bash terminal in the container:
```bash
docker exec -it db bash
```
or a database client:
```bash
docker exec -it db psql odoo-db odoo
```
The *bash* `echo` command can be executed in this way:
```bash
docker exec -it rr bash -c "echo \"I am a container!\""
```

Files can be copied inside a container with
```bash
docker cp \
    <path at host> \
    <container name or id>:<path at container>
```

Changes made in the container can be committed back to the image, it was
created from, with the `docker commit ...` command.
See docker docs for details.

A new container can be started with
```bash
docker run <image name or id>
```
This command always creates a new container, even if another container,
created from the same image, already exists.

Containers can be removed with `docker rm ...` command. All the existing
containers can be removed with the following command:
```bash
docker rm $(docker ps -a -q)
```
With the `-f` flag, also the running containers will be stopped and removed.

If a container is removed, any volume used by that container is not removed.
These volumes will be automatically connected to the new containers, created
from the same image.
See the docker docs on volumes for the details.

Docker images can be removed with `docker rmi ...` command.

The full documentation about docker CLI can be found
[here](https://docs.docker.com/engine/reference/commandline/cli/).


### Docker Storage

[This article](https://rominirani.com/docker-tutorial-series-part-7-data-volumes-93073a1b5b72)
and the [official Docker docs](https://docs.docker.com/storage/) are the
examples of pretty good explanations about docker storage with examples.

In general, there are three types (for Linux) of data storage concepts
in Docker. All the types must be explicitely mounted to the container
on creation. For our current situation only two of the types are interesting.
The **volume** and the **bind mount** types will be considered further.

##### Volumes
[**Volumes**](https://docs.docker.com/storage/volumes/)
(and **named volumes** ?) are special Docker entities and managed
completely by Docker. It must be explicitely specified, if a user wants
to use volumes in his container. If name is not specified, docker will
create an *anonymous* volume.

A new container with the mounted volume can be created with the
following docker command:
```bash
docker run -it \
    --mount type=volume,source=<volume name>,target=<container directory> \
    --name container1 \
    <image name>
```

Since, our project uses *docker-compose*, this explanation will focus
mostly on how to use volumes with *docker-compose*.

[This](https://www.linux.com/learn/docker-volumes-and-networks-compose),
[this](https://devopsheaven.com/docker/docker-compose/volumes/2018/01/17/volumes-in-docker-compose.html)
and the [official docker-compose docs](https://docs.docker.com/compose/compose-file/#volumes)
give much information about using volumes with docker-compose.

*Volumes* can be used internally - by only the container, which it was
created with, and externally - by multiple containers.

In case of external usage, a volume must be first created with the docker
command:
```bash
docker volume create <volume name>
```

For the internal usage it is not necessary - the volume will be created
together with the container, if it does not exist at that moment. This volume
can be shared between the *services* created in the same `docker-compose.yml`
file (?).

The code snippet of the `docker-compose.yml` file with a volume:
```yaml
version '3'

volumes:
  web_data:
    # when using external volume:
    external: true

services:
  app:
    image: nginx:alpine
    ports:
      - 80:80
    volumes:
      - web_data:/usr/share/nginx/html:ro
```

Volumes can be inspected for details:
```bash
docker volume inspect <volume name or id>
```

The *docker storage* mechanism is not completely clear at the moment.
It has been tested, that all the volumes are not deleted, if container
is deleted. Moreover, they are connected back automatically to the newly
created container of the same image.

The best application of volumes is storing and retreiving data by the
running containers.

##### Bind Mounts
[**Bind mounts**]() are the host directories, which will be mounted to the
specified directories in the container. Both, the host dir and the guest
dir, are in synchronisation, so any change in one of the dirs will be
immediately reflected in the counter dir.

**Warning**: If the changes in the container are made by *root*, then they
will also appear as made by *root* on the host.

The code snippet of the `docker-compose.yml` file with a *bind mount*:
```yaml
version '3'

services:
  app:
    image: nginx:alpine
    ports:
      - 80:80
    volumes:
      - ./nginx/html:/usr/share/nginx/html:ro
```

*Bind mounts* are convenient to use to connect directories with the code
to the container. In this way the changes in the code will be immediately
reflected in the container and the application can be restarted without
recreating the whole project:
```bash
docker restart <odoo container name or id>
```

When using *bind mounts*, the host dir must exist, but the container's
counter part will be created on the container creation, if not existing.
So, there is no need to copy those directories in advance with
the `Dockerfile`.


### TODO
Related topics to explore:
- create script to automate project setup
- update container with the new code (done)
- deployment (wip)
- entrypoint aliases
- sharing images (done)
    - sharing archived images
    - create a **private docker registry**
    - subscribe to the dockerhub
- investigate docker for Windows
- include enterprise into the **custom Odoo** image
- investigate on the **preserved volumes** (done)


### Sources

- [Odoo 11](https://github.com/odoo/odoo/tree/11.0)
- [Odoo 10](https://github.com/odoo/odoo/tree/10.0)
- [Post about creating Odoo environment with Docker](https://unkkuri.com/blog/unkkuri-blog-1/post/install-odoo-version-11-in-docker-container-21)
- [Github repo of the Docker for Odoo](https://github.com/odoo/docker)
- [Instructions on setting up the Docker env](https://github.com/olexandrpi/dev-utils/blob/master/docker-utils/docker-setup-instructions.md)
- [Guide on using Odoo and PostgreSQL with Docker](https://github.com/docker-library/docs/tree/master/odoo)
- [Official Docker installation guid](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository)
- [Docker entrypoint](https://stackoverflow.com/a/21564990)
- [Docker volumes](https://linuxhint.com/dockerfile_volumes/)
- [Docker ARG command](https://www.jeffgeerling.com/blog/2017/use-arg-dockerfile-dynamic-image-specification)
- [Do not ignore .dockerignore](https://codefresh.io/docker-tutorial/not-ignore-dockerignore/)
- [Private Docker Registry tutorial](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-private-docker-registry-on-ubuntu-14-04)
