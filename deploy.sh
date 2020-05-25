set -e

git push origin master

ssh -T ec2-user@52.39.88.38 << EOF
set -e
cd studybuddy
git pull origin master
> /var/spool/cron/ec2-user
echo TRELLO_TOKEN=$TRELLO_TOKEN >> /var/spool/cron/ec2-user
cat crontab-ec2-user >> /var/spool/cron/ec2-user
logout
EOF
