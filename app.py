from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from db_config import get_db_connection
from auth import auth_bp  
from blueprints.property_routes import property_bp
from blueprints.profile_routes import profile_bp
from blueprints.profile_update import profile_update_bp


app = Flask(__name__)
app.secret_key = ''  


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(property_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(profile_update_bp)



@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        contact = request.form['contact']

        db = get_db_connection()
        cursor = db.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (email, password, name, contact_number) VALUES (%s, %s, %s, %s)",
                (email, password, name, contact)
            )
            db.commit()
        except Exception as e:
            db.rollback()
            return f"Error: {str(e)}"
        finally:
            cursor.close()
            db.close()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            session['user_phone'] = user['contact_number']
            return redirect(url_for('home'))
        else:
            return "Invalid credentials"

    return render_template ("/login.html")


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}



@app.route('/logout')  
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/explore')
def explore():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('explore.html')

@app.route('/advertise')
def advertise():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('advertise.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html')

@app.route('/saved')
def saved():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('saved.html')

@app.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('settings.html')


if __name__ == '__main__':
    app.run(debug=True)
