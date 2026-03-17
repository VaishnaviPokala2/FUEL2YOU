from flask import Flask,render_template,request,redirect,session
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key="fuel2you"

def db():
    return sqlite3.connect("database.db")

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/register',methods=['POST'])
def register():

    name=request.form['name']
    email=request.form['email']
    password=request.form['password']

    conn=db()
    cur=conn.cursor()

    cur.execute("INSERT INTO users VALUES(NULL,?,?,?,'user')",(name,email,password))
    conn.commit()

    return redirect('/')

@app.route('/login',methods=['POST'])
def login():

    email=request.form['email']
    password=request.form['password']

    conn=db()
    cur=conn.cursor()

    cur.execute("SELECT * FROM users WHERE email=? AND password=?",(email,password))
    user=cur.fetchone()

    if user:

        session['user']=user[1]
        role=user[4]

        if role=="user":
            return redirect('/user')

        if role=="agent":
            return redirect('/agent')

        if role=="admin":
            return redirect('/admin')

    return "Invalid Login"

@app.route('/user')
def user():

    conn=db()
    cur=conn.cursor()

    cur.execute("SELECT * FROM fuel_price")
    price=cur.fetchall()

    return render_template("dashboard_user.html",price=price)

@app.route('/order',methods=['POST'])
def order():

    fuel=request.form['fuel']
    qty=float(request.form['qty'])
    address=request.form['address']
    payment=request.form['payment']

    conn=db()
    cur=conn.cursor()

    cur.execute("SELECT price FROM fuel_price WHERE fuel=?",(fuel,))
    price=cur.fetchone()[0]

    total=price*qty

    cur.execute("INSERT INTO orders VALUES(NULL,?,?,?,?,?,?,?)",
                (session['user'],fuel,qty,total,address,payment,"Pending"))

    conn.commit()

    return render_template("receipt.html",
                           fuel=fuel,
                           qty=qty,
                           total=total,
                           payment=payment,
                           date=datetime.datetime.now())

@app.route('/agent')
def agent():

    conn=db()
    cur=conn.cursor()

    cur.execute("SELECT * FROM orders")
    orders=cur.fetchall()

    return render_template("agent_dashboard.html",orders=orders)

@app.route('/accept/<id>')
def accept(id):

    conn=db()
    cur=conn.cursor()

    cur.execute("UPDATE orders SET status='Accepted' WHERE id=?",(id,))
    conn.commit()

    return redirect('/agent')

@app.route('/deliver/<id>')
def deliver(id):

    conn=db()
    cur=conn.cursor()

    cur.execute("UPDATE orders SET status='Delivered' WHERE id=?",(id,))
    conn.commit()

    return redirect('/agent')

@app.route('/admin')
def admin():

    conn=db()
    cur=conn.cursor()

    cur.execute("SELECT * FROM fuel_price")
    price=cur.fetchall()

    cur.execute("SELECT * FROM orders")
    orders=cur.fetchall()

    return render_template("admin_dashboard.html",price=price,orders=orders)

@app.route('/update_price',methods=['POST'])
def update_price():

    fuel=request.form['fuel']
    price=request.form['price']

    conn=db()
    cur=conn.cursor()

    cur.execute("UPDATE fuel_price SET price=? WHERE fuel=?",(price,fuel))
    conn.commit()

    return redirect('/admin')

if __name__=="__main__":
    app.run(debug=True)