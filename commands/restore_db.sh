#!/bin/bash
SECONDS=0
PROJECT_PATH=/app
LATEST_BACKUP_PATH=${PROJECT_PATH}/db_backups/latest.backup
export DJANGO_SETTINGS_MODULE=Opes.settings


cd "${PROJECT_PATH}"
source venv/bin/activate


DATABASE=$(echo "from django.conf import settings;
print(settings.DATABASES['default']['NAME'])" | python manage.py  hell -i python)
USER=$(echo "from django.conf import settings;
print(settings.DATABASES['default']['USER'])" | python manage.py shell -i python)
PASSWORD=$(echo "from django.conf import settings;
print(settings.DATABASES['default']['PASSWORD'])" | python manage.py shell -i python)
echo "=== Restoring DB from a Backup ==="
echo "- Recreate the database"
psql --dbname=$POSTGRES_DB --command='SELECT
pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity
WHERE datname = current_database() AND pid <> pg_backend_pid();'

dropdb $POSTGRES_DB
createdb --username=$POSTGRES_USER $POSTGRES_DB
echo "- Fill the database with schema and data"
zcat "${LATEST_BACKUP_PATH}.gz" | python manage.py dbshell
duration=$SECONDS
echo "------------------------------------------"
echo "The operation took $((duration / 60)) minutes and $((duration % 60)) seconds."