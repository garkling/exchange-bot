import requests
import io
import re
from datetime import datetime, timedelta
from typing import NamedTuple, Dict, List, Tuple
import matplotlib.pyplot as plt

import db
import config
import exceptions


class Converted(NamedTuple):
    from_: str
    to: str
    sym: str
    value: float
    prefix: bool


class Exchanger:

    def __init__(self):
        self.last_request_time = None
        self.base_codes = {'kr': 'DKK', '$': 'USD'}
        self.currency_list = db.fetchall(['*'])
        self.symbols = []
        self.codenames = []
        self.rates = []
        self._define_fields()

    def _define_fields(self) -> None:
        """Fill symbols, codenames, rates fields"""
        for name, rate, sym in self.currency_list:
            self.symbols.append(sym)
            self.codenames.append(name)
            self.rates.append(rate)

    def get_history_chart_image(self, groups: re.Match) -> io.BytesIO:
        base, target, days = groups[0], groups[1], int(groups[-1])
        days = 31 if days > 31 else days  # days limit
        if base not in self.codenames or target not in self.codenames:
            raise exceptions.InvalidInputError()

        end_at = datetime.now().date()
        start_at = end_at - timedelta(days=days)
        history = self.get_history_from_url(start_at=start_at, end_at=end_at,
                                            base=base, symbols=target)
        return self.make_and_save_chart(history, base, target, days)

    def convert(self, groups: re.Match) -> Converted:
        from_, value, to = groups[0] or groups[2] or groups[3], float(groups[1]), groups[-1]

        if from_ not in self.codenames:
            if from_ not in self.symbols:
                raise exceptions.InvalidInputError()

        # get currency symbol via the index of the currency codename in other list
        symbol = self.symbols[self.codenames.index(to)]

        # check if from_ var is codename if not convert it to appropriate codename
        from_codename = from_ if from_ in self.codenames \
            else self.base_codes.get(from_, self.codenames[self.symbols.index(from_)])

        if from_codename == 'USD' and to != 'USD':
            converted = self.convert_from_usd(value, to)
        else:
            converted = self.convert_to_usd(value, from_codename)

        return Converted(from_codename, to, symbol, converted, (len(symbol) == 1))

    def convert_to_usd(self, value: float, from_: str) -> float:
        rate = self.rates[self.codenames.index(from_)]
        return value / rate

    def convert_from_usd(self, value: float, to: str) -> float:
        rate = self.rates[self.codenames.index(to)]
        return value * rate

    def get_currency_list(self) -> str:
        current_request_time = datetime.now()

        # if there were no requests yet or 10 minutes have passed
        if self.last_request_time is None or \
                (current_request_time - self.last_request_time).seconds > 600:
            data = self.get_latest_currency_info()
            self.update_local_rates(data)
            self.last_request_time = current_request_time
        else:
            data = self.get_currency_from_db()

        return '\n'.join(f'{code} : {round(rate, 2)}' for code, rate in data)

    def update_local_rates(self, data: List[Tuple]) -> None:
        self.rates = [rate for name, rate in data]

    @staticmethod
    def make_and_save_chart(history: Dict, base: str, target: str, days: int) -> io.BytesIO:
        dates = sorted(history)
        rates = [item.get(target) for item in history.values()]
        buffer = io.BytesIO()

        fig = plt.figure()
        plt.title(f'{base} to {target} for {days} days')
        plt.plot(dates, rates)
        fig.autofmt_xdate()  # rotate dates labels in graph
        plt.savefig(buffer, format='png')  # save image in buffer as png
        buffer.seek(0)
        return buffer

    @staticmethod
    def get_history_from_url(**params) -> Dict:
        history_chart = requests.get(config.HISTORY_URL, params=params).json()
        return history_chart.get('rates')

    @staticmethod
    def get_currency_from_db() -> List[Tuple]:
        currency_list = db.fetchall(['codename', 'rate'])
        return currency_list

    @staticmethod
    def get_latest_currency_info() -> List[Tuple]:
        currency_list = requests.get(config.LATEST_RATES_URL).json().get('rates').items()
        db.update(currency_list)
        return currency_list
