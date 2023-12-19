#!/bin/bash

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Installing Node.js..."
    # Install Node.js using a package manager (e.g., apt, yum, or a custom method)
    # Replace the installation command with the appropriate one for your CML environment
    # Example using a package manager (you may need sudo privileges):
    # sudo apt-get install -y nodejs
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

# Install project dependencies
yarn install

# Build the front-end application
yarn build

# Start the front-end application
yarn start
