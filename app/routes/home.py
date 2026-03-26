from flask import Blueprint, render_template_string, render_template
from flask_security import Security, auth_required
from sqlalchemy import select
from app.models import User, Assistido
from app.database import db_session

homes = Blueprint('home',__name__)

@homes.route('/')
@auth_required()
def home():
    stmt = select(User)
    test = select(Assistido)
    query = db_session.scalars(stmt).all()
    qt = db_session.scalars(test).all()
    print(qt[0].__class__.__table__.columns.keys())
    print(query[0].__class__.__table__.columns.keys())
    return render_template('index.html.j2',query=query)
