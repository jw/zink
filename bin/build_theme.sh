#!/usr/bin/env bash

# some bash magic
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT=${SCRIPT_DIR}/..

cwd=$(pwd)

UIKIT_ROOT=${PROJECT_ROOT}/theme/uikit-3.6.20/

cd ${UIKIT_ROOT}
mkdir -p custom
cp ../elevenbits.less custom
yarn
yarn compile

cd ${cwd}
