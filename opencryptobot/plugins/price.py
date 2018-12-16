import opencryptobot.emoji as emo

from telegram import ParseMode
from opencryptobot.api.coingecko import CoinGecko
from opencryptobot.plugin import OpenCryptoPlugin


class Price(OpenCryptoPlugin):

    def get_cmd(self):
        return "p"

    @OpenCryptoPlugin.send_typing
    @OpenCryptoPlugin.save_data
    def get_action(self, bot, update, args):
        vs_cur = str()

        if not args:
            if update.message:
                update.message.reply_text(
                    text=f"Usage:\n{self.get_usage(bot.name)}",
                    parse_mode=ParseMode.MARKDOWN)
            return

        # Coin name
        if "-" in args[0]:
            pair = args[0].split("-", 1)
            vs_cur = pair[0].upper()
            coin = pair[1].upper()
        else:
            coin = args[0].upper()

        # Exchange name
        exchange = str()
        if len(args) > 1:
            exchange = args[1]

        cg = CoinGecko()

        # Get coin ID and name
        coin_id = str()
        for entry in cg.get_coins_list(use_cache=True):
            if entry["symbol"].upper() == coin:
                coin_id = entry["id"]
                break

        msg = str()

        if exchange:
            result = cg.get_coin_by_id(coin_id)

            if result:
                vs_list = list()

                if vs_cur:
                    vs_list = vs_cur.split(",")

                for ticker in result["tickers"]:
                    if ticker["market"]["name"].upper() == exchange.upper():
                        base_coin = ticker["target"]
                        if vs_list:
                            if base_coin in vs_list:
                                price = self.format(ticker["last"])
                                msg += f"`{base_coin}: {price}`\n"
                        else:
                            price = self.format(ticker["last"])
                            msg += f"`{base_coin}: {price}`\n"
        else:
            if not vs_cur:
                if coin == "BTC":
                    vs_cur = "ETH,EUR,USD"
                elif coin == "ETH":
                    vs_cur = "BTC,EUR,USD"
                else:
                    vs_cur = "BTC,ETH,EUR,USD"

            result = cg.get_simple_price(coin_id, vs_cur)

            if result:
                for _, prices in result.items():
                    for symbol, price in prices.items():
                        price = self.format(price)
                        msg += f"`{symbol.upper()}: {price}`\n"

        if msg:
            if exchange:
                msg = f"`Price of {coin} on {exchange.capitalize()}`\n\n" + msg
            else:
                msg = f"`Price of {coin}`\n\n" + msg
        else:
            msg = f"{emo.ERROR} Can't retrieve data for *{coin}*"

        if update.message:
            update.message.reply_text(
                text=msg,
                parse_mode=ParseMode.MARKDOWN)
        else:
            return msg

    def get_usage(self, bot_name):
        return f"`" \
               f"/{self.get_cmd()} <coin>\n" \
               f"/{self.get_cmd()} <vs coin>-<coin>\n" \
               f"{bot_name} /{self.get_cmd()} <coin>.\n" \
               f"{bot_name} /{self.get_cmd()} <vs coin>-<coin>." \
               f"`"

    def get_description(self):
        return "Coin price"

    def inline_mode(self):
        return True
