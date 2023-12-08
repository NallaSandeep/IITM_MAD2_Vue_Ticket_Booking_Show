# Pre-requisites:

Have python installed and set the path variable for it
Have pip installed and set the path variable for it

# How to setup .env folder?

Execute the command
.\local_setup.sh
bash local_setup.sh

# How to run code?

Execute the command
.\local_run.sh
bash local_run.sh

# How to run celery workers?

Execute the command
.\local_workers.sh
bash local_workers.sh

# How to enable celery schedulers?

Execute the command
.\local_beat.sh
bash local_beat.sh

# How to install the required libraries?

pip install -r requirements.txt

# Change directory in WSL

cd /mnt/e/Personal\ documents/IIT\ Online\ Madras/Diploma/Programming/Modern\ Application\ Development\ 2/Project/Ticket\ show\ app/api

# Command to run a daily reminder job

celery -A main.celery call application.tasks.reminder_job

# Command to run a monthly emailable report job

celery -A main.celery call application.tasks.monthly_emailable_report

# How to verify emails?

Download mailhog exe and run it
