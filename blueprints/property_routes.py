from flask import Blueprint, render_template

property_bp = Blueprint('property', __name__, url_prefix='/properties')

@property_bp.route('/advertise')
def advertise():
    return render_template('advertise.html')

@property_bp.route('/explore')
def explore():
    return render_template('explore.html')

@property_bp.route('/saved')
def saved():
    return render_template('saved.html')

@property_bp.route('/<int:id>')
def property_detail(id):
    property_info = {
        "id": id,
        "title": f"Property #{id}",
        "description": "Details about the property."
    }
    return render_template('property_detail.html', prop=property_info)
