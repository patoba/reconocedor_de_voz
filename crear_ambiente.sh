python3 -m virtualenv ASR

source ASR/bin/activate
pip install -r requirements.txt

user=whoami
echo "source ASR/bin/activate" >> /home/$user/.bashrc
