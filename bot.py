from subprocess import PIPE, run
import platform
import GPUtil
from termcolor import colored
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import psutil
from config import *


def add_user(username, password, vail_dates):
    try:
        os.system(f'useradd -e {vail_dates} -M -N -s /bin/false {username} && echo "{username}:{password}" | chpasswd &&')
        return "User added succesfully."
    except Exception:
        return "Faild to add user."


def del_user(username):
    try:
        os.system(f"userdel {username}")
        return f"Successfully deleted user {username}"
    except Exception:
        return "Faild to delete user"


def list_users():
    def out(command):
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        return result.stdout
    try:
        output = out("awk -F: '$3>=1000 {print $1}' /etc/passwd | grep -v nobody")
        return output
    except Exception:
        return "Faild to list users"


def unit(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def clr(text):
    colorgrn = colored(f"{text}", "green")
    return colorgrn


def monitor():
    gpus = GPUtil.getGPUs()
    uname = platform.uname()
    cpufreq = psutil.cpu_freq()
    mem = psutil.virtual_memory()
    gpus = GPUtil.getGPUs()
    internet = psutil.net_io_counters()
    sys = uname.system
    core = psutil.cpu_count(logical=True)
    cpu_freq_mx = cpufreq.max
    mem_total = (int(mem.total)) / (1024 * 1024 * 1024)

    gpu_list = []
    for gpu in gpus:
        gpu_name = gpu.name
        gpu_total_memory = f"{gpu.memoryTotal}MB"
        gpu_temperature = f"{gpu.temperature} °C"
        gpu_list.append((gpu_name, gpu_total_memory))

    g_pu = (gpu_list[0])[0]
    g_pu_mem = (gpu_list[0])[1]
    output = f"""
    {"=" * 20} SYSTEM Info {"=" * 20}
            System       - {sys}
            Total Cores  - {core} Cores
            Cpu Usage    - {psutil.cpu_percent()}%
            Max Cpu Freq - {cpu_freq_mx}MHZ
            Total Ram    - {round(mem_total)}GB
            Ram in Use   - {unit(mem.used)} | {mem.percent}%
            Gpu          - {g_pu}
            Gpu Memory   - {g_pu_mem}
    {"=" * 20} Internet {"=" * 24}        
            Data Sent    - {unit(internet.bytes_sent)}
            Data Receive - {unit(internet.bytes_recv)}

    """
    return output


###############################################################################################

sudo = 1436625686

r = requests.get('https://ip4.seeip.org')
IP_address = r.text

# with open("/root/bot/bot.token", "r") as token:
#     bot_token = token.read()
#     bot_token = str(bot_token)

bot_token = "5662958094:AAEq3ddcqaPiAMi_6G9yqJKT5vW60CwtyfQ"
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
        /vless - create v2ray vless config.
        /vmess - create v2ray vmess config.
        /v2ray_all_configs - show all v2ray configs.
        /reboot_server - reboot the server.""")


def vless(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        port = update.message.text[7:]
        try:
            vless_config = vless_ws_gen(port)
            update.message.reply_text(vless_config)
        except Exception:
            update.message.reply_text("Faild to create vless config.")


def vmess(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        port = update.message.text[7:]
        try:
            vmess_config = vless_ws_gen(port)
            update.message.reply_text(vmess_config)
        except Exception:
            update.message.reply_text("Faild to create vmess config.")


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

        except Exception:
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
        except Exception:
            update.message.reply_text("Reboot faild.")


def hardware_usage(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        try:
            sys_usage = monitor()
            update.message.reply_text(sys_usage)
        except Exception:
            update.message.reply_photo("faild to get hardware info.")


def unknown_text(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        update.message.reply_text(
            "Sorry I can't recognize you , you said '%s'" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('vless', vless))
updater.dispatcher.add_handler(CommandHandler('vmess', vmess))
# updater.dispatcher.add_handler(CommandHandler('v2ray_all_configs', v2ray_all_configs))
updater.dispatcher.add_handler(CommandHandler('speed_test', speed_test))
updater.dispatcher.add_handler(CommandHandler('hardware_usage', hardware_usage))
updater.dispatcher.add_handler(CommandHandler('reboot_server', reboot_server))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown))  # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()


#!/usr/bin/env python


