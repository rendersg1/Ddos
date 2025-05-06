#!/bin/bash

# This script updates the GitHub repository with the new code

echo "Updating GitHub repository at https://github.com/rendersg1/Ddos"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed. Please install git first."
    exit 1
fi

# Clone the repository if it doesn't exist
if [ ! -d "repo" ]; then
    echo "Cloning repository..."
    git clone https://github.com/rendersg1/Ddos.git repo
    if [ $? -ne 0 ]; then
        echo "Error: Failed to clone repository."
        exit 1
    fi
fi

# Copy files to the repository
echo "Copying files to repository..."
cp start.py repo/
cp easy_run.py repo/
cp termux_install.sh repo/
cp cloud_install.sh repo/
cp README.md repo/

# Change to the repository directory
cd repo

# Add all files
echo "Adding files to git..."
git add .

# Commit changes
echo "Committing changes..."
git commit -m "Complete rewrite of DDoS tool with async architecture"

# Push changes
echo "Pushing changes to GitHub..."
git push

if [ $? -eq 0 ]; then
    echo "Successfully updated GitHub repository!"
else
    echo "Error: Failed to push changes. You may need to configure git credentials."
    echo "Run the following commands manually:"
    echo "git config --global user.email 'youremail@example.com'"
    echo "git config --global user.name 'Your Name'"
    echo "git config --global credential.helper store"
    echo "Then try again."
    exit 1
fi

echo "Done."
