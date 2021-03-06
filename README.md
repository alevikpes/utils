
# Developer's tools

Some tools, which help me at work.


### Make rebasing a default option for pulling from remote repo
In order to not specify `--rebase` every time updating your branch from
the remote `master`, it is possible to set it as a default option for
`git pull` command. To apply it globally for all repos on your local machine,
run this:
```bash
git config --global pull.rebase true
```

### Using different emails for different git repos
Run the following command to set git to ask you before setting the default
user for each git repo:
```bash
git config --global user.useConfigOnly true
```

After this *git* will remind you to set your email and name for each new repo.
You should not use `--global`` flag in this case, so your details will only be
saved for the current repo.

There is also a command to unset the user.email from all the repos, 
but it does not work for me:
```bash
git config --global --unset-all user.email
```

### Using different git accounts on one machine
When it is necessary to use different git accounts, it is possible to setup
different **ssh keys** and configure *ssh* to use appropriate key when pushing.
The configuration details described
[**here**](https://code.tutsplus.com/tutorials/quick-tip-how-to-work-with-github-and-multiple-accounts--net-22574).

Basic idea is to set two different github hosts in *~/.ssh/config* and then use
their corresponding names when setting the remote urls for git repos. For
example, if you set the *Host* as `github-private` in your ssh config, then
the remote url for the corresponding repo must be
`git@github-private:<git account>/<repo name>.git`. It will also use the correct
ssh key, which you also specify in the config.

### Hide your real email from public on Github
In the *Settings* -> *Emails*, there is an option to hide your real email from
public. If you choose for this option, there will appear an autogenerated
email, which you need to use in your public repos.

If there is at least one commit with your real email, then git will not allow
you to push it. In this case you need to change the email in the commit.
[**Here**](https://stackoverflow.com/a/1320317) is a detailed explanation of
this process.


### rsync

[A nice tutorial on **rsync**](https://everythinglinux.org/rsync/)


### Source environemtn variables from a file

The most convenient way (*in my oppinion*) to set environment variables
on a Linux system is to source a file containing those variables in the
format `ENV_VAR=value`. It is done with the following routing:
```bash
set -a
. /path/to/env/file
set +a
```


### Pytest
When using **pytest** in a docker container, it creates compiled files
(`.pyc`) with the permissions of the container user. This user is not
the same one, which is logged in at your
host system, so those compiled files cannot be read by the host user.
This raises a *Permission Denied* error, when running *docker-compose*
commands.

These compiled files can be removed with the following command:
```bash
sudo rm -f $(find . -type f -name "**.pyc")
```


### Remap CapsLock to BackSpace on Ubuntu

Remap for only the current session with
```bash
setxkbmap -option caps:backspace
```
This will be reset back to the default after logout.

There are a few ways to make it constant. I consider here two of them.

One is to set it in the corresponding keyboard config file, such as
`/usr/share/X11/xkb/symbols/us`. The last part is the corresponding keyboard
layout. This is an example for the **us** layout. The first section of the
file is the **basic** config. It is inherited by the other once, so it is
enough to set the remap in this section and it will be picked up by the others.

For remapping add the following line to the end of the first section:
```
xkb_symbols "basic" {
    name[Group1]= "English (US)";
    ...
    ...
    key <CAPS> {    [ BackSpace,    BackSpace   ]   };  # add this line
};
```
After loging out your changes will take effect.
[*Source*](https://www.reddit.com/r/Colemak/comments/4i4mx5/linux_remap_caps_lock_backspace_to_ctrl/d2vmvmf)

Another method is to add the command, used in the first method
`setxkbmap -option caps:backspace` to auto-startup.
[*Source*](https://michaeljaylissner.com/posts/2008/04/29/remap-caps-lock-as-backspace/)

After both these operations your remapped key should work fine except the
auto-repeat functionality on long press. This can be fixed for the current
session by typing:
```bash
xset r 66
```
For all the new sessions the following can be added to `.Xmodmap` file in
your home directory:
```
!
! Make the caps lock button a backspace button
!
remove Lock = Caps_Lock
keycode 66 = BackSpace
```
If the file does not exist, create it.



### Detecting file type based on its signature

Detecting file type based on the extension is not very reliable method. The
better way is to check the file signature and detect the MIME type of the file.

These are the usefull resources:
https://www.iana.org/assignments/media-types/media-types.xhtml
https://en.wikipedia.org/wiki/List_of_file_signatures
https://mimesniff.spec.whatwg.org/#understanding-mime-types

##### Testing
Testing of the MIME type may look like this:
```python
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile


FILE_DATA = (
    ('application/pdf', bytearray(b'\x25\x50\x44\x46\x2d'), True),
    # any file with normal text is considered as `text/plain`
    # the most common headers are:
    ('text/plain', bytearray(b'\xEF\xBB\xBF'), True),
    ('text/plain', bytearray(b'\xfe\xff'), True),
    ('text/plain', bytearray(b'\xff\xfe'), True),
    ('text/xml', bytearray(b'\x3C\x3F\x78\x6D\x6C'), False),
    # older doc, xls, ppt etc.
    ('application/msword', bytearray(b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1'),
     True),
    ('rtf', bytearray(b'7B\x5C\x72\x74\x66\x31'), True),
    # also all modern ms office types are recognised as zip files
    ('application/zip', bytearray(b'\x50\x4B\x03\x04'), True),
    ('application/zip', bytearray(b'\x50\x4B\x05\x06'), True),
    ('application/zip', bytearray(b'\x50\x4B\x07\x08'), True),
    ('application/7z', bytearray(b'\x37\x7A\xBC\xAF\x27\x1C'), True),
    ('application/x-tar', bytearray(b'\x75\x73\x74\x61\x72\x00\x30\x30'),
     True),
    ('application/x-gtar', bytearray(b'\x75\x73\x74\x61\x72\x20\x20\x00'),
     True),
    # exe: application/octet-stream, application/x-msdownload
    ('application/octet-stream', bytearray(b'\x4D\x5A'), False),
    ('application/x-msdownload', bytearray(b'\x4D\x5A'), False),
    ('image/png', bytearray(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'), False),
)


@pytest.mark.parametrize('content_type,file_content,validation',
                          FILE_DATA)
def test_upload_file(self, content_type, file_content, validation):
    test_file = SimpleUploadedFile('test-file', file_content, content_type)
    # do some test
```
