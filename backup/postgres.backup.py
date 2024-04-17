import os
import subprocess
import datetime
import psycopg2
import boto3

# Database connection details
host = ""
user = ""
password = ""
bucket_name = 'linthr-dev-db-backups'
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# backup_dir = f"/home/raveen/linthr-backup/{now}"
backup_dir = f"/var/backups/linthr/{now}"
aws_access_key_id = ""
aws_secret_access_key = ""


if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)
    print(f"Folder '{backup_dir}' created.")
else:
    print(f"Folder '{backup_dir}' already exists.")

companies = [
    {
        "name": "company",
        "db_name": "company",
        "db_url": host,
        "db_username": user,
        "db_password": password,
        "db_port": 5432,
    }
]

conn = psycopg2.connect(host=host, database="company", user=user, password=password)

with conn.cursor() as cur:
    cur.execute(
        "SELECT name, db_name, db_url, db_username, db_password, db_port FROM public.lc_conf_companycredential"
    )
    db_rows = cur.fetchall()

    for row in db_rows:
        companies.append(
            {
                "name": row[0],
                "db_name": row[1],
                "db_url": row[2],
                "db_username": row[3],
                "db_password": row[4],
                "db_port": row[5],
            }
        )

for company in companies:
    dump_cmd = f"pg_dump -U {company['db_username']} -h {company['db_url']} -p {company['db_port']} -c {company['db_name']} > '{backup_dir}/{company['db_name']}.sql'"
    subprocess.call(dump_cmd, shell=True, env={"PGPASSWORD": company['db_password']})

conn.close()

# upload to s3
# Set up the AWS credentials and S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

# Set the S3 bucket name and the local folder path

# Walk through the local folder and upload each file
for root, dirs, files in os.walk(backup_dir):
    for file in files:
        local_file_path = os.path.join(root, file)
        s3_key = f"{now}/{file}"

        try:
            s3.upload_file(local_file_path, bucket_name, s3_key)
            print(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_key}")
        except Exception as e:
            print(f"Error uploading {local_file_path}: {e}")

print(f"Backup created successfully: {backup_dir}")
