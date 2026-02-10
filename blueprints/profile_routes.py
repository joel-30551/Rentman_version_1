from flask import Blueprint, render_template

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/settings')
def settings():
    return render_template('settings.html')




