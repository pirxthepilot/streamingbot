#!/bin/bash

set -ue

PKGTMP_DIR="./pkgtmp"
LAMBDA_FUNC_FILE="./bot.py"
ZIP_FILE="$(pwd)/package.zip"

# Cleanup the pkgtmp dir
rm -rf $PKGTMP_DIR

# Install requirements (skip boto3)
pip install --target $PKGTMP_DIR -r requirements-lambda.txt

# Install streamingbot
pip install --target $PKGTMP_DIR .

# Copy the lambda entrypoint to pkgtmp
cp $LAMBDA_FUNC_FILE $PKGTMP_DIR/

# Zip it!
cd $PKGTMP_DIR
zip -r9 $ZIP_FILE .
