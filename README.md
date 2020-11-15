A system for scheduling studying and review of technical books backed by Trello.


TODO/NOTES:
- Cards should really be a separate table from book sections
- Formalize/document host setup: python3.8 (+ special sqlite stuff), ssh key, git, TRELLO_TOKEN, nginx
- TRELLO TOKEN goes in /etc/environment
- logrotate on server
- set last reviewed date for review cards
- how to view db remotely
- daemonize gunicorn
- make webapp deploy optional
- check in and deploy nginx config
- better way to run schedule study without sshing

- gunicorn webapp.app:app -b :5002 -w 4 -p /var/run/studybuddy/studybuddy.pid is running in a screen session called studybuddy, where logs can be seen
