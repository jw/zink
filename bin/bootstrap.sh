#!/usr/bin/env bash

# some bash magic
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT=${SCRIPT_DIR}/..

cwd=$(pwd)

THEME_ROOT=${PROJECT_ROOT}/theme
# UIKIT_ROOT=${THEME_ROOT}//uikit-3.6.20/

cd ${THEME_ROOT}
wget https://github.com/uikit/uikit/archive/refs/tags/v3.6.20.tar.gz
tar xvfz v3.6.20.tar.gz
rm v3.6.20.tar.gz

cd ${cwd}
