#! /bin/sh
echo "======================================================================"
echo "Welcome to to the celery schedulers. This will enable schedulers."
echo "Make sure to run this on Linux environment or Windows WSL (Ubuntu)."
echo "Make sure redis is up and running."
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
# To run celery schedulers
python3 -m celery -A main.celery beat --max-interval 1 -l info
