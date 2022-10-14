apt install speedtest-cli -y
apt install python3
apt install python3-pip
pip3 install python-telegram-bot requests
mkdir /root/bot
cp bot.py /root/bot
chmod +x /root/bot/bot.sh
cp horapusa.service /etc/systemd/system/
sudo systemctl enable horapusa.service
cp bot.token /root/bot
pip3 install psutil
python3 vless.py
reboot
