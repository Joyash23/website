#!/bin/sh
export PORT=9090
export DBNAME=test.db
export WEB_DOMAIN=localhost:8080
export CORS_DOMAIN="*"
# Assume SMTP is empty by default
export SMTP_SERVER="${SMTP_SERVER:-""}"
quickweb run api/ -l localhost
