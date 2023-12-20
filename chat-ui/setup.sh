#!/bin/bash

echo "Current Versions"
node -v
npm -v
yarn -v

# Install or update nvm
if [ -d "$HOME/.nvm" ]; then
    cd "$HOME/.nvm" && git pull origin master
else
    git clone https://github.com/nvm-sh/nvm.git "$HOME/.nvm"
fi

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm


# Install specific Node.js version
nvm install 21
nvm alias default 21
nvm use default

# Install specific npm version
npm install -g npm@10

# Install specific Yarn version
npm install -g yarn@1.22

echo "Current Versions after install"
node -v
npm -v
yarn -v