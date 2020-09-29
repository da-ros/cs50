import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


# Flags to check if recently bought or sold stock
recent_bought = False
recent_sold = False

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Only accepts get method, query actual_stock table to obtain actual stocks owned by user, the following returns a list of dict objects
    user_rows = db.execute("SELECT symbol, name, shares FROM actual_stock WHERE user_id = :user_id", user_id=session["user_id"])
    # Insert current price of a share in each dict of the list, and the total value of each holding (shares times current price)
    for i in range(len(user_rows)):
        user_rows[i]["price"] = lookup(user_rows[i]["symbol"])["price"]
        user_rows[i]["total"] = user_rows[i]["shares"] * user_rows[i]["price"]
    # Obtain actual user cash
    actual_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]
    # Calculate balance
    balance = actual_cash
    for row in user_rows:
        balance += row["total"]
    # Format to usd before pass to template
    actual_cash = usd(actual_cash)
    balance = usd(balance)

    # Pass the variables to render in template
    return render_template("index.html", user_rows=user_rows, actual_cash=actual_cash, balance=balance)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol is submitted in buy.html or form comes from index.html
        if not request.form.get("symbol") and not request.form.get("stock_symbol"):
            return apology("MISSING SYMBOL")
        # Ensure shares is submitted in buy.html or index.html
        if not request.form.get("shares") and not request.form.get("tobuy"):
            return apology("MISSING SHARES")

        # Pull user_id from session global_dict
        actual_user_id = session["user_id"]

        # Pull symbol and shares from form.get dict, first check if form comes from buy.html; if not pull the data from index.html form; if yes pull the data from buy.html form
        if request.form.get("symbol") == None:
            actual_symbol = request.form.get("stock_symbol")
            actual_shares = int(request.form.get("tobuy"))
        else:
            actual_symbol = request.form.get("symbol")
            actual_shares = int(request.form.get("shares"))

        # Check if symbol actually exists
        symbol_info_dict = lookup(actual_symbol)
        if symbol_info_dict == None:
            return apology("INVALID SYMBOL")
        # Override actual_symbol with symbol pulled out from symbol_info_dict (result of lookup) in case that user inputted lowercase in form
        actual_symbol = symbol_info_dict["symbol"]

        # Calculate price of intended purchase
        shares_price = actual_shares * symbol_info_dict["price"]
        # Obtain actual user's cash, the following returns a list of dict objects
        user_row = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=actual_user_id)
        actual_user_cash = user_row[0]["cash"]
        # Check if user can afford purchase; if not, raise an apology
        if (actual_user_cash < shares_price):
            return apology("CAN'T AFFORD")

        # At this point, user can purchase the stock, so lets insert transaction into transactions table in finance.db to keep track of history of purchases
        db.execute("INSERT INTO transactions(user_id, symbol, name, shares, price) VALUES(:user_id, :symbol, :name, :shares, :price)", user_id=actual_user_id, symbol=actual_symbol, name=symbol_info_dict["name"], shares=actual_shares, price=symbol_info_dict["price"])
        # Update user's cash in users table in finance.db
        db.execute("UPDATE users SET cash = :new_cash WHERE id = :user_id", new_cash = actual_user_cash - shares_price, user_id=actual_user_id)

        # Insert purchase into actual_stock table, if already exists that symbol, just add number of shares purchased
        actual_stock_row = db.execute("SELECT * FROM actual_stock WHERE user_id = :user_id AND symbol = :symbol", user_id=actual_user_id, symbol=actual_symbol)
            # If there is no record for that symbol and user_id, insert record of purchase
        if actual_stock_row == []:
            db.execute("INSERT INTO actual_stock(user_id, symbol, name, shares) VALUES(:user_id, :symbol, :name, :shares)", user_id=actual_user_id, symbol=actual_symbol, name=symbol_info_dict["name"], shares=actual_shares)
            # If there is already a record for that symbol and user_id, update adding number of purchased shares
        else:
            current_shares = actual_stock_row[0]["shares"]
            db.execute("UPDATE actual_stock SET shares = :new_shares WHERE user_id = :user_id AND symbol = :symbol", new_shares = current_shares + actual_shares, user_id=actual_user_id, symbol=actual_symbol)

        # Flash message to appear in top of table on index page
        flash("Bought!")
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Accepts only GET method, query database to obtain history of purchases or sales, the following returns a list of dict objects
    user_row = db.execute("SELECT symbol, shares, price, transacted FROM transactions WHERE user_id = :user_id ORDER BY transacted", user_id=session["user_id"])
    # Pass user_row to render_template in order to render apropiately the info there
    return render_template("history.html", user_row=user_row)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
        # Ensure symbol is submitted
        if not request.form.get("symbol"):
            return apology("MISSING SYMBOL")
        # Look up submitted symbol
        symbol_info_dict = lookup(request.form.get("symbol"))
        # Check if symbol not valid
        if symbol_info_dict == None:
            return apology("INVALID SYMBOL")
        # Show results of quotation
        return render_template("quoted.html", name=symbol_info_dict["name"], price=usd(symbol_info_dict["price"]), symbol=symbol_info_dict["symbol"])

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user ID
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == 'POST':
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 403)

        # Check if passwords match
        if (request.form.get("password") != request.form.get("confirmation")):
            return apology("both passwors must match", 403)
        # Check if username alreaady exists
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        if len(rows) != 0:
            return apology("username already exists, please choose another", 403)

        # Create new account, i.e. insert new user and hashed password into database
        hashed_pass = generate_password_hash(request.form.get("password"))
            # When we pass an 'INSERT' value to 'execute' it returns the primary key value of the new generated record
        new_id = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashed)", username=request.form.get("username"), hashed=hashed_pass)
        if not new_id:
            return apology("something went wrong", 403)
            # Create new session variable for new user
        session["user_id"] = new_id
            # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure a stock's symbol is selected from dropdown menu in sell.html or form comes from index.html
        if not request.form.get("symbol") and not request.form.get("stock_symbol"):
            return apology("MISSING SYMBOL")
        # Ensure shares is submitted on sell.html or index.html
        if not request.form.get("shares") and not request.form.get("tosell"):
            return apology("MISSING SHARES")

        # Pull user_id from session global_dict
        actual_user_id = session["user_id"]

        # Pull symbol and shares from form.get dict, first check if form comes from sell.html; if not pull the data from index.html form; if yes pull the data from sell.html form
        if request.form.get("symbol") == None:
            actual_symbol = request.form.get("stock_symbol")
            actual_shares = int(request.form.get("tosell"))
        else:
            actual_symbol = request.form.get("symbol")
            actual_shares = int(request.form.get("shares"))

        # Ensure user owns that number of shares, the following returns a list of 1 dict
        actual_stock_row = db.execute("SELECT shares FROM actual_stock WHERE user_id = :user_id AND symbol = :symbol", user_id=actual_user_id, symbol=actual_symbol)
            # If actual_shares (shares intended to sell) > real shares user owns, render an apology
        if actual_shares > actual_stock_row[0]["shares"]:
            return apology("TOO MANY SHARES")

        # At this point user can sell actual_shares (shares intended to sell), so update 3 tables in database
            # Query API to obtain name and actual price of stock intended to sell, and pull out that data
        symbol_info_dict = lookup(actual_symbol)
        actual_price = symbol_info_dict["price"]
        actual_name = symbol_info_dict["name"]

        # Update transactions table
        db.execute("INSERT INTO transactions(user_id, symbol, name, shares, price) VALUES(:user_id, :symbol, :name, :shares, :price)", user_id=actual_user_id, symbol=actual_symbol, name=actual_name, shares=-(actual_shares), price=actual_price)

        # Update users table cash field with new cash obtained from sale
        sale_cash = actual_price * actual_shares
            # Obtain actual user's cash, the following returns a list of 1 dict object
        user_row = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=actual_user_id)
        actual_user_cash = user_row[0]["cash"]
            # Update user cash in users table
        db.execute("UPDATE users SET cash = :new_cash WHERE id = :user_id", new_cash = actual_user_cash + sale_cash, user_id=actual_user_id)

        # Update actual_stock table, if shares happen to be 0 after the transaction, delete record from actual_stock
        if actual_stock_row[0]["shares"] - actual_shares == 0:
            db.execute("DELETE FROM actual_stock WHERE user_id = :user_id AND symbol = :symbol", user_id=actual_user_id, symbol=actual_symbol)
        else:
            # If user still has >=1 shares of a stock after transaction, update actual_stock table with new value of shares of a stock
            db.execute("UPDATE actual_stock SET shares = :new_shares WHERE user_id = :user_id AND symbol = :symbol", new_shares = actual_stock_row[0]["shares"] - actual_shares, user_id=actual_user_id, symbol=actual_symbol)

        # Flash message to appear in top of table on index page
        flash("Sold!")
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Obtain iterable of actual stocks' symbol for options in <select> hmtl_tag (sell.html) from actual_stock table
        stocks_dicts_in_list = db.execute("SELECT symbol FROM actual_stock WHERE user_id = :user_id", user_id=session["user_id"])
        # Pull stocks' symbol from list of dictionaries to pass to template just a list of symbols
        stocks_list = [dicts["symbol"] for dicts in stocks_dicts_in_list]
        # <select> html tag will show only symbols of stock if user owns at leats 1 share of that stock
        return render_template("sell.html", stocks_list=stocks_list)


