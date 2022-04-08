#!/bin/bash
python manage.py db upgrade
echo "DB migration done."
python main.py