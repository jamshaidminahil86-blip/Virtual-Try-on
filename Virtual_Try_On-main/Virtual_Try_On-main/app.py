import requests

from flask import Flask, request, render_template, url_for,abort,jsonify, redirect, session, flash
from extensions import db # Import db and bcrypt from extensions
from models import Admin, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/try_on'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'b9d2188f098760c5ba1997a5a292e9d8f2923cf5c8b2e6594b7cbb42d456edb1'  # Set a secret key for sessions

# Initialize the app with the extensions
db.init_app(app)

#Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()  # Get JSON data from the frontend
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if the email already exists in the database
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'success': False, 'message': 'Email already exists!'})

    # Create a new user
    new_user = User(username=username, email=email, password=password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Sign up successful! Please log in.'})
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({'success': False, 'message': 'Signup failed. Please try again.'})

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Get JSON data from the frontend
    email = data.get('email')
    password = data.get('password')

 # Check for admin login
    admin = Admin.query.filter_by(email=email).first()
    if admin and admin.password == password:
        session['admin_id'] = admin.id
        return jsonify({'success': True, 'message': 'Admin login successful!', 'redirect': 'admin_dashboard'})

    # Find user by email
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        # Store user session
        session['user_id'] = user.id
        return jsonify({'success': True, 'message': 'Login successful!'})
    else:
        return jsonify({'success': False, 'message': 'Invalid email or password.'})
    
#logout Route
@app.route("/logout")
def logout():
    session.pop('user_id', None)  # Clear the session
    return redirect(url_for('index'))  # Redirect to home page

#Change_password Route
@app.route('/change-password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        flash('You must be logged in to change your password.', 'danger')
        return redirect(request.referrer or url_for('index'))

    old_password = request.form['old_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    user = User.query.get(session['user_id'])

    if not user or user.password != old_password:
        flash('Old password is incorrect.', 'danger')
        return redirect(request.referrer or url_for('index'))

    if new_password != confirm_password:
        flash('New passwords do not match.', 'danger')
        return redirect(request.referrer or url_for('index'))

    # Update password (plain text)
    user.password = new_password
    db.session.commit()

    flash('Password updated successfully!', 'success')
    return redirect(request.referrer or url_for('index'))

#Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))

    users = User.query.all()  # Fetch all users
    print(users)  # Add this to debug and check the data
    user_count = len(users)   # Get the total number of users

    return render_template('dashboard.html', users=users, user_count=user_count)


PIXELCUT_API_KEY = "sk_43d702073b0e44dda8218644b381de2c"
PIXELCUT_URL = "https://api.developer.pixelcut.ai/v1/try-on"

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route("/admin_dashboard")
def admin_dashboard():
    if 'admin_id' in session:
        return render_template("dashboard.html")
@app.route("/db-user")
def user():
    return render_template("db-user.html")

@app.route("/db-bc")
def change():
    return render_template("db-bc.html")

@app.route("/db-en")
def enhance():
    return render_template("db-en.html")

@app.route("/db-br")
def background():
    return render_template("db-br.html")
@app.route("/User Profile")
def profile():
    return render_template("userprofile.html")
@app.route('/features')
def features():
    return render_template('features.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/tryon')
def tryon():
     return render_template('app.html')
 
@app.route('/virtual-tryon', methods=['POST'])
def virtual_tryon():
    person_image = request.files['person_image']
    garment_image = request.files['garment_image']

    files = {
        "person_image": (person_image.filename, person_image.stream, person_image.mimetype),
        "garment_image": (garment_image.filename, garment_image.stream, garment_image.mimetype)
    }

    headers = {"X-API-KEY": PIXELCUT_API_KEY}
    response = requests.post(PIXELCUT_URL, headers=headers, files=files)

    if response.status_code == 200:
        result_url = response.json().get("result_url")
        return render_template('app.html', result_url=result_url)
    else:
        error = response.text
        return render_template('app.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
