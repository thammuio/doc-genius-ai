#!/bin/bash
set -e

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


# Biuild the project
# Select nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm


# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js first."
    exit 1
else
    version=$(node -v)
    major_version=${version:1:2}
    if [ "$major_version" != "21" ]; then
        echo "Node.js version 21 is not installed. Please install Node.js version 21."
        exit 1
    fi
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm is not installed. Please install npm first."
    exit 1
else
    version=$(npm -v)
    major_version=${version%%.*}
    if [ "$major_version" != "10" ]; then
        echo "npm version 10 is not installed. Please install npm version 10."
        exit 1
    fi
fi

# Check if Yarn is installed
if ! command -v yarn &> /dev/null; then
    echo "Yarn is not installed. Installing Yarn..."
    # Install Yarn using npm (Node.js package manager)
    npm install -g yarn
else
    version=$(yarn -v)
    major_minor_version=${version%.*}
    if [ "$major_minor_version" != "1.22" ]; then
        echo "Yarn version 1.22 is not installed. Please install Yarn version 1.22."
        exit 1
    fi
fi

# Define the project directory where your front-end application code is located
PROJECT_DIR="$PWD/chat-ui"

# Navigate to the project directory
cd $PROJECT_DIR
echo "Current working directory: $PWD"

# Delete node_modules directory if it exists
echo "Deleting previos project dependencies..."
if [ -d "node_modules" ]; then
    rm -rf node_modules
fi

# Delete .next directory if it exists
if [ -d ".next" ]; then
    rm -rf .next
fi

# Delete yarn.lock file if it exists
if [ -f "yarn.lock" ]; then
    rm yarn.lock
fi


# Install project dependencies
yarn install
if [ $? -ne 0 ]; then
    echo "yarn install failed"
    exit 1
fi

# Build the front-end application
yarn build
if [ $? -ne 0 ]; then
    echo "yarn build failed"
    exit 1
fi