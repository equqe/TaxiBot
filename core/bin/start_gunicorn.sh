#!/bin/bash
exec gunicorn  -c "/app/core/gunicorn_config.py" core.wsgi
