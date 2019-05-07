import datetime


class Node:
    def __init__(self, v=None):
        self.v = v
        self.n = None


class CardTracker:
    col_names = [
        "Txn amount over month",
        "Average over 3 months",
        "Average daily over month",
        "Amount same day",
        "Number same day",
        "Amount currency type over month",
        "Number currency type over month",
        "Amount country type over month",
        "Number country type over month",
    ]

    def __init__(self, id) -> None:
        self.id = id

        self._last_30_days: Node = None
        self._last_90_days: Node = None
        self._last_day: Node = None
        self._last: Node = None

        # 1 day
        self._amount_1 = 0
        self._count_1 = 0

        # 30 days
        self._amount_30 = 0
        self._count_30 = 0
        self._currency_amount_30 = {}
        self._currency_count_30 = {}
        self._country_amount_30 = {}
        self._country_count_30 = {}

        # 90 days
        self._amount_90 = 0
        self._count_90 = 0

    def feed(self, entry):
        current_ts = entry['creationdate']
        self._move_queue(current_ts)

        ret = [
            # Txn amount over month
            self._amount_30 / self._count_30 if self._count_30 != 0 else 0,

            # Average over 3 months
            self._amount_90 / 12,

            # Average daily over month
            self._amount_30 / 30,

            # Amount same day
            self._amount_1,

            # Number same day
            self._count_1,

            # Amount currency type over month
            self._currency_amount_30.get(entry['currencycode'], 0),

            # Number currency type over month
            self._currency_count_30.get(entry['currencycode'], 0),

            # Amount country type over month
            self._country_amount_30.get(entry['shoppercountrycode'], 0),

            # Number country type over month
            self._country_count_30.get(entry['shoppercountrycode'], 0),
        ]

        # add it
        if self._last is None:
            self._last = self._last_day = self._last_30_days = self._last_90_days = Node(entry)
        else:
            self._last.n = Node(entry)
            self._last = self._last.n

            if self._last_day is None:
                self._last_day = self._last

            if self._last_30_days is None:
                self._last_30_days = self._last

            if self._last_90_days is None:
                self._last_90_days = self._last

        amount = entry['amount']

        # 1
        self._amount_1 += amount
        self._count_1 += 1

        # 30
        self._amount_30 += amount
        self._count_30 += 1

        self._currency_amount_30[entry['currencycode']] = self._currency_amount_30.get(entry['currencycode'],
                                                                                       0) + amount
        self._currency_count_30[entry['currencycode']] = self._currency_count_30.get(entry['currencycode'], 0) + 1

        self._country_amount_30[entry['shoppercountrycode']] = self._country_amount_30.get(entry['shoppercountrycode'],
                                                                                           0) + amount
        self._country_count_30[entry['shoppercountrycode']] = self._country_count_30.get(entry['shoppercountrycode'],
                                                                                         0) + 1
        # 90
        self._amount_90 += amount
        self._count_90 += 1

        return ret

    def _move_queue(self, current_ts):

        # 1
        new_date = current_ts - datetime.timedelta(days=1)
        while self._last_day is not None and self._last_day.v['creationdate'] < new_date:
            self._amount_1 -= self._last_day.v['amount']
            self._count_1 -= 1

            self._last_day = self._last_day.n

        # 30
        new_date = current_ts - datetime.timedelta(days=30)
        while self._last_30_days is not None and self._last_30_days.v['creationdate'] < new_date:
            amount = self._last_30_days.v['amount']

            self._amount_30 -= amount
            self._count_30 -= 1

            self._currency_amount_30[self._last_30_days.v['currencycode']] = self._currency_amount_30.get(
                self._last_30_days.v['currencycode'], 0) - amount
            self._currency_count_30[self._last_30_days.v['currencycode']] = self._currency_count_30.get(
                self._last_30_days.v['currencycode'], 0) - 1

            self._country_amount_30[self._last_30_days.v['shoppercountrycode']] = self._country_amount_30.get(
                self._last_30_days.v['shoppercountrycode'],
                0) - amount
            self._country_count_30[self._last_30_days.v['shoppercountrycode']] = self._country_count_30.get(
                self._last_30_days.v['shoppercountrycode'],
                0) - 1

            self._last_30_days = self._last_30_days.n

        new_date = current_ts - datetime.timedelta(days=90)
        while self._last_90_days is not None and self._last_90_days.v['creationdate'] < new_date:
            # 90
            self._amount_90 -= self._last_90_days.v['amount']
            self._count_90 -= 1

            self._last_90_days = self._last_90_days.n


