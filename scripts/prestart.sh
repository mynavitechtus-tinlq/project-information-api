#! /usr/bin/env sh

# Let the DB start

# Run migrations
alembic upgrade head