@app.route("/change_pass", methods=["GET", "POST"])
@login_required
def change_pass():
    """Change Password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure a new password is submitted
        if not request.form.get("password"):
            return apology("Missing New Password")
        # Ensure confirmation password is submitted
        if not request.form.get("confirmation"):
            return apology("Missing Confirmation Password")

        # Check if passwords match
        if (request.form.get("password") != request.form.get("confirmation")):
            return apology("both passwors must match", 403)

        # At this point both passwords are submitted, valid(managed by html tag), and match, so update database
            # First hash password before update database
        hashed_pass = generate_password_hash(request.form.get("password"))
        db.execute("UPDATE users SET hash = :new_hash WHERE id = :user_id", new_hash = hashed_pass, user_id = session["user_id"])

        # Flash message to appear in top of table on index page
        flash("Password Changed!")
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change_pass.html")


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add cash to current user's cash"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure cash is submitted
        if not request.form.get("cash"):
            return apology("MISSING CASH")

        # Update database, first obtain previous cash, the following returs a list of 1 dict
        actual_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])[0]["cash"]
        db.execute("UPDATE users SET cash = :new_cash WHERE id = :user_id", new_cash = int(request.form.get("cash")) + actual_cash, user_id=session["user_id"])

        # Flash message to appear in top of table on index page
        flash("Cash Added!")
        # Redirect ro user home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("addcash.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
