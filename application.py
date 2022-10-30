from flask import *
import sqlite3
app = Flask(__name__)
app.secret_key="123"

class User:
    def __init__(self,id,username,password):
        self.id=id
        self.username=username
        self.password=password

users=[]
users.append(User(id=1,username='manokaran',password='manokaran@123'))
users.append(User(id=2,username='mahesh',password='mahesh@123'))
users.append(User(id=3,username='suraj',password='suraj@123'))   

@app.route("/",methods=['GET','POST'])
def login():
    if request.method=='POST':
        uname=request.form['uname']
        upass = request.form['upass']

        for data in users:
            if data.username==uname and data.password==upass:
                session['userid']=data.id
                g.record=1
                return redirect(url_for('index'))
            else:
                g.record=0
        if g.record!=1:
            flash("Username or Password Mismatch...!!!",'danger')
            return redirect(url_for('login'))
    return render_template("login.html")


@app.before_request
def before_request():
    if 'userid' in session:
        for data in users:
            if data.id==session['userid']:
                g.user=data
@app.route('/user')
def user():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('user.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/home",methods=['GET','POST'])
def index(): 
    return render_template("index.html");

@app.route("/searchrecord",methods = ['GET','POST'])
def searchrecord():
    return render_template("searchdata.html");

@app.route("/search",methods = ["POST"])
def search():
    roll = request.form["roll"]
    with sqlite3.connect("student_detials.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        cursor.execute("select * from Student_Info where roll=?",(roll,))
        rows = cursor.fetchall()
        msg = "Student detial successfully Selected"
        return render_template("sdata.html",rows=rows)

@app.route("/supdate",methods = ['GET','POST'])
def supdate():
    return render_template("supdate.html");

@app.route("/update",methods = ['GET','POST'])
def update():
    roll = request.form["roll"]
    with sqlite3.connect("student_detials.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("select * from Student_Info where roll=?",(roll,))
        rows = cursor.fetchall()
        msg = "Student detial successfully Selected"
        return render_template("update.html",rows=rows)


@app.route("/edit",methods = ['GET','POST'])
def edit():
    
    if request.method == "POST":
        a = request.form["roll"]
        roll = request.form["roll"]
        name = request.form["name"]
        email = request.form["email"]
        gender = request.form["gender"]
        contact = request.form["contact"]
        dob = request.form["dob"]
        address = request.form["address"]
        
        with sqlite3.connect("student_detials.db") as connection: #conecting to the sqlite database with name as connectioon
            cursor = connection.cursor() #For Flask Cursor thus provides a means for Flask to interact with the database tables. It can scan the database for data, execute SQL queries, and delete table records.
            qry="INSERT OR REPLACE INTO Student_Info VALUES(?,?,?,?,?,?,?)"#qery code
            cursor.execute(qry,(roll,name, email, gender, contact, dob, address)) #Execute to add data in database
            connection.commit()# save change in Database
            cursor.close()
        connection = sqlite3.connect("student_detials.db")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("select * from Student_Info")
        rows = cursor.fetchall()
        return render_template("student_info.html",rows = rows)

       
    
        

@app.route("/add_student")
def add_student():
    return render_template("add_student.html")


@app.route("/saverecord",methods = ["POST","GET"])
def saveRecord():
    msg = "msg"
    if request.method == "POST":
        try:
            roll = request.form["roll"]
            name = request.form["name"]
            email = request.form["email"]
            gender = request.form["gender"]
            contact = request.form["contact"]
            dob = request.form["dob"]
            address = request.form["address"]
            with sqlite3.connect("student_detials.db") as connection: #conecting to the sqlite database with name as connectioon
                cursor = connection.cursor() #For Flask Cursor thus provides a means for Flask to interact with the database tables. It can scan the database for data, execute SQL queries, and delete table records.
                qry="INSERT into Student_Info (roll,name, email, gender, contact, dob, address) values (?,?,?,?,?,?,?)"#qery code
                cursor.execute(qry,(roll,name, email, gender, contact, dob, address)) #Execute to add data in database
                connection.commit()# save change in Database
                msg = "Student detials successfully Added"
        except:
            connection.rollback()
            msg = "We can not add Student detials to the database"
        finally:
            return render_template("success_record.html",msg = msg)
            connection.close()



@app.route("/delete_student")
def delete_student():
    return render_template("delete_student.html")



@app.route("/student_info")
def student_info():
    connection = sqlite3.connect("student_detials.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("select * from Student_Info")
    rows = cursor.fetchall()
    return render_template("student_info.html",rows = rows)



@app.route("/deleterecord",methods = ["POST"])
def deleterecord():
    roll = request.form["roll"]
    with sqlite3.connect("student_detials.db") as connection:

        cursor = connection.cursor()
        cursor.execute("select * from Student_Info where roll=?", (roll,))
        rows = cursor.fetchall()
        if not rows == []:

            cursor.execute("delete from Student_Info where roll = ?",(roll,))
            msg = "Student detial successfully deleted"
            return render_template("delete_record.html", msg=msg)

        else:
            msg = "can't be deleted"
            return render_template("delete_record.html", msg=msg)





        
        
if __name__ == "__main__":
    app.run(debug = True)  
