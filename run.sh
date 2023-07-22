#!/bin/bash

poetry run alembic upgrade head
poetry run uvicorn ugeougeo.main:app --host 0.0.0.0 --reload