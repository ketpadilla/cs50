import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from datetime import datetime, timezone

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get portfolio
    USER_ID = session["user_id"]
    PORTFOLIO = []
    DATA = db.execute("SELECT symbol, shares FROM shares WHERE user_id = ?", USER_ID)
    TOTAL = 0

    for index in DATA:
        SYMBOL, SHARES = index["symbol"], index["shares"]
        stock = lookup(SYMBOL)

        if stock is None:
            continue

        NAME, PRICE = stock["name"], stock["price"]
        STOCK_VALUE = SHARES * PRICE
        TOTAL += STOCK_VALUE

        PORTFOLIO.append((SYMBOL, SHARES, NAME, usd(PRICE), usd(STOCK_VALUE)))

    CASH = db.execute("SELECT cash FROM users WHERE id = ?", USER_ID)[0]['cash']
    TOTAL += CASH

    return render_template("index.html", portfolio=PORTFOLIO, cash=usd(CASH), total=usd(TOTAL))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol is not blank and exists
        SYMBOL = request.form.get("symbol")
        STOCK = lookup(SYMBOL)
        if not STOCK:
            return apology("symbol is blank or does not exist", 400)

        # Ensure number of shares is a positive integer
        SHARES = request.form.get("shares")
        if not SHARES.isnumeric() or float(SHARES) < 1:
            return apology("Number of shares must be a positive integer", 400)
        SHARES = int(SHARES)

        # Get price of stock and user's cash amount
        PRICE = STOCK["price"]
        USER_ID = session["user_id"]
        USER_CASH = db.execute("SELECT cash FROM users WHERE id = ?", USER_ID)[0]['cash']

        # Ensure user can afford purchase
        REMAINING = USER_CASH - (PRICE * SHARES)
        if REMAINING < 0:
            return apology("not enough cash. purchase failed", 400)

        # Check if user has current shares on stock
        DATA = db.execute("SELECT shares FROM shares WHERE user_id = ? AND symbol = ?", USER_ID, SYMBOL)
        if not DATA:
            USER_SHARES = 0
        else:
            USER_SHARES = DATA[0]["shares"]

        # Procceed with purchase
        NOW_TIMESTAMP = datetime.now(timezone.utc)
        TIMESTAMP = str(NOW_TIMESTAMP.date()) + " " + NOW_TIMESTAMP.time().strftime("%H:%M:%S")

        db.execute("UPDATE users SET cash = ? WHERE id = ?", REMAINING, USER_ID)
        db.execute("INSERT INTO purchases (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", USER_ID, SYMBOL, SHARES, PRICE)

        # Get current number of shares

        if USER_SHARES == 0:
            db.execute("INSERT INTO shares (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
                       USER_ID, SYMBOL, SHARES, PRICE, TIMESTAMP)
        else:
            NEW_USER_SHARES = USER_SHARES + SHARES
            db.execute("UPDATE shares SET shares = ?, timestamp = ?, price = ? WHERE user_id = ? AND symbol = ?",
                       NEW_USER_SHARES, TIMESTAMP, PRICE, USER_ID, SYMBOL)

        # Return to homepage
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get user ID
    USER_ID = session["user_id"]

    # Get transactions ordered by timestamp
    TRANSACTIONS = db.execute(
        "SELECT symbol, shares, price, timestamp, type FROM "
        "(SELECT symbol, shares, price, timestamp, 'Bought' AS type FROM purchases WHERE user_id = ? "
        "UNION ALL "
        "SELECT symbol, shares, price, timestamp, 'Sold' AS type FROM sales WHERE user_id = ?) "
        "ORDER BY timestamp",
        USER_ID, USER_ID
    )

    # Prepare transaction history
    HISTORY = []
    for index in TRANSACTIONS:
        SYMBOL, SHARES, PRICE, TIMESTAMP, TRANSACTION_TYPE = (
            index["symbol"],
            index["shares"],
            index["price"],
            index["timestamp"],
            index["type"]
        )

        HISTORY.append((SYMBOL, SHARES, usd(PRICE), TRANSACTION_TYPE.capitalize(), TIMESTAMP))

    return render_template("history.html", history=HISTORY)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        SYMBOL = request.form.get("symbol")
        STOCK = lookup(SYMBOL)

        if not STOCK:
            return render_template("quote.html", invalid=True, symbol=SYMBOL), 400

        return render_template("quoted.html", company=STOCK["name"], price=usd(STOCK["price"]), symbol=STOCK["symbol"])

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        USERNAME = request.form.get("username")
        PASSWORD = request.form.get("password")
        CONFIRMATION = request.form.get("confirmation")

        # Ensure username was submitted
        if not USERNAME:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not PASSWORD:
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not CONFIRMATION:
            return apology("confirm password is blank", 400)

        # Ensure password match
        elif PASSWORD != CONFIRMATION:
            return apology("password mismatch", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", USERNAME)

        # Ensure username does not exists
        if len(rows) == 1:
            return apology("username already exists", 400)

        # Generate password hash
        HASH = generate_password_hash(PASSWORD)

        # Add user to database with the has for their password
        db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=USERNAME, hash=HASH)

        # Redirect user to login page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

   # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol is not blank and exists
        SYMBOL = request.form.get("symbol")
        if not SYMBOL:
            return apology("stock not selected", 400)

        # Ensure user has stock
        USER_ID = session["user_id"]
        USER_SYMBOL = db.execute("SELECT * FROM shares WHERE user_id = ? AND symbol = ?", USER_ID, SYMBOL)
        if not USER_SYMBOL:
            return apology("user does not own any share of that stock", 400)

        # Ensure number of shares is not blank
        SHARES = request.form.get("shares")
        if not SHARES:
            return apology("number of shares missing", 400)

        # Ensure number of shares is a positive integer
        SHARES = int(SHARES)
        if SHARES < 1:
            return apology("number of shares must be a positive integer", 400)

        # Ensure user has enough shares
        USER_SHARES = db.execute("SELECT shares FROM shares WHERE user_id = ? AND symbol = ?", USER_ID, SYMBOL)[0]["shares"]
        if SHARES > USER_SHARES:
            return apology("user does not have enough shares", 400)

        # Get price of stock and user's cash amount
        STOCK = lookup(SYMBOL)
        if STOCK is None or "price" not in STOCK:
            return render_template("sell.html", alert_message="Failed to get stock price. Please try again.")

        PRICE = STOCK["price"]
        USER_CASH = db.execute("SELECT cash FROM users WHERE id = ?", USER_ID)[0]['cash']

        # Procceed with sale
        REMAINING_SHARES = USER_SHARES - SHARES
        NEW_USER_CASH = USER_CASH + (PRICE * SHARES)
        NOW_TIMESTAMP = datetime.now(timezone.utc)
        TIMESTAMP = str(NOW_TIMESTAMP.date()) + " " + NOW_TIMESTAMP.time().strftime("%H:%M:%S")

        db.execute("UPDATE users SET cash = ? WHERE id = ?", NEW_USER_CASH, USER_ID)
        db.execute("INSERT INTO sales (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", USER_ID, SYMBOL, SHARES, PRICE)

        if REMAINING_SHARES == 0:
            db.execute("DELETE FROM shares WHERE user_id = ? AND symbol = ?", USER_ID, SYMBOL)
        else:
            db.execute("UPDATE shares SET shares = ?, timestamp = ? WHERE user_id = ? AND symbol = ?",
                       REMAINING_SHARES, TIMESTAMP, USER_ID, SYMBOL)

        # Return to homepage
        return redirect("/")

    USER_ID = session["user_id"]
    SYMBOL = list()
    DATA = db.execute("SELECT symbol FROM shares WHERE user_id = ?", USER_ID)
    for index in DATA:
        SYMBOL.append(index['symbol'])

    return render_template("sell.html", symbol=SYMBOL)


# Run the Flask application
if __name__ == "__main__":
    app.run()