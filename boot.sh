#!/bin/bash
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - campaign_tracker:app