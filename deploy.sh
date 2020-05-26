set -e

echo "***************** Pushing to remote master branch"
git push origin master


ssh -T ec2-user@52.39.88.38 << EOF
set -e
cd studybuddy

echo "***************** Pulling master onto server"
git pull origin master

echo "***************** Installing requirements"
source ve/bin/activate
pip install -r requirements.txt

echo "***************** Replacing crontab"
crontab crontab-ec2-user

echo "Reloading gunicorn"
kill -HUP `cat studybuddy.pid`

echo "***************** Deploy complete"
EOF
