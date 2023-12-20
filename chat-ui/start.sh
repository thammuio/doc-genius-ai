#!/bin/bash

# Stop the script if any command fails
set -e

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm is not installed. Please install npm first."
    exit 1
fi

# Check if Yarn is installed
if ! command -v yarn &> /dev/null; then
    echo "Yarn is not installed. Installing Yarn..."
    # Install Yarn using npm (Node.js package manager)
    npm install -g yarn
fi

# Define the project directory where your front-end application code is located
PROJECT_DIR="$PWD/chat-ui"

# Navigate to the project directory
cd $PROJECT_DIR
echo "Current working directory: $PWD"

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

# Start the front-end application
yarn start
if [ $? -ne 0 ]; then
    echo "yarn start failed"
    exit 1
fi
