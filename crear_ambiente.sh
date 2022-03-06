sudo apt-get update && sudo apt-get install -y screen libfuzzy-dev libsndfile1 ffmpeg python3.7 python3.7-venv libpython3.7-dev

/usr/bin/python3.7 -m pip install virtualenv
/usr/bin/python3.7 -m venv ASR

source ASR/bin/activate

pip install --upgrade pip
pip install wheel
pip install Cython

# pip install -r requirements.txt

user=$(whoami)
dir_actual=$(pwd)
echo "source $dir_actual/ASR/bin/activate" >> /home/$user/.bashrc
