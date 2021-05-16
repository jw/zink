#!/usr/bin/env bash

# some bash magic
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT=${SCRIPT_DIR}/..

# uikit
UIKIT_ROOT=${PROJECT_ROOT}/theme/uikit-3.6.20/
UIKIT_CSS=${UIKIT_ROOT}/dist/css
UIKIT_JS=${UIKIT_ROOT}/dist/js

# static
STATIC_ROOT=${PROJECT_ROOT}/zink/static
STATIC_CSS=${STATIC_ROOT}/css
STATIC_JS=${STATIC_ROOT}/js

# copy created css and js files
cp ${UIKIT_CSS}/uikit.elevenbits.min.css ${STATIC_CSS}
cp ${UIKIT_JS}/uikit.min.js ${STATIC_JS}
cp ${UIKIT_JS}/uikit-icons.min.js ${STATIC_JS}

echo "Copied js to ${STATIC_JS}."
echo "Copied css and ElevenBits theme to ${STATIC_CSS}."
