#!/bin/sh
# Pulls the latest version of All About Berlin and rebuilds it as needed
set -e

URSUS_PATH=/usr/lib/ursus
URSUS_REPO_URL="https://github.com/nicbou/ursus.git"
alias ursus_git="git -C $URSUS_PATH"
alias install_ursus="pip install -e $URSUS_PATH"

SITE_PATH=/var/ursus/site
SITE_REPO_URL=$GIT_REPO_URL
alias site_git="git -C $SITE_PATH"
alias build_site="ursus -c $SITE_PATH/ursus_config.py"

# Clone repos if they don't exist
if [ ! -d "$URSUS_PATH/.git" ]
then
    mkdir -p $URSUS_PATH
    git clone $URSUS_REPO_URL $URSUS_PATH
fi
install_ursus

if [ ! -d "$SITE_PATH/.git" ]
then
    mkdir -p $SITE_PATH
    git clone $SITE_REPO_URL $SITE_PATH
    build_site;
fi

# Initial build on start
site_git pull;
build_site;

# Wait for changes
while true; do
    # Update ursus if needed
    ursus_git fetch > /dev/null
    ursus_commit_count=$(ursus_git rev-list HEAD...origin/master --count)
    if [ "$ursus_commit_count" -gt "0" ]; then
        ursus_git pull
        install_ursus
    fi

    # Rebuild site if needed
    site_git fetch > /dev/null
    site_commit_count=$(site_git rev-list HEAD...origin/master --count)
    if [ "$site_commit_count" -gt "0" ]; then
        site_git pull
        build_site
    fi

    sleep 60
done
