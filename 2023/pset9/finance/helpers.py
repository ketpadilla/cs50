import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid

from flask import redirect, render_template, session
from functools import wraps


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

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Code for the lookup function below has been revised by ChatGPT to fix the return name issue
# Code for the lookup function
def lookup(symbol):
    """Look up quote for symbol."""

    # Prepare API request
    symbol = symbol.upper()
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # Yahoo Finance API
    url = (
        f"https://query1.finance.yahoo.com/v7/finance/download/{urllib.parse.quote_plus(symbol)}"
        f"?period1={int(start.timestamp())}"
        f"&period2={int(end.timestamp())}"
        f"&interval=1d&events=history&includeAdjustedClose=true"
    )

    # Query API
    try:
        response = requests.get(url, cookies={"session": str(uuid.uuid4())}, headers={
            "User-Agent": "python-requests", "Accept": "*/*"})
        response.raise_for_status()

        if response.status_code != 200:
            return apology(f"API Error: {response.status_code}", code=response.status_code)

        # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
        quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
        quotes.reverse()

        if len(quotes) == 0:
            return apology("No stock data found for symbol", code=404)

        price = round(float(quotes[0]["Adj Close"]), 2)

        # Alpha Vantage API for company overview
        alpha_vantage_api_key = "YOUR_ALPHA_VANTAGE_API_KEY"
        overview_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={urllib.parse.quote_plus(symbol)}&apikey={alpha_vantage_api_key}"
        overview_response = requests.get(overview_url)
        overview_response.raise_for_status()

        if overview_response.status_code != 200:
            return apology(f"API Error: {overview_response.status_code}", code=overview_response.status_code)

        try:
            overview_data = overview_response.json()
        except ValueError as e:
            print(f"JSON Parsing Error: {e}")
            return None

        name = overview_data.get("Name")
        if name is None:
            name = symbol  # Use the symbol as an alternative

        return {
            "name": name,
            "price": price,
            "symbol": symbol
        }

    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        return None
    except ValueError as e:
        print(f"Value Error: {e}")
        return None
    except KeyError as e:
        print(f"Key Error: {e}")
        return None
    except IndexError as e:
        print(f"Index Error: {e}")
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"