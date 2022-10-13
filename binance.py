"""This module contains the class BinanceUS, designed to look for arbitrage opportunities on 
the exchange binance.us. It utilizes Binance's REST API and Python's requests library to get 
market data."""

import requests
import json
import apikeys
from typing import List, Dict, Any, Tuple

class BinanceUS:
    """The goal of this class is to identify arbitrage opportunities on BinanceUS."""
    # Static variables
    endpoint = 'https://api.binance.us/api/v3'
    apikey = apikeys.apikey
    secret_key = apikeys.secret_key

    def exchange_info(self):
        return requests.get(self.endpoint + '/exchangeInfo').json()

    def latest_ask(self, symbol: str) -> float:
        """Get the latest ask price for a given trading pair.
        
        Parameters:
            symbol (str): A trading pair on binance.us, e.g. 'LTCBTC'.
        
        Returns:
            float: The latest ask price of the base currency in terms of the quote currency.
        """
        return float(requests.get(self.endpoint + '/depth?symbol=' + symbol + '&limit=1').json()['asks'][0][0])

    def latest_bid(self, symbol: str) -> float:
        """Get the latest bid price for a given trading pair"""
        return float(requests.get(self.endpoint + '/depth?symbol=' + symbol + '&limit=1').json()['bids'][0][0])

    def get_trades(self, symbol: str):
        pass

    def markets_as_dict(self) -> Dict[str, Dict[str, Any]]:
        """Returns a Python dictionary where: 
            key = a trading pair (str)
            value = a dict containing exchange info about the trading pair
        """
        return {symbol['symbol']: symbol for symbol in self.exchange_info()['symbols']}
    
    def trading_pairs(self) -> List[str]:
        """Returns a list of all trading pairs offered on binance.us."""
        return [symbol['symbol'] for symbol in self.exchange_info()['symbols']]
        
    def base_currencies(self) -> List[str]:
        # A duplicates-removed list of base currencies available on binance.us
        markets = self.markets_as_dict()
        base_currencies = set()
        for m in markets:
            base_currencies.add(markets[m]['baseAsset'])
        return sorted(list(base_currencies))
    
    def triangle_triples(self) -> List[Tuple[str]]:
        """A relatively intense method. Expected to run in theta(n * m) time
            where n = number of unique baseAssets and m = number of trading pairs.
        Returns:
            A list of 3-tuples in the form (fiat, intermediate, token)
        """
        triples = []
        markets = self.markets_as_dict()
        for base in self.base_currencies():
            # USD BTC 
            if base + 'USD' in markets and base + 'BTC' in markets:
                triples.append(('USD', 'BTC', base))
            # USDT BTC
            if base + 'USDT' in markets and base + 'BTC' in markets:
                triples.append(('USDT', 'BTC', base))
            # USD USDT
            if base + 'USD' in markets and base + 'USDT' in markets:
                triples.append(('USD', 'USDT', base))
        return triples

    def compute_profit(self, fiat, intermediate, token):
    # Given the symbols of three tokens, compute the resulting profit multiple 
    # The first two arguments are base currencies (e.g. USD and BTC)
    # The third argument is the pivot currency, e.g. YFI
        return self.latest_ask(intermediate + fiat) * self.latest_ask(token + intermediate)\
             * (1 / self.latest_bid(token + fiat))




def main():
    b = BinanceUS()
    print(b.latest_ask('LTCBTC'))
    print(b.latest_bid('LTCBTC'))
    with open('exchangeInfo.txt', 'w') as f:
        f.write(json.dumps(b.exchange_info(), indent=2))
    print(len(b.exchange_info()['symbols']))
    for symbol in b.trading_pairs():
        print(symbol)
    print(len(b.trading_pairs()))
    print(b.base_currencies())
    for t in b.triangle_triples():
        print(t)
    print(len(b.triangle_triples()))
    

if __name__ == "__main__":
    main()
