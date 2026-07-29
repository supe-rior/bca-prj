from flask import Flask,render_template,request,redirect,url_for,flash,session,make_response

import os
app=Flask(__name__)
app.secret_key="mykey"
UPLOAD_DIR='uploads'
app.config['UPLOAD_FOLDER']=UPLOAD_DIR

@app.route('/')
def home():
    name='Krish'
    isValid=True
    return render_template('index.html',name1=name,isValid=isValid)

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    contactDetails={
        "Ram":{"Email":"Ram@gmail.com","phone":"9853452234"},
        "Shyam":{"Email":"shyam@gmail.com","phone":"988652654"}
    }
    return render_template('contact.html',details=contactDetails)
@app.route('/services')
def services():
    return render_template('services.html')
@app.route('/login',methods=['POST','GET'])
def login():
    user="admin"
    password="admin123"
    if request.method=='POST':
        username=request.form['username']
        pwd=request.form['password']
        if user==username and pwd==password:
            session['user']="Krish" #setting session
            session['email']='abc@gmail.com'
            return redirect('/dashboard')
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html')
    else:
        return redirect('login')
@app.route('/signup', methods=['POST','GET'])
def signup():
    errors=[]
    if request.method == "POST":
        username=request.form['username'].strip()
        password=request.form['password'].strip()
        email=request.form['email'].strip()
        images=request.files['image']
        if not username:
            errors.append("Username is required.")
        if not password:
            errors.append("Password is required.")
        elif len(password)<8:
            errors.append("Password should be 8 or more characters.")
        if not email:
            errors.append("Email is reqiured.")
        elif '@' not in email or '.' not in email:
            errors.append("Input Valid Email")
        if not errors:
            if images.filename:
                images.save(os.path.join(app.config['UPLOAD_FOLDER'],images.filename))
            flash("User Created")
            return redirect(url_for('login'))
    return render_template('signup.html',errors=errors)
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
@app.route('/setcookie')
def setcookie():
    resp=make_response("Cookie is set")
    resp.set_cookie('user',"Krish")
    return resp
@app.route('/getcookie')
def getcookie():
    user=request.cookies.get('user')
    if user:
        return f"Welcome {user}"
    else:
        return "You are new here!"
@app.route('/deletecookie')
def deletecookie():
    resp=make_response("Cookie Deleted")
    resp.delete_cookie('user')
    return resp








if  __name__=='__main__':
    app.run(debug=True)