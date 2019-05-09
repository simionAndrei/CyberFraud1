import datetime
import numpy as np


class Node:
    def __init__(self, v=None):
        self.v = v.copy()
        self.n = None


class CardTracker:
    colnames = [
        "Txn_Amount_Month",
        "Average_3Months",
        "Average_DailyMonth",
        "Amount_SameDay",
        "Number_Same_Day",
        "Amount_Currency_Type_Month",
        "Number_Currency_Type_Month",
        "Amount_Country_Type_Month",
        "Number_Country_Type_Month",
        "Unique emails",
        "Unique ips"
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

        self._emails = set()
        self._ips = set()

    def feed(self, entry):
        current_ts = entry['creationdate']
        self._move_queue(current_ts)

        self._emails.add(entry['mail_id'])
        self._ips.add(entry['ip_id'])

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
            self._currency_amount_30.get(entry['currencycode'], 0) / 30,

            # Number currency type over month
            self._currency_count_30.get(entry['currencycode'], 0),

            # Amount country type over month
            self._country_amount_30.get(entry['shoppercountrycode'], 0) / 30,

            # Number country type over month
            self._country_count_30.get(entry['shoppercountrycode'], 0),

            # Number of unique emails used
            len(self._emails),

            # Number of unique ips used
            len(self._ips),
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
        new_date = current_ts - np.timedelta64(1, 'D')
        while self._last_day is not None and self._last_day.v['creationdate'] < new_date:
            self._amount_1 -= self._last_day.v['amount']
            self._count_1 -= 1

            self._last_day = self._last_day.n

        # 30
        new_date = current_ts - np.timedelta64(30, 'D')
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

        new_date = current_ts - np.timedelta64(90, 'D')
        while self._last_90_days is not None and self._last_90_days.v['creationdate'] < new_date:
            # 90
            self._amount_90 -= self._last_90_days.v['amount']
            self._count_90 -= 1

            self._last_90_days = self._last_90_days.n


'''
def extract_feature(row, _hash):
    key = row['card_id']

    if key in _hash:
        card_tracker = _hash[key]
    else:
        card_tracker = CardTracker(key)
        _hash[key] = card_tracker

    return card_tracker.feed(row)


def extract_features_from_data(df):
    _hash = {}
    features = df.apply(lambda e: extract_feature(e, _hash), axis=1)


    return features
''' 

if __name__ == "__main__":
    print("Library module. No main function")
