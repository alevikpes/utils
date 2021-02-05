*Based on <https://github.com/Keats/django-drf-template>*


# Setting up the development environment
We use *Docker* for setting up development environment. Here are the step by
step instructions **for Ubuntu only**, since only the Ubuntu path was tested.

We repeat here all the instructions, but also provide the links to the sources,
in case something has changed.

The instructions must be similar for other Linux distributions.

**If you tried other OS's, please update this README**


## Install *Docker*
Choose your *Docker* version from [here](https://store.docker.com/search?offering=community&q=&type=edition)
and follow the installation instructions for your favourite system.
For *Ubuntu* it is [here](https://store.docker.com/editions/community/docker-ce-server-ubuntu?tab=description).

### Install required packages
```
sudo apt -y install \
    apt-transport-https \
    ca-certificates \
    curl
```

### Add the *Docker* repository key
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

### Add the *Docker* repository
```
sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"
```

### Update
```
sudo apt update
```

### Install *Docker*
```
sudo apt -y install docker-ce
```

### Test your installation
```
sudo docker run hello-world
```

If your test passed successfully, go on with the other steps.


## Optional *Docker* post installation steps
In order to avoid using *sudo* for every *Docker* command follow the
[instructions here](https://docs.docker.com/engine/installation/linux/linux-postinstall/).

### Create the `docker` group
```
sudo groupadd docker
```

### Add your user to the group
```
sudo usermod -aG docker $USER
```

Log out and log back in so that your group membership is re-evaluated. Verify:
```
docker run hello-world
```


## Install *Docker Machine*
Follow [these instructions](https://docs.docker.com/machine/install-machine/#installing-machine-directly)
to install the *Machine*. Include the correct version in the command:
```
curl -L \
        https://github.com/docker/machine/releases/download/<version>/docker-machine-`uname -s`-`uname -m` \
        > /tmp/docker-machine \
    && chmod +x /tmp/docker-machine \
    && sudo cp /tmp/docker-machine /usr/local/bin/docker-machine
```

Check the installation by displaying the Machine version:
```
docker-machine version
```

The output must be similar to this:
```
docker-machine version 0.10.0, build 76ed2a6
```


## Install *Docker Compose*
The executable of the correct version must be requested with `curl`. Check
[here](https://docs.docker.com/compose/install/#install-compose) and copy
the command with the correct version. It must look like this:
```
curl -L \
    https://github.com/docker/compose/releases/download/<version>/docker-compose-`uname -s`-`uname -m` \
    > /usr/local/bin/docker-compose
```

If you get a “Permission denied” error, you may need to run this command
as a `root` user. So, first do
```
sudo -i
```
Your command prompt must change to `root@host:~#`. Then repeat the
`curl` command. Logout from the `root` environment by executing `exit` and run
the following command to make the *docker-compose* executable
```
sudo chmod +x /usr/local/bin/docker-compose
```

Check the version
```
docker-compose --version
```


## Add ssh keys to the GitLab repo
```
ssh-keygen -t rsa -C "some-key-identifier"
```
Press `Enter` for all prompts to have default configuration.

Copy the public part of your key
```
cat ~/.ssh/id_rsa.pub
```
and paste it to your profile. Give this key a name, since you may have several
machines connected to the same repo.


## Build the *Docker* image of your repo
Clone the repo in the directory of your choice
```
git clone git@gitlab.company.com:project/repo.git
```
and `cd` to that directory
```
cd /your/dir/repo
```

Now you need to login to the registry with your *GitLab* credentials:
```
docker login registry.company.com
```

Then run
```
docker-compose build
```
When it is finished, your image is ready.


## Start your environment
Start *Docker* instance
```
docker-compose up
```
When it is running, start the *Django* server locally on port 8000
```
docker exec -it contaner_name python manage.py runserver 0.0.0.0:8000
```


## Set up your application
Update your migrations
```
docker exec -it container_name python manage.py migrate
```

Create a user
```
docker exec -it container_name python manage.py createsuperuser
```
Make an email and a password for the user, which you are going to use to login
to the application. Can be fake.



## Tips and tricks

### Remove `*.pyc` files created by root in the docker

```bash
sudo rm $(find . -type f -name "*.pyc")
```
