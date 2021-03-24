from flask import Flask, render_template,url_for,flash,get_flashed_messages, redirect,request
import sqlite3

app = Flask(__name__, template_folder="templates")
app.secret_key = "privateDB"

connection = "None"
try:
    connection = sqlite3.connect("Library_Data.db")
    connection.execute("create table LibraryBookData( ID INTEGER PRIMARY KEY, Title TEXT NOT NULL, Author TEXT NOT NULL, Status TEXT NOT NULL)")

except sqlite3.Error as e:
    pass

finally:
    if connection:
        connection.close()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/addbookForm")
def addBookForm():
        return render_template("addbookForm.html")

@app.route("/addbook", methods=["GET","POST"])
def addBOOKs():
    if request.method == "POST":
        try:
            ID = request.form["ID"]
            Title = request.form["title"]
            Author = request.form["author"]
            Status = request.form["status"]

            with sqlite3.connect('Library_Data.db') as db:
                cur = db.cursor()
                cur.execute("INSERT into LibraryBookData (ID, Title, Author, Status) values (?,?,?,?)",(ID, Title, Author, Status))
                print('3')
                db.commit()
                flash("ADDEDE SUCCESSFULLY")
        
        except Exception as e:
            db.rollback()
            flash("TRY AGAIN LATER")
            
        finally:
            return redirect(url_for("home"))
            db.close()

@app.route('/viewbooks')
def viewbooks():
    with sqlite3.connect('Library_Data.db') as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM LibraryBookData")
        rows = cur.fetchall()

    return render_template('viewbook.html', rows = rows)

@app.route('/deletebooks', methods=['GET', 'POST'])
def deletebooks():
    if request.method == 'POST':
        ID = request.form['ID']
        with sqlite3.connect('Library_Data.db') as db:
            try:
            
                cur = db.cursor()
                cur.execute('DELETE FROM LibraryBookData WHERE ID = ?', [ID])
                db.commit()
                flash('DELETED SUCCESSFULLY')
            except Exception as e:
                db.rollback()
                print(e)
            finally:
                return redirect(url_for("home"))
                db.close()

    elif request.method == 'GET':
        return render_template('deletebooksForm.html')

@app.route('/issuebook', methods=['GET', 'POST'])
def issuebook():
    if request.method == 'GET':
        return render_template('issuebook.html')
    elif request.method == 'POST':
        ID = request.form['ID']
        IssueTo = request.form['issuetoNAME']
        
        with sqlite3.connect('Library_Data.db') as db:
            try:
                cur = db.cursor()
                cur.execute('UPDATE LibraryBookData SET Status = "issued" WHERE Status <> "issued" AND ID = ?',[ID])
                flash('SUCCESSFUL!!!')
            except:
                flash("CAN'T UPDATE")
            finally:
                return redirect(url_for('home'))

@app.route("/returnbook", methods=["GET", "POST"])
def returnbook():
    if request.method == "POST":
        ID = request.form['ID']
        
        with sqlite3.connect('Library_Data.db') as db:
            try:
                cur = db.cursor()
                cur.execute('UPDATE LibraryBookData SET Status = "avail" WHERE ID = ? AND Status <> "avail"',[ID])
                flash('SUCCESSFUL!!!')
            except:
                flash("CAN'T UPDATE")
            finally:
                return redirect(url_for('home'))
    elif request.method == "GET":
        return render_template('returnbook.html')

if __name__ == "__main__":
    app.run(debug=True)