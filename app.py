# IMPORTED MODULES
from cs50 import SQL
from flask import Flask, redirect, render_template, request, render_template_string


# CONFIGURE APPLICATION
app = Flask(__name__)


# ERROR HANDLING 
def handle_error(error):
    # Get the status code from the error object (default to 500)
    STATUS_CODE = getattr(error, 'code', 500)
    # Get the description of the status code (default to ISE)
    DESCRIPTION = getattr(error, 'description', 'Internal Server Error')
    return render_template("pages/error.html", statusCode=STATUS_CODE, description=DESCRIPTION)


# HOME PAGE
@app.route("/")
def index():
    return render_template("pages/index.html")


# RUN FLASK APPLICATION
if __name__ == "__main__":
    app.run()