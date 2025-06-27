#!/bin/bash

# Get the path to this script in order to make its behaviour consistend
# regardless of where it is called from.
dir_root=$(realpath $(dirname -- "${BASH_SOURCE[0]}"))

version=$(cat "${dir_root}/version.txt")
echo "Installing PrettyLog ${version}"

# Ensure a clean installation be first uninstalling. Don't delete config files.
$dir_root/uninstall.sh -n

# Create a virtual environment.
dir_venv="${dir_root}/venv"
echo "Creating virtual environment: ${dir_venv}"
python3 -m venv "${dir_venv}"

# Install the package.
$dir_venv/bin/python -m pip install -e "${dir_root}"