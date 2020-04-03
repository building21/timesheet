#!/bin/sh

files="$(find "$(dirname $0)/static/pdf" -iname "*.pdf" -mmin +30 | wc -l)"
echo "[`date`]: Deleted $files generated pdf files"

find "$(dirname $0)/static/pdf" -iname "*.pdf" -mmin +30 -delete

# */30 * * * * /home/b21/timesheet/cleanup_timesheets.sh >> /home/b21/cleanup.log 2>&1