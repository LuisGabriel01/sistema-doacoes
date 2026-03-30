from flask import Blueprint, render_template, redirect, request, url_for, render_template_string
from flask_security.decorators import auth_required
from flask_wtf import FlaskForm

from sqlalchemy import select
from app.forms import AssistidoForm, DoadorForm, ColetaForm
from app.database import db_session
from app.models import Assistido, Doador, Coleta, Instituicao

cadastro_blueprint = Blueprint('cadastro',__name__)

tables = {
    'assistido': {
        'form': AssistidoForm,
        'model': Assistido,
    },
    'doador': {
        'form': DoadorForm,
        'model': Doador,
    },
}

@cadastro_blueprint.route('/cadastro/<table>', methods= ['GET'])
@auth_required()
def tabela(table):
    model = tables[table]['model']
    stmt = select(model)
    query = db_session.scalars(stmt).all()
    print(type(query))
    return render_template(f'cadastro/{table}.html.j2',query=query)

# id==0 para incluir novo?
@cadastro_blueprint.route('/cadastro/<table>/<int:id>', methods=['GET', 'POST'])
@auth_required()
def ficha(table, id):
    model = tables[table]['model']
    form = tables[table]['form']()
    read_only = True
    try:
        if request.args['edit'] == 'true':
            read_only = False
    except KeyError:
        pass
    if id != 0:
        query = db_session.query(model).get(id)
        form = tables[table]['form'](obj=query)
        if request.method == 'POST':
            print(form.errors)
            if form.validate_on_submit():
                print('validado!!!')
                form.populate_obj(query)
                db_session.add(query)
                db_session.commit()
                return redirect(request.url)
            else:
                print('erro validacao')
    else:
        if request.method == 'POST':
            print(form.errors)
            if form.validate_on_submit():
                print('validado!!!')
                data = form.data
                data.pop('csrf_token')
                db_session.add(model(**data))
                db_session.commit()
                return redirect(request.url)
            else:
                print('erro validacao')

    return render_template(f'cadastro/ficha/{table}.html.j2', form=form, read_only=read_only)
