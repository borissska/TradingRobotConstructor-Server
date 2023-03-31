import pandas as pd
import numpy as np
import datetime
import os
import requests
import io
import zipfile
from classes.stock import Stock


def download_csv_file(*, link, path_csv):
    r = requests.get(link)
    zip_file = zipfile.ZipFile(io.BytesIO(r.content))
    zip_file.extractall(path_csv)


def download_zip_file(*, link, path_zip):
    r = requests.get(link)
    with open(os.path.join(path_zip), "wb") as zip_file:
        zip_file.write(r.content)


def download_zip_files(*, start_date):
    end_date = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
    delay = datetime.timedelta(days=3)
    delta = datetime.timedelta(days=1)

    while start_date <= end_date - delay:
        stock.set_date(year=start_date.year, month_number=start_date.month, day=start_date.day)
        link = f"https://data.binance.vision/data/spot/daily/klines/{stock.get_full_link_string()}.zip"
        path_zip = f"D:\candleData\{stock.get_ticker()}\{stock.get_ticker()}-{stock.get_timeframe()}-{stock.get_datetime()}.zip"
        if os.path.exists(path_zip):
            pass
        else:
            download_zip_file(link=link, path_zip=path_zip)
            add_zip_file_to_final_csv_in_needed_format(path_zip=path_zip, path_final_csv=path_final_csv)
        start_date += delta


def reformat_csv_file(*, all_data):
    needed_data = all_data.loc[0:, ['datetime', 'open', 'high', 'low', 'close', 'volume']]
    for el in range(len(needed_data)):
        needed_data.at[el, "datetime"] = datetime.datetime.utcfromtimestamp(
            int(needed_data.loc[el, "datetime"]) / 1000)
    return needed_data


def add_zip_file_to_final_csv_in_needed_format(*, path_zip, path_final_csv):
    all_data = pd.DataFrame(np.array(pd.read_csv(path_zip, header=None, compression='zip')),
                            columns=['datetime', 'open', 'high', 'low', 'close', 'volume', 'Kline Close time',
                                     'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
                                     'Taker buy quote asset volume', 'Unused field, ignore.'])
    needed_data = reformat_csv_file(all_data=all_data)
    if os.path.exists(path_final_csv):
        data_csv = needed_data.to_csv(index=False, header=False)
    else:
        data_csv = needed_data.to_csv(index=False)
    with open(os.path.join(path_final_csv), "a", newline='') as file_csv:
        file_csv.write(data_csv)


def make_final_csv_file(*, start_date, path_final_csv):
    os.remove(path_final_csv)
    end_date = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
    delay = datetime.timedelta(days=3)
    delta = datetime.timedelta(days=1)

    while start_date <= end_date - delay:
        stock.set_date(year=start_date.year, month_number=start_date.month, day=start_date.day)
        path_zip = f"D:\candleData\{stock.get_ticker()}\{stock.get_ticker()}-{stock.get_timeframe()}-{stock.get_datetime()}.zip"
        add_zip_file_to_final_csv_in_needed_format(path_zip=path_zip, path_final_csv=path_final_csv)
        start_date += delta


if __name__ == '__main__':
    stock = Stock(ticker="BTCUSDT", timeframe="1d")
    path_final_csv = f"D:\candleData\{stock.get_ticker()}\{stock.get_ticker()}-{stock.get_timeframe()}.csv"
    start_date = datetime.date(2021, 3, 1)

    download_zip_files(start_date=start_date)

    # path_csv = f"D:\candleData\{stock.get_ticker()}"
    # download_csv_file(link=link, path_csv=path_csv)
    # download_zip_file(link=link, path_zip=path_csv)
    # add_zip_data_to_final_csv_in_needed_format(path_zip=path_zip, path_final_csv=path_final_csv)
