apt -y install python3.10 python3.10-venv python3-pip

pip3 install -r requirements.txt
mkdir /root/bot
cp bot.py /root/bot
chmod +x /root/bot/bot.sh
cp horapusa.service /etc/systemd/system/
sudo systemctl enable horapusa.service
bash v2ray.sh
