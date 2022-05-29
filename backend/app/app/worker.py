import datetime
import time
from datetime import timedelta, date

import investpy
import numpy as np
from celery.schedules import crontab
from raven import Client

from app import crud
from app.core.celery_app import celery_app
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.stock import Side
from app.schemas.signal import SignalCreate
from app.schemas.stock import StockCreate
from app.utils import send_invest_email

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"


@celery_app.task(acks_late=True)
def notification_task():
    db = SessionLocal()
    signal = crud.signal.get_last(db)
    users = crud.user.get_all_notifiable(db)
    db.close()
    send_invest_email(email_to=[user.email for user in users if user.need_notification], data=signal.text)


@celery_app.task(acks_late=True)
def invest_task():
    country = 'russia'
    stocks = investpy.stocks.get_stocks(country=country)["symbol"]
    # stocks = ["FEES", "MAGN", "MSNG", "NMTP", "ROSN", "SBER", "BLNG"]
    count_stocks = len(stocks)
    counter = 0
    index_for_buy = 1
    index_for_sell = 1
    buy_stocks = []
    total_buy_str = "### STOCKS FOR BUYING ###\n"
    sell_stocks = []
    total_sell_str = "### STOCKS FOR SELLING ###\n"
    today = date.today()
    current_date = today.strftime("%d/%m/%Y")
    from_date = (today - timedelta(days=6)).strftime("%d/%m/%Y")
    for index, stock in enumerate(stocks, start=1):
        print(f"{stock} ({index}/{count_stocks})")
        if counter == 10:
            time.sleep(3)
            counter = 0
        try:
            # technical_indicators = investpy.technical.technical_indicators(stock, country, 'stock', interval='daily')
            technical_indicators = investpy.technical.technical_indicators(stock, country, 'stock', interval='1hour')
            # moving_averages = investpy.technical.moving_averages(stock, country, 'stock', interval='daily')
            moving_averages = investpy.technical.moving_averages(stock, country, 'stock', interval='1hour')

            tech_sell = len(technical_indicators[technical_indicators['signal'] == 'sell'])
            tech_buy = len(technical_indicators[technical_indicators['signal'] == 'buy'])

            moving_sma_sell = len(moving_averages[moving_averages['sma_signal'] == 'sell'])
            moving_sma_buy = len(moving_averages[moving_averages['sma_signal'] == 'buy'])

            moving_ema_sell = len(moving_averages[moving_averages['ema_signal'] == 'sell'])
            moving_ema_buy = len(moving_averages[moving_averages['ema_signal'] == 'buy'])
        except:
            continue

        sma_20 = moving_averages['sma_signal'][2]
        sma_100 = moving_averages['sma_signal'][4]
        ema_20 = moving_averages['ema_signal'][2]
        ema_100 = moving_averages['ema_signal'][4]
        if tech_buy > 8 and tech_sell < 3 and moving_sma_buy > 4 and moving_ema_buy > 4:
            df = investpy.get_stock_historical_data(stock=stock, country=country, from_date=from_date,
                                                    to_date=current_date)
            info = investpy.get_stock_company_profile(stock, country)
            info["ticker"] = stock
            info["country"] = country
            info["price"] = df['Close'][-1]
            info["side"] = Side.buy.value
            buy_stocks.append(info)

            buy_str = (
                f"{index_for_buy}) STOCK = {stock}\n"
                f"Link: {info.get('url')}\n"
                f"Tech sell indicators: to buy ={tech_buy} of 12; to sell ={tech_sell} of 12\n"
                f"SMA moving averages: to buy ={moving_sma_buy} of 6; to sell ={moving_sma_sell} of 6\n"
                f"EMA moving averages: to buy ={moving_ema_buy} of 6; to sell ={moving_ema_sell} of 6\n"
                f"SMA_20 ={sma_20}; SMA_100 ={sma_100}; EMA_20 ={ema_20}; EMA_100 ={ema_100}\n"
                f"Prices Last Five days of {stock} = {'; '.join(np.array(df['Close'][-5:]).astype(str))}\n\n"
            )
            print(buy_str)
            total_buy_str += buy_str
            index_for_buy += 1
            counter += 1

        elif tech_sell > 8 and tech_buy < 2 and moving_sma_sell > 4 and moving_ema_sell > 4:
            df = investpy.get_stock_historical_data(stock=stock, country=country, from_date=from_date,
                                                    to_date=current_date)
            info = investpy.get_stock_company_profile(stock, country)
            info["ticker"] = stock
            info["country"] = country
            info["price"] = df['Close'][-1]
            info["side"] = Side.sell.value
            sell_stocks.append(info)

            sell_str = (
                f"{index_for_sell}) STOCK = {stock}\n"
                f"Link: {info.get('url')}\n"
                f"Tech sell indicators: to buy ={tech_buy} of 12; to sell ={tech_sell} of 12\n"
                f"SMA moving averages: to buy ={moving_sma_buy} of 6; to sell ={moving_sma_sell} of 6\n"
                f"EMA moving averages: to buy ={moving_ema_buy} of 6; to sell ={moving_ema_sell} of 6\n"
                f"SMA_20 ={sma_20}; SMA_100 ={sma_100}; EMA_20 ={ema_20}; EMA_100 ={ema_100}\n"
                f"Prices Last Five days of {stock} = {'; '.join(np.array(df['Close'][-5:]).astype(str))}\n\n"
            )
            print(sell_str)
            total_sell_str += sell_str
            index_for_sell += 1
            counter += 1

    print('==================================================')
    text = total_buy_str + "\n" + total_sell_str
    print(text)

    db = SessionLocal()
    signal_scheme = SignalCreate(created_datetime=datetime.datetime.now(), text=text)
    signal = crud.signal.create(db, obj_in=signal_scheme)
    for stock in buy_stocks + sell_stocks:
        scheme = StockCreate(**stock, signal_id=signal.id)
        crud.stock.create(db, obj_in=scheme)

    db.close()


# Configure celery beat
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(15.0, test_celery.s("Test"), name='Do something every 15 seconds')
    sender.add_periodic_task(crontab(hour="1-13", minute=30, day_of_week="1-5"), invest_task.s(),
                             name='Stocks calculation')
    sender.add_periodic_task(crontab(hour="1-13", minute=0, day_of_week="1-5"), notification_task.s(),
                             name='Stocks notification')
