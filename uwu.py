from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
from mss import mss
import subprocess
import re

url_regex = re.compile(r'(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|'
                       r'biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|'
                       r'am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|'
                       r'ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|'
                       r'er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|'
                       r'hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|'
                       r'la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|'
                       r'mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|'
                       r'qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|'
                       r'td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|'
                       r'ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+'
                       r'(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:".,<>?«»“”‘’])|'
                       r'(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.]'
                       r'(?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|'
                       r'travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|'
                       r'bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|'
                       r'dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|'
                       r'gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|'
                       r'km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|'
                       r'mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|'
                       r'pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|'
                       r'sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|'
                       r'vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))')


class Control:
    def __init__(self, token: str):
        self.authorized = False
        self.updater = Updater(token, use_context=True)
        self.dp = self.updater.dispatcher
        self.sys_info = {}
        self.bot_messages = list()
        self.boss_messages = list()

        self.get_system_info()

    def check_authorization(self, update, context):
        self.authorized = int(update.message.from_user['id']) == 835917180 \
                          and update.message.from_user['username'] == 'acangmaul'

        if not self.authorized:
            update.message.reply_text("I'm sorry but you're not my boss :(")

        return self.authorized

    def start_callback(self, update, context):
        if self.check_authorization(update, context):
            update.message.reply_text("Hi boss!")

    def command_callback(self, update, context):
        if self.check_authorization(update, context):
            message = str(update.message.text)

            if message == "bye":
                update.message.reply_text("Goodbye boss! :)", quote=True)
                if len(self.bot_messages) > 0:
                    for bot_message in self.bot_messages:
                        bot_message.delete()
                if len(self.bot_messages) > 0:
                    for boss_message in self.boss_messages:
                        boss_message.delete()
                self.updater.stop()
                return

            self.bot_messages.append(update.message.reply_text("As you wish boss :D", quote=True))
            self.boss_messages.append(update.message)

            if message == "uptime":
                boot_time = datetime.strptime(self.sys_info["System Boot Time"], '%d/%m/%Y, %H:%M:%S')
                up_time = self.convert_time_delta(datetime.now() - boot_time)
                self.bot_messages[len(self.bot_messages) - 1] \
                    .edit_text(text=f"Boss, your computer has been up for:\n\n"
                                    f"{up_time[0]} Hour(s) {up_time[1]} Minute(s) and "
                                    f"{up_time[2]} Second(s)")
                return

            if message == "ss":
                self.take_screenshot()
                with open("ss.png", "rb") as ss:
                    self.bot_messages.append(context.bot.send_document(chat_id=update.effective_chat.id, document=ss))
                return

            if message == "status":
                info = self.sys_info
                self.bot_messages[len(self.bot_messages) - 1] \
                    .edit_text(f"Host Name: {info['Host Name']}\n\n"
                               f"OS Name: {info['OS Name']}\n\n"
                               f"OS Version: {info['OS Version']}\n\n"
                               f"Product ID: {info['Product ID']}\n\n"
                               f"Registered Owner: {info['Registered Owner']}\n\n"
                               f"Original Install Date: {info['Original Install Date']}\n\n"
                               f"System Boot Time: {info['System Boot Time']}")
                return

            command = self.get_command(message)
            response = self.execute(command)

            if response[1] != '':
                self.bot_messages[len(self.bot_messages) - 1]\
                    .edit_text(text=f"I'm sorry boss, but there's an error when I tried to do that :(\n\n"
                                    f"Reason: {response[1]}")

    def get_system_info(self):
        if len(self.sys_info) == 0:
            res = self.execute("SYSTEMINFO")[0]
            opts = ["Host Name", "OS Name", "OS Version", "Product ID",
                    "Registered Owner", "Original Install Date", "System Boot Time"]

            for opt in opts:
                self.sys_info[opt] = [item.strip() for item in
                                      re.findall(r"%s:\w*(.*?)\n" % opt, res, re.IGNORECASE)][0]

    @staticmethod
    def take_screenshot():
        with mss() as sct:
            sct.compression_level = 1
            sct.shot(output="ss.png")

    @staticmethod
    def convert_time_delta(td):
        return [td.seconds // 3600, (td.seconds // 60) % 60, td.seconds % 60]

    @staticmethod
    def execute(command: str):
        return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"). \
            communicate()

    @staticmethod
    def get_command(command: str):
        ret = command
        if re.match(url_regex, command):
            ret = "start " + ("https://" if command.find("http") == -1 else "") + command
        elif command == "lock":
            ret = "rundll32.exe user32.dll,LockWorkStation"
        elif command == "shutdown":
            ret = "shutdown /s"
        elif command == "restart":
            ret = "shutdown /r"
        elif command.find("kill") != -1:
            ret = f"taskkill /F /IM {command.split(' ')[1]}.exe"
        return ret

    @staticmethod
    def delete_recent_message(update, context):
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)

    def start(self):
        self.dp.add_handler(CommandHandler("start", self.start_callback))
        self.dp.add_handler(MessageHandler(Filters.text & (~Filters.command), self.command_callback))
        self.updater.start_polling()
        self.updater.idle()


def main():
    control = Control("1366436196:AAE2qgBYdv0m3-F5-6wU6Z1QPEW-KJqEyzo")
    control.start()


if __name__ == '__main__':
    main()
