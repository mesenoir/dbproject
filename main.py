import pymysql
import pymysql
from flask import Flask, render_template, request,redirect,url_for

app = Flask(__name__)

class Database:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = "password"
        db = "dbproject"
        self.con = pymysql.connect(host = host, user = user, password = password, db = db, cursorclass = pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
    def list_products(self):
        self.cur.execute("SELECT * from Year;")
        result = self.cur.fetchall()
        return result

    def list_groups(self, variable):
        self.cur.execute(f"SELECT * from Year where Year = {variable};")
        result = self.cur.fetchall()
        return result

    def list_subjects(self):
        self.cur.execute("SELECT * from Subjects;")
        result = self.cur.fetchall()
        return result

    def get_login(self, name, pas):
        self.cur.execute(f"select * from Students where Student_id='{name}' and Pass='{pas}';")
        result = self.cur.fetchall()
        return result
    def list_student(self):
        q = request.args.get('q')
        if q:
            self.cur.execute(f"select * from Students where Student_id='{q}' or Name='{q}'")
            result = self.cur.fetchall()
            if result:
                pass
            else:
                self.cur.execute(f"select * from Students where Group_id='{q}'  or Year={q}")
                result = self.cur.fetchall()
        else:
            self.cur.execute("select * from Students;")
            result = self.cur.fetchall()
        return result

    def list_grade(self, variable):
        q = request.args.get('q')
        if q:
            self.cur.execute(f"select * from Grades where Teacher_id='{q}' or Subject_name='{q}'")
            result = self.cur.fetchall()
            if result:
                pass
            else:
                self.cur.execute(f"select * from Grades where Grade={q}")
                result = self.cur.fetchall()
        else:
            self.cur.execute(f"select * from Grades where Student_id='{variable}'")
            result = self.cur.fetchall()
        return result

    def list_students(self, variable, variable1):
        self.cur.execute(f"select * from Students where Year = {variable} and Group_id = {variable1}")
        result = self.cur.fetchall()
        return result


@app.route('/')
def auth():
    return render_template("home.html")

@app.route('/preview')
def preview():
    return render_template("preview.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

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
            return redirect(url_for("preview"))
        else:
            return redirect(url_for("login"))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
     return f"<h1>{usr}</h1>"


@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/subject')
def product():
    def db_query():
        db = Database()
        product = db.list_subjects()
        return product
    res = db_query()
    return render_template("product.html" , result = res)

@app.route('/group')
def group():
    def db_query():
        db = Database()
        product = db.list_products()
        return product
    res = db_query()
    return render_template("group.html", result = res)

@app.route('/student')
def student():
    def db_query():
        db = Database()
        product = db.list_student()
        return product
    res = db_query()
    return render_template("student.html", result=res)

@app.route('/library')
def student():
    def db_query():
        db = Database()
        library = db.list_student()
        return library
    res = db_query()
    return render_template("library.html", result=res)

@app.route('/students/<variable>/<variable1>', methods=['GET','POST'])
def students(variable, variable1):
    def db_query():
        db = Database()
        product = db.list_students(variable, variable1)
        return product
    res = db_query()
    return render_template("student.html", result =res)

@app.route('/groups/<variable>', methods=['GET','POST'])
def groups(variable):
    def db_query():
        db = Database()
        product = db.list_groups(variable)
        return product
    res = db_query()
    return render_template("group.html", result =res)

@app.route('/grade/<variable>', methods=['GET','POST'])
def grade(variable):
    def db_query():
        db = Database()
        product = db.list_grade(variable)
        return product
    res = db_query()
    return render_template("grade.html", result =res)

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == '__main__':
   app.run(debug = True)
