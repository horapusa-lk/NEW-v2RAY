import os
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import subprocess
import psutil
import requests
sudo = 1436625686

r = requests.get('https://ip4.seeip.org')
IP_address = r.text
UUID = "890f636a-2608-4200-b05b-ac65fd4e11df"

# with open("/root/bot/bot.token", "r") as token:
#     bot_token = token.read()
#     bot_token = str(bot_token)

bot_token = "5662958094:AAFTQWRLmlzjjFFFuZhQuPZhZI4R_0HVxCk"
updater = Updater(bot_token, use_context=True)


def start(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        update.message.reply_text("""Hello sir, Welcome to the Hora_Pusa-server-manager-bot.
    Please write
    /help to see the commands available.""")


def help(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        update.message.reply_text("""Available Commands :-
        /speed_test - test server speed.
        /hardware_usage - check hardware usage.
        /vless_config - get the vless config.
        /reboot_server - reboot the server.""")


def speed_test(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        try:
            import speedtest

            # If you want to test against a specific server
            # servers = [1234]

            threads = None
            # If you want to use a single threaded test
            # threads = 1

            s = speedtest.Speedtest()
            s.get_best_server()
            s.download(threads=threads)
            s.upload(threads=threads)
            s.results.share()

            results_dict = s.results.dict()
            print(results_dict["share"])
            update.message.chat.send_photo(results_dict["share"])

        except:
            update.message.reply_text("speedtest faild.")


def unknown(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        update.message.reply_text(
            "Sorry '%s' is not a valid command" % update.message.text)


def reboot_server(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        try:
            update.message.reply_text("Rebooting...")
            os.system("reboot")
        except:
            update.message.reply_text("Reboot faild.")


def vless_config(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        update.message.reply_text(f"vless://{UUID}@{IP_address}:443?security=xtls&encryption=none&headerType=none&type=tcp&flow=xtls-rprx-direct&sni=your.package.sni#Horapusa+VPN")


def hardware_usage(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            hardware_usage = f"""
        + - + - + - + - + -+ +-+ -+-+ -+
        |S|y|s|t|e|m| |I|n|f|o|
        + -+ -+-+-+ -+ - + +-+ -+-+ -+
        CPU : {cpu}%
        RAM : {ram}%
        """
            update.message.reply_text(hardware_usage)
        except:
            update.message.reply_photo("faild to get hardware info.")

def unknown_text(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        update.message.reply_text(
            "Sorry I can't recognize you , you said '%s'" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('speed_test', speed_test))
updater.dispatcher.add_handler(CommandHandler('hardware_usage', hardware_usage))
updater.dispatcher.add_handler(CommandHandler('vless_config', vless_config))
updater.dispatcher.add_handler(CommandHandler('reboot_server', reboot_server))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown))  # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()


#!/usr/bin/env python

