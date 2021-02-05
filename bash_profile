### bash history options ###

# ignore duplicate commands, ignore commands starting with a space
export HISTCONTROL=ignoreboth:erasedups

# keep the last 5000 entries
export HISTSIZE=5000

# append to the history instead of overwriting (good for multiple connections)
shopt -s histappend

# set default text editor
export EDITOR='/usr/bin/vim'
export VISUAL='/usr/bin/vim'

# autologout on tty1-6 after 10 minutes
if [[ $(tty) =~ /dev\/tty[1-6] ]]; then
    TMOUT=600
fi

#####################
### Shows current git branch and/or python virtualenv on the command line ###
#####################

# set colours
RED="\[\033[0;31m\]"
YELLOW="\[\033[0;33m\]"
GREEN="\[\033[0;32m\]"
OCHRE="\[\033[38;5;95m\]"
BLUE="\[\033[0;34m\]"
WHITE="\[\033[0;37m\]"
RESET="\[\033[0m\]"

State=
Remote=

# Detect whether the current directory is a git repository.
function is_git_repository {
    git branch > /dev/null 2>&1
}

# Set arrow icon based on status against remote.
function check_remote() {
    remote_pattern="Your branch is (ahead|behind)"
    if [[ ${git_status} =~ ${remote_pattern} ]]; then
        if [[ ${BASH_REMATCH[1]} == "ahead" ]]; then
            remote="↑"
        else
            remote="↓"
        fi

    else
        remote=""
    fi

    State=$1
    Remote="${remote}"
    return
}

# Determine the branch/state information for this git repository.
function set_git_branch {
    # Capture the output of the "git status" command.
    git_status="$(git status 2> /dev/null)"

    # For Ubuntu version >=18.04 `tree` is in git status message
    # For Ubuntu version <18.04 `directory` is in git status message
    repo_clean_msg="working (tree|directory) clean" 
    repo_changed_msg="Changes to be committed" 
    if [[ ${git_status} =~ ${repo_clean_msg} ]]; then
        check_remote ${GREEN}
    elif [[ ${git_status} =~ ${repo_changed_msg} ]]; then
        check_remote ${YELLOW}
    else
        check_remote ${RED}
    fi


    diverge_pattern="# Your branch and (.*) have diverged"
    if [[ ${git_status} =~ ${diverge_pattern} ]]; then
        remote="↕"
    fi

    # Get the name of the branch.
    branch_pattern="^(# )?On branch ([^${IFS}]*)"
    if [[ ${git_status} =~ ${branch_pattern} ]]; then
        branch=${BASH_REMATCH[2]}
    fi

    # Set the final branch PS1 string.
    BRANCH="${State}[${branch}]${Remote}${RESET} "
}

# Determine active Python virtualenv details.
function set_virtualenv () {
    if test -z "$VIRTUAL_ENV" ; then
        PYTHON_VIRTUALENV=""
    else
        PYTHON_VIRTUALENV="${YELLOW}[`basename \"$VIRTUAL_ENV\"`]${RESET} "
    fi
}

function set_bash_prompt(){
    # Set the PYTHON_VIRTUALENV variable.
    set_virtualenv

    # Set the BRANCH variable.
    if is_git_repository ; then
        set_git_branch
    else
        BRANCH=''
    fi

    # Set the bash prompt variable.
    PS1="${BLUE}[\$(date +%H:%M)]"  # coloured date
    PS1+="${PYTHON_VIRTUALENV}"     # python virtualenv
    PS1+="${RESET}\u@\h:"           # host and user name
    PS1+="${BLUE}\W${RESET}"        # working directory
    PS1+="${BRANCH}"                # git branch
    PS1+="${BLUE}\$${RESET} "       # prompt symbol
}

# Tell bash to execute this function just before displaying its prompt.
PROMPT_COMMAND=set_bash_prompt

#####################
#####################
#####################

# set directories' colours
alias ls='ls --color'
LS_COLORS=$LS_COLORS:'di=0;35:*.py=0;33'
export LS_COLORS

### set aliases
# decrypt, mount and cd
#mount_point=<mount point>
#function decrypt_mount_and_cd() {
#    sudo cryptsetup open /dev/disk decrypted
#    echo "Disk decrypted"
#    sudo mount /dev/mapper/decrypted "${mount_point}"
#    echo "Dick mounted to ${mount_point}"
#    cd ${mount_point}
#    echo "Directory changed to ${mount_point}"
#}
#alias mnt-encrypt='sudo decrypt_mount_and_cd'
alias ll='ls -l --group-directories-first'
alias lla='ll -a'
alias grep='GREP_COLOR="1;32" grep --color=always'
# for operations with disks
#alias mnt-<disk label>='sudo mount <device (for ex. /dev/sdb3)> <mount point (for ex. /media/user/disk-label/)>'
#alias cd-<disk label>='cd <mount point>'
#alias cd-projects='cd <path/to/projects>'

# docker aliases
alias dockex='docker exec -ti'
# docker-compose
alias dc='docker-compose'
alias dc-up-build='dc up -d --build --remove-orphans'
alias dc-down='dc down --remove-orphans'
alias dc-up-build-force='dc up -d --build --remove-orphans --force-recreate'
alias dc-up-build-e2e-tests='dc -f docker-compose-e2e-tests.yml up --build -d --remove-orphans'
alias dc-down-e2e-tests='dc -f docker-compose-e2e-tests.yml down --remove-orphans'

# git aliases
alias git-tree='git log --all --graph --decorate --oneline'
alias gits='git status'
alias gitcom='git commit -m'

# set venv for a project
alias set-venv-project='. ~/projects/venvs/project-venv/bin/activate && set -a && . ../environments/local.env && set +a'

## add the projects dir to PYTHONPATH
#export PYTHONPATH=${PYTHONPATH}:${HOME}/projects

## add golang to the PATH
#export PATH=$PATH:/usr/local/go/bin
## add other dirs to the GOPATH
#production=$HOME/projects/Production/go
#export GOPATH=$HOME/go:"${production}"
#export GOBIN="${production}"

## add CUDA to the PATH
#export PATH=$PATH:/usr/local/cuda-10.2/bin
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.2/lib64

## set the PATH to android-sdk
#export PATH=$PATH:/usr/lib/android-sdk/platform-tools/adb
