### BACKUP AND RESTORE

1. Note down all the installed apps
   bench --site .. list-apps
2. Backup using the command
   bench --site .. backup
3. copy the site folder to local
   docker cp contianer:path ./backup
4. start the new docker containers and add an new app with correct name, header and port
   check the docker-compose file for reference
   docker compose down
   docker compose up
5. login to frontend container
   docker exec -it .. bash
6. create a new site
   bench new-site ..
7. install all the apps
   bench --site .. install-app ..
8. logout of the container and copy the backup files
   docker cp ./backup container:/home/frappe/frappe-bench/sites/backup
9. login back into the contianer
   docker exec -it .. bash
10. copy the backup files from backup folder to our site
    cd sites
    cp -r backup/private/backup [site]/private
11. Run the backup command
    bench --site .. restore --force [sql path]
12. Migrate the site once
    bench --site .. Migrate
13. Backup the files as well ?

14. Our site is ready.
