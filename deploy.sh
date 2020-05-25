set -e

git push origin master

# I irretrievably messed up the cron permissions,
# hence the nonstandard crontab installation
ssh -T ec2-user@52.39.88.38 << EOF
set -e
cd studybuddy
git pull origin master
cat crontab-ec2-user >> /var/spool/cron/ec2-user
logout
EOF
