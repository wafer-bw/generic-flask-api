#!/bin/bash
gunicorn 'app.factory:create_app("Prod")' --bind 0.0.0.0:8000 --workers 4 --name api --log-level info
