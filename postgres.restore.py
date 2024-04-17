import subprocess
import os
from getpass import getpass

# Database connection details
host = "localhost"
user = "postgres"
password = "root"
port = 5433

# Backup directory
backup_dir = "/home/raveen/backup"
dest_database = 'vayulo_cloud'

# Get the backup file name
backup_files = [f for f in os.listdir(backup_dir) if f.endswith(".sql")]
if not backup_files:
    print("No backup files found in the specified directory.")
    exit()

print(backup_files)

for backup_file in backup_files:
    backup_file = os.path.join(backup_dir, backup_file)
    database = backup_file.split(".")[-2]
    if database != dest_database:
        continue
    # Loop through each database and restore the backup
    # Create the database if it doesn't exist
    create_db_cmd = (
        f"psql -U {user} -h {host} -p {port} -c 'CREATE DATABASE {database};'"
    )
    try:
        subprocess.call(create_db_cmd, shell=True, env={"PGPASSWORD": password})
    except subprocess.CalledProcessError as e:
        if e.returncode != 1:  # Ignore error code 1 (database already exists)
            raise
    restore_cmd = (
        f"pg_restore -U {user} -h {host} -p 5433 -Fc -d {database} {backup_file}"
    )
    subprocess.call(restore_cmd, shell=True, env={"PGPASSWORD": password})

print("Restore completed successfully.")
