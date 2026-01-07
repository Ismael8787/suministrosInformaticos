from flask import Flask, render_template, request, redirect, url_for
import db
#from models import login

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("login.html")


if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)