if __name__ == "__main__":
    tracker = CardTracker("sample")

    print(dict(zip(CardTracker.col_names, tracker.feed({'amount': 10,
                                                        'creationdate': datetime.datetime(2015, 7, 1, 0, 0, 43),
                                                        'currencycode': 'GBP',
                                                        'shoppercountrycode': 'GB',
                                                        'txvariantcode': 'visadebit'}))))
    print(dict(zip(CardTracker.col_names, tracker.feed({'amount': 10,
                                                        'creationdate': datetime.datetime(2015, 7, 1, 0, 0, 43),
                                                        'currencycode': 'GBP',
                                                        'shoppercountrycode': 'GB',
                                                        'txvariantcode': 'visadebit'}))))
    print(dict(zip(CardTracker.col_names, tracker.feed({'amount': 10,
                                                        'creationdate': datetime.datetime(2015, 7, 1, 0, 0, 43),
                                                        'currencycode': 'GBP',
                                                        'shoppercountrycode': 'GB',
                                                        'txvariantcode': 'visadebit'}))))
    print(dict(zip(CardTracker.col_names, tracker.feed({'amount': 10,
                                                        'creationdate': datetime.datetime(2015, 7, 1, 0, 0, 43),
                                                        'currencycode': 'GBP',
                                                        'shoppercountrycode': 'GB',
                                                        'txvariantcode': 'visadebit'}))))

    print(dict(zip(CardTracker.col_names, tracker.feed({'amount': 10,
                                                        'creationdate': datetime.datetime(2015, 7, 1, 0, 0, 43),
                                                        'currencycode': 'MXN',
                                                        'shoppercountrycode': 'GB',
                                                        'txvariantcode': 'visadebit'}))))
    print(dict(zip(CardTracker.col_names, tracker.feed({'amount': 10,
                                                        'creationdate': datetime.datetime(2015, 7, 1, 0, 0, 43),
                                                        'currencycode': 'MXN',
                                                        'shoppercountrycode': 'GB',
                                                        'txvariantcode': 'visadebit'}))))

    print(dict(zip(CardTracker.col_names, tracker.feed({'amount': 10,
                                                        'creationdate': datetime.datetime(2015, 7, 1, 0, 0, 43),
                                                        'currencycode': 'MXN',
                                                        'shoppercountrycode': 'US',
                                                        'txvariantcode': 'visadebit'}))))
    print(dict(zip(CardTracker.col_names, tracker.feed({'amount': 10,
                                                        'creationdate': datetime.datetime(2015, 7, 1, 0, 0, 43),
                                                        'currencycode': 'MXN',
                                                        'shoppercountrycode': 'US',
                                                        'txvariantcode': 'visadebit'}))))

    print(dict(zip(CardTracker.col_names, tracker.feed({'amount': 10,
                                                        'creationdate': datetime.datetime(2015, 7, 4, 0, 0, 43),
                                                        'currencycode': 'MXN',
                                                        'shoppercountrycode': 'US',
                                                        'txvariantcode': 'visadebit'}))))
    print(dict(zip(CardTracker.col_names, tracker.feed({'amount': 10,
                                                        'creationdate': datetime.datetime(2015, 7, 4, 0, 0, 43),
                                                        'currencycode': 'MXN',
                                                        'shoppercountrycode': 'US',
                                                        'txvariantcode': 'visadebit'}))))

    print(dict(zip(CardTracker.col_names, tracker.feed({'amount': 10,
                                                        'creationdate': datetime.datetime(2015, 8, 4, 0, 0, 43),
                                                        'currencycode': 'MXN',
                                                        'shoppercountrycode': 'US',
                                                        'txvariantcode': 'visadebit'}))))

    print(dict(zip(CardTracker.col_names, tracker.feed({'amount': 10,
                                                        'creationdate': datetime.datetime(2015, 8, 4, 0, 0, 43),
                                                        'currencycode': 'MXN',
                                                        'shoppercountrycode': 'US',
                                                        'txvariantcode': 'visadebit'}))))

    print(dict(zip(CardTracker.col_names, tracker.feed({'amount': 10,
                                                        'creationdate': datetime.datetime(2016, 8, 4, 0, 0, 43),
                                                        'currencycode': 'MXN',
                                                        'shoppercountrycode': 'US',
                                                        'txvariantcode': 'visadebit'}))))

    print(dict(zip(CardTracker.col_names, tracker.feed({'amount': 10,
                                                        'creationdate': datetime.datetime(2016, 8, 4, 0, 0, 44),
                                                        'currencycode': 'MXN',
                                                        'shoppercountrycode': 'US',
                                                        'txvariantcode': 'visadebit'}))))
