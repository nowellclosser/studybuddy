set -e

ssh -T ec2-user@52.39.88.38 << 'EOF'
set -e
echo "***************** Committing db changes on server"
git commit -a -m "autocommitting db changes"
git push origin master
EOF

echo "***************** Pushing to remote master branch"
git pull origin master
git push origin master


ssh -T ec2-user@52.39.88.38 << 'EOF'
set -e
cd studybuddy

echo "***************** Pulling master onto server"
git pull origin master

echo "***************** Installing requirements"
source ve/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "***************** Replacing crontab"
crontab crontab-ec2-user

echo "***************** Reloading gunicorn"
kill -HUP $(cat /var/run/studybuddy/studybuddy.pid)

echo "***************** Deploy complete"
EOF
