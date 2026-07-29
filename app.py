from flask import Flask,render_template,redirect,request,url_for,flash,session,make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:%40nime4ever@localhost/PythonDb'#@=%40
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class Users(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(150),nullable=False)
    status=db.Column(db.Integer)

class posts:
    __tablename__='posts'
    id=db.Column(db.Integer,primary_key=True)
    heading=db.Column(db.String(100),nullable=False)
    subheading=db.Column(db.String(150),nullable=False)
    posted_date=db.Column(db.DateTime,default=datetime.utcnow)
    post_by=db.Column(db.Integer, db.ForeignKey('users.id'))
    description=db.Column(db.Text)
    status=db.Column(db.Integer)

    users=db.relationship('Users', back_populates='posts')

@app.route('/')
def home():
    #users=Users.query.limit(4).all() #display first 3 data
    #users=Users.query.offset(3).limit(2).all() #display 2 data after first 3 data
    q=''
    users=Users.query.filter(Users.username.like(f"%{q}%")).all()
    #users=Users.query.filter(Users.status==1,).all()#filter by status and username
    #users=Users.query.filter(Users.status==1).order_by(Users.username.desc()).all()
    return render_template('index.html',users=users)
'''
    try:
        #Correct usage of raw SQL
        db.session.execute(text('SELECT 1'))
        return "MYSQL Connection Succesful!"
    except Exception as e:
        return f"Connection Failed: {str(e)}"
'''
@app.route('/adduser',methods=['GET','POST'])
def adduser():
    if request.method=="POST":
        user=Users(
            username=request.form['username'],
            password=request.form['password'],
            status=1
        )
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('adduser.html')
@app.route('/updateuser/<int:id>',methods=['GET','POST'])
def updateuser(id):
    user=Users.query.get(id)
    if request.method=="POST":
        user.username=request.form['username']
        user.password=request.form['password']
        db.session.commit()
        return redirect('/')
    return render_template('updateuser.html',user=user)
@app.route('/deleteuser/<int:id>')
def deleteuser(id):
    user=Users.query.get(id)
    db.session.delete(user)
    return redirect('/')




if __name__ == '__main__':
    app.run(debug=True)