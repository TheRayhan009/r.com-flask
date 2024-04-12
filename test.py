import flask
from flask_mail import Mail
from flask import request ,redirect ,url_for,session
from flask import Flask , render_template
from flask_sqlalchemy import SQLAlchemy
import MySQLdb
import json
# Define a decorator function to check if the user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('first_login'))  # Redirect to login page if not logged in
        return f(*args, **kwargs)
    return decorated_function

# Apply the login_required decorator to routes that require login
@panel.route("/home")
@login_required
def home():
    b = blogs
    return render_template("index.html", b=b)

@panel.route("/post/<string:post_slug>", methods=["GET"])
@login_required
def postx(post_slug):
    post = Post.query.filter_by(slug=post_slug).first()
    return render_template("post.html", post=post)

@panel.route("/about")
@login_required
def about():
    p = paramiters
    return render_template("about.html", p=p)

@panel.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    if request.method == "POST":
        name = request.form.get("username")
        email = request.form.get("email")
        message = request.form.get("message")
        entry = Contact(username=name, email=email, message=message)
        db.session.add(entry)
        db.session.commit()
        return render_template("scontac.html")
    return render_template("contact.html")

@panel.route("/blog")
@login_required
def Xblog():
    b = blogs
    return render_template("blog.html", b=b)

@panel.route("/login", methods=["GET", "POST"])
def Xlogin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        entry = Login(unameemail=username, password=password)
        db.session.add(entry)
        db.session.commit()
        return render_template("slogin.html")
    return render_template("login.html")

# Add other routes here...

# Apply the login_required decorator to the addpost route
@panel.route("/addpost", methods=["GET", "POST"])
@login_required
def addpost():
    if request.method == "POST":
        title = request.form.get("title")
        slug = request.form.get("slug")
        content = request.form.get("content")
        date = request.form.get("date")
        entry = Post(titel=title, slug=slug, content=content, date=date)
        db.session.add(entry)
        db.session.commit()
    return render_template("addpost.html")

# Apply the login_required decorator to the addpostlogin route
@panel.route("/addpostlogin", methods=["GET", "POST"])
def addlogin():
    user = request.form.get("username")
    password = request.form.get("password")
    if user == paramiters["loguser"] and password == paramiters["logpass"]:
        session['logged_in'] = True  # Set session variable to indicate logged in
        return redirect(url_for("addpost"))
    return render_template("addpostlogin.html")

# Define the logout route
@panel.route("/logout")
def logout():
    session.pop('logged_in', None)  # Remove logged_in session variable
    return redirect(url_for('first_login'))  # Redirect to login page

# Other routes...

panel.run(debug=True)
