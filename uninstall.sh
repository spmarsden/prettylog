#!/bin/bash

# Get the path to this script in order to make its behaviour consistend
# regardless of where it is called from.
dir_root=$(realpath $(dirname -- "${BASH_SOURCE[0]}"))

echo "Uninstalling prettylog"

for target in \
    "${dir_root}/venv"
do
    echo -n "  Deleting: ${target} ... "
    rm -rf -- "${target}"
    echo "done"
done