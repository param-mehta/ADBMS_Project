import os
import requests
import urllib.parse
import yfinance as yf
import matplotlib.pyplot as plt
from flask import redirect, render_template, request, session
from functools import wraps
import lxml

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    try:
        quote = yf.Ticker(symbol)
        name = quote.info["longName"]
        period = '1d'
        interval = '1d'
        hist = quote.history(period=period, interval=interval)
        data = hist.to_dict()
        data = data['Close']
        price = list(data.values())
        price = price[0]
    except requests.RequestException:
        return None

    try:
        return {
            "name": name,
            "price": price,
            "symbol": symbol
        }

    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def lookup1(symbol):

    quote = yf.Ticker(symbol)
    period = '10d'
    interval = '1d'
    hist = quote.history(period=period, interval=interval)
    data = hist.to_dict()
    data = data['Close']
    price = data.values()
    date = data.keys()
    price = list(price)
    date = list(date)
    return date, price

# def lookup2(symbol):
#     """Look up quote for symbol."""
#
#     # Contact API
#     try:
#         api_key = os.environ.get("API_KEY")
#         response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
#         response.raise_for_status()
#     except requests.RequestException:
#         return None
#
#     # Parse response
#     try:
#         quote = response.json()
#         return {
#             "name": quote["companyName"],
#             "price": float(quote["latestPrice"]),
#             "symbol": quote["symbol"]
#         }
#     except (KeyError, TypeError, ValueError):
#         return None
