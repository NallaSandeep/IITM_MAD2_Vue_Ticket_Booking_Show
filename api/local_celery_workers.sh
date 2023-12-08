#! /bin/sh
echo "======================================================================"
echo "Welcome to to the celery workers. This will setup the local virtual env."
echo "And then it will initialize the celery broker and celery backend."
echo "Make sure redis is up and running."
echo "Make sure to run this on Linux environment or Windows WSL (Ubuntu)."
echo "Use Docker Desktop to start redis."
echo "----------------------------------------------------------------------"
if [ -d ".env" ]; then
    echo "Enabling virtual env"
else
    echo "No Virtual env. Please run setup.sh first"
    exit N
fi
sleep 5s
# Activate virtual env
.env/bin/activate
export ENV=development
# To run celery workers
python3 -m celery -A main.celery worker --loglevel=info

sleep 10s
