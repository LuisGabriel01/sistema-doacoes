from flask import Blueprint, render_template_string
from flask_security import Security, auth_required

homes = Blueprint('home',__name__)

@homes.route('/')
@auth_required()
def home():
    return render_template_string('ola')