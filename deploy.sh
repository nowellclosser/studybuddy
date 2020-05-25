set -e

git push origin master

ssh -T ec2-user@52.39.88.38 << EOF
cd studybuddy
git pull origin master
ls
mv crontab /var/spool/cron/ec2-user
logout
EOF
