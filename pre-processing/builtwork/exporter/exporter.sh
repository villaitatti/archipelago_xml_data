#!/bin/bash

# Load database connection info
source .env 

# Read query into a variable
sql="$(cat query.sql)"

# Connect to the database, run the query, then disconnect
PGPASSWORD="$POSTGRES_PASSWORD" psql -t -A \
-h "$POSTGRES_HOST" \
-p "$POSTGRES_PORT" \
-d "$POSTGRES_DATABASE" \
-U "$POSTGRES_USERNAME" \
-c "$sql" 