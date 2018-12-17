import os
import opencryptobot.constants as con

from telegram import ParseMode
from opencryptobot.plugin import OpenCryptoPlugin, Category


class About(OpenCryptoPlugin):

    ABOUT_FILENAME = "about.md"

    def get_cmd(self):
        return "about"

    @OpenCryptoPlugin.send_typing
    @OpenCryptoPlugin.save_data
    def get_action(self, bot, update, args):
        about_file = os.path.join(con.RES_DIR, self.ABOUT_FILENAME)
        with open(about_file, "r", encoding="utf8") as file:
            content = file.readlines()

        update.message.reply_text(
            text="".join(content),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True)

    def get_usage(self):
        return None

    def get_description(self):
        return "Information about bot"

    def get_category(self):
        return Category.BOT
