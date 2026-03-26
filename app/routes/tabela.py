from flask import Blueprint, render_template, redirect, render_template_string
from flask_security.decorators import auth_required

from sqlalchemy import select
from app.database import db_session
from app.models import Assistido, Doador, Coleta, Entrega, Instituicao, Item

tabelas = Blueprint('tabelas',__name__)

models = {
    'assistido': Assistido,
    'doador': Doador,
}

@tabelas.route('/registro/<table>', methods= ['GET'])
@auth_required()
def tabela(table):
    model = models[table]
    stmt = select(model)
    query = db_session.scalars(stmt).all()
    print(query)
    return render_template(f'tabelas/tabela_{table}.html.j2',query=query)