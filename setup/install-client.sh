sudo apt update
sudo apt install python3-dev python3-pip python3-venv

python3 -m venv --system-site-packages ./venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r ../requirements.txt
