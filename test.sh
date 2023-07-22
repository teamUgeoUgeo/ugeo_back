#!/bin/bash

poetry run alembic upgrade head
poetry run pytest --log-cli-level DEBUG -s