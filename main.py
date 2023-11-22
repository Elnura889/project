from flask import Flask, get_flashed_messages
from flask import render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask import send_file
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databasedb.db'
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(150))
    posts = db.relationship('Post', backref='user', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10000))
    content = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_filename = db.Column(db.String(255))

@app.route('/')   # Main page
def index():
        return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    user_id = session.get("user_id")
    posts = Post.query.filter_by(user_id=user_id).all()  # Get all user posts

    if request.method == 'POST':
        post_data = request.form
        title = post_data["title"]
        content = post_data["content"]
        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save(os.path.join('static/uploads', filename))
        post = Post(title=title, content=content, user_id=user_id, image_filename=filename)

        # Remove the following line
        # if image:
        #     filename = secure_filename(image.filename)
        #     image.save(os.path.join('uploads', filename))
        #     post = Post(title=title, content=content, user_id=user_id, image=filename)

        db.session.add(post)
        db.session.commit()
        flash("Your post is successfully added!", "success")
        return redirect("/add")

    return render_template("add_post.html", posts=posts)



@app.route('/view_profile')
def view_profile():
    user_id = session.get('user_id')
    if user_id:
        posts = Post.query.filter_by(user_id=user_id)
        posts = Post.query.all()
        return render_template('view_profile.html', posts=posts, os=os)
    return "No posts found."


@app.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    post = Post.query.get(post_id)

    if post:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully!", "success")

    return redirect("/add")
@app.route('/home')
def home():
    if 'username' in session:
        greeting = 'Welcome, ' + session['username'] + '!'
    else:
        greeting = 'You are not logged in.'
    return render_template('home.html', greeting=greeting)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                flash('Logged in successfully!', category='success')
                session['user_id'] = user.id  # Store the user ID in the session
                return redirect(url_for('home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html")

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Email already exists.', category='error')
            return render_template("registration.html", messages=get_flashed_messages())
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
            return render_template("registration.html", messages=get_flashed_messages())
        elif password1 != password2:
            flash('Passwords don`t match.', category='error')
            return render_template("registration.html", messages=get_flashed_messages())
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
            return render_template("registration.html", messages=get_flashed_messages())
        else:
            user = User(email=email, username=username, password=password2)
            db.session.add(user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('login'))
    return render_template("registration.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', category='info')
    return render_template("hom.html")

@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if request.method == 'POST':
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            db.session.delete(user)
            db.session.commit()
            session.pop('username', None)
            session.pop('user_id', None)
            flash('You have deleted account!', category='info')
        return redirect(url_for('index'))
    return render_template('delete_account.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = os.path.join('static/uploads', file.filename)
            file.save(filename)
            flash(f'File {file.filename} succesfuly upload.', 'success')
            return redirect(url_for('upload'))

    return render_template('fileupload.html')

    # function to view and delete files
@app.route('/files', methods=['GET', 'POST'])
def files():
    if request.method == 'POST':
        # get a list of files in the uploads directory
        files = os.listdir('static/uploads')

        # If  click the "delete" button, we delete the selected file
        if 'delete' in request.form:
            filename = request.form['delete']
            if filename in files:
                os.remove(os.path.join('static/uploads', filename))
                flash(f'File {filename} deleted.', 'success')
                return redirect(url_for('files'))

        # Passing a list of files to the page
    files = os.listdir('static/uploads')
    return render_template('files.html', files=files)

    # Function for downloading files
@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join('static/uploads', filename)
    return send_file(file_path, as_attachment=True)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return redirect(url_for('index'))

    if request.method == 'POST':
        post_data = request.form
        title = post_data["title"]
        content = post_data["content"]
        filename = post.image_filename if post.image_filename else None
        image = request.files['image'] if 'image' in request.files else None

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join('static/uploads', filename))

        post.title = title
        post.content = content
        post.image_filename = filename
        db.session.commit()
        flash("Your post is successfully updated!", "success")
        return redirect(url_for('add'))

    return render_template("edit_post.html", post=post)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
