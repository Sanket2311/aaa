from flask import Flask, render_template, url_for, redirect,request, flash
from flask_sqlalchemy import SQLAlchemy

# import os

app = Flask(__name__)
app.secret_key = "Secret key"
 


#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://n1kgmt4q3oqm5vd8:yzay4mron21zi4np@u6354r3es4optspf.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/g6k28qe8qz4sd3us"
#"mysql://root:''@localhost/crud"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
 
 
#Creating model table for our CRUD database
class Data(db.Model):
    student_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    dob = db.Column(db.Date())
    amount_due = db.Column(db.String(100))
 
    def __init__(self, first_name, last_name, dob, amount_due):
 
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.amount_due = amount_due
 
 

@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", students = all_data)

 
#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():
 
    if request.method == 'POST':
 
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        amount_due = request.form['amount_due']
 
        my_data = Data(first_name, last_name, dob, amount_due)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Student Inserted Successfully")
 
        return redirect(url_for('Index'))
 
 
 
#this is our update route where we are going to update our student
@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('student_id'))
 
        my_data.first_name = request.form['first_name']
        my_data.last_name = request.form['last_name']
        my_data.dob = request.form['dob']
        my_data.amount_due=request.form['amount_due']
 
        db.session.commit()
        flash("Student Updated Successfully")
 
        return redirect(url_for('Index'))
 
 
#This is our delete route where we are going to delete our student
@app.route('/delete/<student_id>/', methods = ['GET' , 'POST'])
def delete(student_id):

    my_data = Data.query.get(student_id)
    db.session.delete(my_data)
    db.session.commit()

    flash("Student Deleted Successfully")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)