#!/bin/bash
ACCOUNT_NAME=$1
CONTAINER_NAME=$2
BLOB_NAME=$3

if [ $(az storage blob exists --account-name $ACCOUNT_NAME --container-name $CONTAINER_NAME --name $BLOB_NAME --auth-mode login -o tsv) = "True" ]
then
  az storage blob delete --account-name $ACCOUNT_NAME --container-name $CONTAINER_NAME --name $BLOB_NAME --auth-mode login
  echo "$BLOB_NAME deleted from $ACCOUNT_NAME"
else
  echo "$BLOB_NAME does not exist in $ACCOUNT_NAME"
fi