
from flask import render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_db_connection
from . import auth_bp


@auth_bp.route('/update-profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    full_name = request.form['full_name']
    email = request.form['email']
    phone = request.form['phone']
    user_id = session['user_id']

    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE users SET name=%s, email=%s, contact_number=%s WHERE id=%s",
            (full_name, email, phone, user_id)
        )
        db.commit()
        session['user_name'] = full_name
        session['user_email'] = email
        session['user_phone'] = phone
        flash('Profile updated successfully.')
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}')
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('settings'))


@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    if new_password != confirm_password:
        flash('Passwords do not match.')
        return redirect(url_for('settings'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT password FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()

    if not user or not check_password_hash(user['password'], current_password):
        flash('Current password is incorrect.')
        return redirect(url_for('settings'))

    new_hashed = generate_password_hash(new_password)

    try:
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_hashed, session['user_id']))
        db.commit()
        flash('Password changed successfully.')
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}')
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('settings'))


@auth_bp.route('/toggle-2fa', methods=['POST'])
def toggle_2fa():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    current = session.get('2fa_enabled', False)
    session['2fa_enabled'] = not current
    flash('Two-factor authentication updated.')
    return redirect(url_for('settings'))


@auth_bp.route('/update-notifications', methods=['POST'])
def update_notifications():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    session['email_notifications'] = 'email_notifications' in request.form
    session['sms_notifications'] = 'sms_notifications' in request.form
    flash('Notification preferences updated.')
    return redirect(url_for('settings'))


@auth_bp.route('/delete-account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        db.commit()
        session.clear()
        flash('Your account has been deleted.')
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}')
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@auth_bp.route('/login')
def login():
    return redirect('/login')  
