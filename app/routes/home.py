from flask import Blueprint, render_template_string, render_template
from flask_security import Security, auth_required
from sqlalchemy import select
from app.models import User
from app.database import db_session

homes = Blueprint('home',__name__)

@homes.route('/')
@auth_required()
def home():
    stmt = select(User)
    query = db_session.scalars(stmt).all()
    return render_template('index.html',query=query)