from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
import MySQLdb
import requests 
import re
from parsel import Selector

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'login'

db = MySQL(app)

@app.route('/')

@app.route('/dash/<value>',methods=['GET', 'POST'])
def add(value=None):
    if request.method == "POST":
        url_val = request.form['url']
        ex_price = request.form['exprice'] #expected price
        ex_price = ex_price
        URL = url_val
        headers = {
        "User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36' }
        page = requests.get(URL, headers = headers).text
        selector = Selector(text=page)
        p = selector.xpath("//span[starts-with(@id,'priceblock')]/text()").get()
        title = selector.xpath("//span[starts-with(@id,'productTitle')]/text()").get()
        p = re.sub('₹','',p)
        p = re.sub(',','',p)
        price_new = p[:-3]
        title_new = title.strip() # value of title
        user_val = value
        
        cursor_test = db.connection.cursor(MySQLdb.cursors.DictCursor)
        test = f"SELECT user FROM login.server WHERE URL ='{URL}'"
        cursor_test.execute(test)
        info = cursor_test.fetchall()

        if len(info)>0:
            
            return render_template("dashboardflask.html", error='Url already subscribed')
        else:

            #connecting database and adding values
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            query = f"UPDATE login.server SET URL ='{URL}',title='{title_new}' ,price='{price_new}',expected_price='{ex_price}' WHERE user='{user_val}'"
            
            cursor.execute(query)
            db.connection.commit()
            return render_template("dashboardflask.html", error='Submission Succesful')

        #id="priceblock_ourprice" 

    return render_template("dashboardflask.html") 


@app.route('/login',methods=['GET', 'POST'])
def login():    
    if request.method == "POST":
        user_log = request.form['userlog']
        pass_log = request.form['passlog']

        
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM login.server WHERE  user=%s AND password=%s ",(user_log, pass_log))
        info = cursor.fetchone()
       
        if info['user'] == user_log and info['password'] == pass_log:
            val = user_log
            return redirect(url_for('add',value=val))
        else:
            return 'Please register'
    return render_template('loginflask.html',error=None)


@app.route('/message')
def message():
    return render_template("message.html")

@app.route('/signupflask', methods=["GET","POST"])
def signup():
    if request.method == "POST":
        user_val = request.form['username']
        print(type(user_val))
        pass_val = request.form['password']
        email_val = request.form['email']
        cursor1 = db.connection.cursor(MySQLdb.cursors.DictCursor)
        quer = f"SELECT * FROM login.server WHERE user ='{user_val}'"
        cursor1.execute(quer)
        info = cursor1.fetchall()

        
        if len(info)>0:
            return render_template("signupflask.html", error='Username Already Taken')
        else:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO login.server(user,password,email) VALUES(%s,%s,%s)", (user_val, pass_val,email_val))
            db.connection.commit()
            return render_template("signupflask.html", error='Registration succesful')

        
    return render_template("signupflask.html", error=None)

   
    





if __name__ == '__main__':
    app.run(debug=True)




