import pymysql
import pymysql
from flask import Flask, render_template, request,redirect,url_for

app = Flask(__name__)

class Database:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = "password"
        db = "test"
        self.con = pymysql.connect(host = host, user = user, password = password, db = db, cursorclass = pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
    def list_products(self):
        self.cur.execute("SELECT name, product_image from products;")
        result = self.cur.fetchall()
        return result

    def get_login(self, name, pas):
        self.cur.execute(f"select * from Techers where Name='{name}' and Password='{pas}';")
        result = self.cur.fetchall()
        return result


@app.route('/')
def auth():
    return render_template("home.html")

@app.route('/login',methods = ['POST', 'GET'])
def login():
    def db_query(name,pas):
        db = Database()
        auth = db.get_login(name,pas)
        return auth
    if request.method == "POST":
        user = request.form["nm"]
        password = request.form["password"]
        res = db_query(user,password)
        if res:
            return redirect(url_for("product"))
        else:
            return "<h1>WRONG</h1>"
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
     return f"<h1>{usr}</h1>"


@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/product')
def product():
    def db_query():
        db = Database()
        product = db.list_products()
        return product
    res = db_query()
    return render_template("product.html" , result = res)

if __name__ == '__main__':
   app.run(debug = True)
