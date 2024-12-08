#! /bin/bash

touch .env

echo "export DB_PASSWORD=$DB_PASSWORD" >> .env
echo "export DB_USER=$DB_USER" >> .env
echo "export DATABASE=$DATABASE" >> .env
echo "export HOST=$HOST" >> .env
echo "export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex())')" >> .env