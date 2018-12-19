import inspect

from telegram import ChatAction
from opencryptobot.config import ConfigManager as Cfg


class OpenCryptoPlugin:

    def __init__(self, updater, db):
        self.updater = updater
        self.db = db

    @classmethod
    def send_typing(cls, func):
        def _send_typing_action(self, bot, update, **kwargs):
            if update.message:
                user_id = update.message.chat_id
            elif update.callback_query:
                user_id = update.callback_query.message.chat_id
            else:
                return func(self, bot, update, **kwargs)

            bot.send_chat_action(
                chat_id=user_id,
                action=ChatAction.TYPING)

            return func(self, bot, update, **kwargs)
        return _send_typing_action

    @classmethod
    def only_owner(cls, func):
        def _only_owner(self, bot, update, **kwargs):
            if Cfg.get("admin_id") == update.effective_user.id:
                return func(self, bot, update, **kwargs)

        return _only_owner

    @classmethod
    def save_data(cls, func):
        def _save_data(self, bot, update, **kwargs):
            if Cfg.get("use_db"):
                if update.message:
                    usr = update.message.from_user
                    cmd = update.message.text
                    self.db.save(usr, cmd)
                elif update.inline_query:
                    usr = update.effective_user
                    cmd = update.inline_query.query[:-1]
                    self.db.save(usr, cmd)

            return func(self, bot, update, **kwargs)
        return _save_data

    @classmethod
    def is_number(cls, string):
        try:
            float(string)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(string)
            return True
        except (TypeError, ValueError):
            pass

        return False

    # TODO: Still needed to distinguish between crypto and fiat?
    @classmethod
    def format(cls, value, decimals=None, force_length=True, template=None):
        try:
            if isinstance(value, str):
                value = value.replace(",", "")
            v = float(value)
        except Exception:
            return str(value)

        try:
            if isinstance(template, str):
                template = template.replace(",", "")
            t = float(template)
        except Exception:
            t = v

        try:
            decimals = int(decimals)
        except Exception:
            decimals = None

        if t < 1:
            if decimals:
                v = "{1:.{0}f}".format(decimals, v)
            else:
                v = "{0:.8f}".format(v)
        elif t < 100:
            if decimals:
                v = "{1:.{0}f}".format(decimals, v)
            else:
                v = "{0:.4f}".format(v)
        elif t < 10000:
            if decimals:
                v = "{1:,.{0}f}".format(decimals, v)
            else:
                v = "{0:,.2f}".format(v)
        else:
            v = "{0:,.0f}".format(v)

        if not force_length:
            while "." in v and v.endswith(("0", ".")):
                v = v[:-1]

        return v

    def get_cmd(self):
        method = inspect.currentframe().f_code.co_name
        raise NotImplementedError(f"Interface method '{method}' not implemented")

    def get_cmd_alt(self):
        return list()

    def get_action(self, bot, update, args):
        method = inspect.currentframe().f_code.co_name
        raise NotImplementedError(f"Interface method '{method}' not implemented")

    def get_usage(self):
        return None

    def get_description(self):
        return None

    def get_category(self):
        return None

    def inline_mode(self):
        return False


class Category:

    GENERAL = "General"
    PRICE = "Price"
    CHARTS = "Charts"
    NEWS = "News & Events"
    UTIL = "Utilities"
    BOT = "Bot"
    FUN = "Fun"

    @classmethod
    def get_categories(cls):
        categories = list()

        for k, v in vars(cls).items():
            if k.isupper() and isinstance(v, str):
                categories.append({k: v})

        return categories
