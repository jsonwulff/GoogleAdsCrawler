#!/bin/bash
#
# Based of this script:
# https://gist.github.com/codeinthehole/26b37efa67041e1307db

echo "Starting installing..."

# Check for Homebrew, install if we don't have it
if test ! $(which brew); then
    echo "Installaing homebrew..."
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi

# Update homebrew recipes
echo "Updating brew..."
brew update

# Install git
echo "Installing git..."
brew install git

# Install python
echo "Installing python..."
brew install python3

echo "Cleaning up..."
brew cleanup

echo "Updating pip..."
sudo pip3 install --upgrade pip

echo "Installing Python packages..."
PYTHON_PACKAGES=(
    requests
    beautifulsoup4
    xlsxwriter
)

sudo pip3 install ${PYTHON_PACKAGES[@]}