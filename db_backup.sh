# A quick and dirty script to create weekly backups of the db
# run with cron

DATE_STR=$(date '+%Y_%W')
FILE_NAME="db_backup_"
FILE_NAME+=${DATE_STR}
FILE_NAME+=".db"
cp /home/matt/trackr/trackr.db /home/matt/trackr/db_backups/${FILE_NAME}
