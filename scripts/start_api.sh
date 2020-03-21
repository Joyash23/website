#!/bin/sh
export PORT=9090
export DBNAME=test.db
export WEB_DOMAIN=localhost:8080
export CORS_DOMAIN="*"
export SMTP_SERVER="localhost"
quickweb run api/ -l localhost
