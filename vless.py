import os
import requests

bot_token = input("Enter Bot toekn : ")
with open("bot.token", "w") as token:
    token.write(bot_token)

UUID = "890f636a-2608-4200-b05b-ac65fd4e11df"
os.system("rm -rf /etc/localtime")
os.system("cp /usr/share/zoneinfo/Asia/Colombo /etc/localtime")

# Updating the system
os.system("apt update")
os.system("apt upgrade -y")
os.system("apt purge iptables-persistent")
os.system("apt install ufw")
os.system("ufw allow 'OpenSSH'")
os.system("ufw allow 443/tcp")
os.system("ufw enable")
os.system('bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install"')
os.system("rm -rf /usr/local/etc/xray/config.json")
os.system("mv config.json /usr/local/etc/xray/")
os.system('openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=www.example.com" -keyout xray.key  -out xray.crt')
os.system("mkdir /etc/xray")
os.system("cp xray.key /etc/xray/xray.key")
os.system("cp xray.crt /etc/xray/xray.crt")
os.system("chmod 644 /etc/xray/xray.key")
os.system("systemctl enable xray")
os.system("systemctl restart xray")
os.system("curl -LJO https://raw.githubusercontent.com/teddysun/across/master/bbr.sh")
os.system("bash bbr.sh")
r = requests.get('https://ip4.seeip.org')
IP_address = r.text

print(f"""v2ray Vless Config
vless://{UUID}@{IP_address}:443?security=xtls&encryption=none&headerType=none&type=tcp&flow=xtls-rprx-direct&sni=your.package.sni#Horapusa+VPN""")


