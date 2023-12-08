#! /bin/sh
echo "======================================================================"
echo "Welcome to to the setup. This will setup the local virtual env."
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
if [ -d ".env" ]; then
    echo ".env folder exists. Installing using pip"
else
    echo "creating .env and install using pip"
    python3 -m venv .env
fi
sleep 10s
echo "Activate virtual env"
.env/bin/activate
echo "Upgrade the PIP"
pip install --upgrade pip
pip install -r requirements.txt
echo "Work done"
