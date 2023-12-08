#! /bin/sh
echo "======================================================================"
echo "Welcome to to the local run. This will setup the local virtual env and run the application."
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
python3 main.py
sleep 10s
