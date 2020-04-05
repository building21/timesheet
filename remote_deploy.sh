#!/bin/bash

set -e

source .remote-deploy.env

ssh -T $REMOTE_DEPLOY_USER@$REMOTE_DEPLOY_HOST <<EOF
set -e
cd timesheet
echo '>>> UPDATING SOURCES'
git fetch
git reset --hard origin/master
echo '>>> INSTALLING DEPENDENCIES'
sudo apt-get install uwsgi -y
sudo apt-get install uwsgi-plugin-python3 -y
python3 -m venv .
. bin/activate
pip install -r requirements.txt
deactivate
echo '>>> RELOAD SYSTEMD UWSGI PROCESS'
echo '>>> This may take a while...'
sudo cp timesheet.service /etc/systemd/system/timesheet.service
sudo systemctl daemon-reload
sudo systemctl restart timesheet
sudo systemctl enable timesheet
EOF

echo '>>> DEPLOY COMPLETE'

