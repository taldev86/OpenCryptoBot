import json
import requests


class CoinGecko(object):

    _base_url = 'https://api.coingecko.com/api/v3/'
    _request_timeout = 120

    def __init__(self, api_base_url=None, request_timeout=None):
        if api_base_url:
            self._base_url = api_base_url
        if request_timeout:
            self._request_timeout = request_timeout

    def _request(self, url):
        try:
            response = requests.get(url, timeout=self._request_timeout)
            response.raise_for_status()
            return json.loads(response.content.decode('utf-8'))
        except Exception as e:
            raise e

    def _api_url_params(self, api_url, params):
        if params:
            api_url += '?'
            for key, value in params.items():
                api_url += "{0}={1}&".format(key, value)
            api_url = api_url[:-1]

        return api_url

    # ---------- PING ----------
    def ping(self):
        """Check API server status"""

        api_url = '{0}ping'.format(self._base_url)

        return self._request(api_url)

    # ---------- COINS ----------
    def get_coins(self, **kwargs):
        """List all coins with data (name, price, market, developer, community, etc)"""

        api_url = '{0}coins'.format(self._base_url)
        #['order', 'per_page', 'page', 'localization']
        api_url = self._api_url_params(api_url, kwargs)

        return self._request(api_url)

    def get_coins_list(self):
        """List all supported coins id, name and symbol (no pagination required)"""

        api_url = '{0}coins/list'.format(self._base_url)

        return self._request(api_url)

    def get_coins_markets(self, vs_currency, **kwargs):
        """List all supported coins price, market cap, volume, and market related data (no pagination required)"""

        kwargs['vs_currency'] = vs_currency

        api_url = '{0}coins/markets'.format(self._base_url)
        api_url = self._api_url_params(api_url, kwargs)

        return self._request(api_url)

    def get_coin_by_id(self, id, **kwargs):
        """Get current data (name, price, market, ... including exchange tickers) for a coin"""

        api_url = '{0}coins/{1}/'.format(self._base_url, id)
        api_url = self._api_url_params(api_url, kwargs)

        return self._request(api_url)

    def get_coin_history_by_id(self, id, date, **kwargs):
        """Get historical data (name, price, market, stats) at a given date for a coin"""

        kwargs['date'] = date

        api_url = '{0}coins/{1}/history'.format(self._base_url, id)
        api_url = self._api_url_params(api_url, kwargs)

        return self._request(api_url)

    def get_coin_market_chart_by_id(self, id, vs_currency, days):
        """Get historical market data include price, market cap, and 24h volume (granularity auto)"""

        api_url = '{0}coins/{1}/market_chart?vs_currency={2}&days={3}'.format(self._base_url, id, vs_currency, days)

        return self._request(api_url)

    # ---------- EXCHANGES ----------
    def get_exchanges_list(self):
        """List all exchanges"""

        api_url = '{0}exchanges'.format(self._base_url)

        return self._request(api_url)

    def get_exchanges_by_id(self, id):
        """Get exchange volume in BTC and tickers"""

        api_url = '{0}exchanges/{1}'.format(self._base_url, id)

        return self._request(api_url)

    # ---------- EXCHANGE-RATES ----------
    def get_exchange_rates(self):
        """Get BTC-to-Currency exchange rates"""

        api_url = '{0}exchange_rates'.format(self._base_url)

        return self._request(api_url)

    # ---------- GLOBAL ----------
    def get_global(self):
        """Get cryptocurrency global data"""

        api_url = '{0}global'.format(self._base_url)

        return self._request(api_url)['data']
