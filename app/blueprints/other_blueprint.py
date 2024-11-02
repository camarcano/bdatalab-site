from flask import Blueprint, render_template

other_bp = Blueprint('other', __name__, url_prefix='/other')

@other_bp.route('/')
def other_home():
    return render_template('other/other_page.html', title="Other Page")
