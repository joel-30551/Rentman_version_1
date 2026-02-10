from flask import Blueprint, render_template, request, redirect, url_for, session, flash

profile_update_bp = Blueprint('profile_update', __name__, template_folder='templates')


def get_user_by_id(user_id):
    return {
        "name": "",
        "email": "",
        "phone": ""
    }

@profile_update_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = get_user_by_id(session['user_id'])
    return render_template('profile.html', user=user)

@profile_update_bp.route('/profile/update', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    

    flash("Profile updated successfully!", "success")
    return redirect(url_for('profile_update.profile'))

@profile_update_bp.route('/profile/change-password')
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('change_password.html')

@profile_update_bp.route('/profile/delete', methods=['GET', 'POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        session.clear()
        flash("Your account has been deleted.", "info")
        return redirect(url_for('home'))  

    
    return render_template('delete_account.html')
