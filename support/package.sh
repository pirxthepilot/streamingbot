#!/bin/bash
# Collect the Pythons and zip into a package for Lambda
#
# These envvars must already be declared:
#   PKGTMP_DIR
#   LAMBDA_FUNC_FILE
#   ZIP_FILE

set -ue


## Cleanup the pkgtmp dir
printf "Cleaning up ${PKGTMP_DIR}...\n\n"
rm -rf $PKGTMP_DIR

## Pythons
printf "Compiling python packages into ${PKGTMP_DIR}...\n\n"

# Install requirements (skip boto3)
pip install --target $PKGTMP_DIR -r requirements-lambda.txt

# Install streamingbot
pip install --target $PKGTMP_DIR .

# Copy the lambda entrypoint to pkgtmp
cp $LAMBDA_FUNC_FILE $PKGTMP_DIR/

# Zip it!
printf "Zipping the packages as ${ZIP_FILE}...\n\n"
cd $PKGTMP_DIR
zip -r9 $ZIP_FILE .

printf "\nAll done!\n"
