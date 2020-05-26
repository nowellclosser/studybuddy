set -e

echo "***************** Pushing to remote master"
git push origin master

# I irretrievably messed up the cron permissions,
# hence the nonstandard crontab installation
ssh -T ec2-user@52.39.88.38 << EOF
set -e
cd studybuddy
echo "***************** Pushing master onto server"
git pull origin master
echo "***************** Replacing crontab"
crontab crontab-ec2-user
echo "***************** Deploy complete"
EOF
