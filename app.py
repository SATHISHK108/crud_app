from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16).hex()
bcrypt = Bcrypt(app)

load_dotenv()
database_uri = os.environ.get('DATABASE_URI')
print('database_uri', database_uri)

# Replace the placeholders with your actual connection details
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
print('db connection successfull')
print('db', db)

class UserDetails(db.Model):
    __tablename__ = 'userdetails'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True)
    password_ = db.Column(db.String(255))
    phone_number = db.Column(db.BigInteger)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        email = request.form.get('email')

        user = UserDetails.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password_, password):
            username = user.username
            phone_number = user.phone_number
            session['id'] = user.id
            return render_template('profile.html', username=username, email=email, phone_number=phone_number)
        else:
            flash("Invalid email or password", "error")
            return redirect('/')


@app.route("/adduser", methods=['POST'])
def adduser():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        phone = request.form.get('phone')

        try:
            new_user = UserDetails(username=username, email=email, password_=hashed_password, phone_number=phone)
            db.session.add(new_user)
            db.session.commit()

            flash("User added successfully, please login now", "success")

            return render_template('signup.html')
        
        except IntegrityError:
            # Handle the case when a unique constraint violation occurs
            # Email already exists in the database
            flash("Email already exists. Please sign up with a different email.", "error")

            return render_template('signup.html')

        except Exception as e:
            # Handle any other exceptions that may occur
            print("Error adding user:", str(e))

            flash("An error occurred while adding the user. Please try again later.", "error")

            return render_template('signup.html')

    # Handle the case when the request method is not POST
    return "Invalid request method"

@app.route('/edit_profile')
def editprofile():
    #email = session.get('email')
    id = session.get('id')
    if id:
        user = UserDetails.query.filter_by(id = id).first()
        if user:
            return render_template('edit_profile.html', user=user)
        else:
            flash('User not found', 'error')
            return redirect('/')
    else:
        flash('You need to log in', 'error')
        return render_template('profile.html')
    
@app.route('/updateprofile',methods=['POST'])
def updateprofile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')

        #session_email = session.get('email')
        id = session.get('id')

        user = UserDetails.query.filter_by(id = id).first()

        if user:
            try:
                UserDetails.query.filter_by(id = id).update(
                    {UserDetails.username: username,
                    UserDetails.email: email,
                    UserDetails.phone_number: phone}
                )
                db.session.commit()
                user=UserDetails.query.filter_by(id = id).first()
                flash('Profile updated successfully!!!', 'success')
                return render_template('profile.html',username=user.username, email=user.email, phone_number=user.phone_number)
            except Exception as e:
                print(f'error while updating the profile {e}')
                flash(e, 'error')
                return render_template('profile.html',username=user.username, email=user.email, phone=user.phone_number)
        # else:
        #     flash('User not found', 'error')
        #     return render_template('edit_profile.html', user=UserDetails.query.filter_by(id = id).first())

@app.route('/delete_profile', methods=['POST'])
def deleteprofile():
        #sessionemail = session.get('email')
        id = session.get('id')
        user = UserDetails.query.filter_by(id=id).first()

        if user:
            db.session.delete(user)
            db.session.commit()
            flash("Profile deleted successfully", "success")
            return render_template('profile.html')
        else:
            flash("Error!!!", "error")
            return render_template('profile.html')           


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)