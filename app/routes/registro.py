from flask import Blueprint, render_template, redirect
from flask_security.decorators import auth_required
from flask_wtf import FlaskForm

from sqlalchemy import select
from app.forms import AssistidoForm, DoadorForm
from app.database import db_session
from app.models import Assistido, Doador

registros = Blueprint('registro',__name__)

tables = {
    'assistido': {
        'form': AssistidoForm,
        'model': Assistido,
        'template': 'registro/assistido.html.j2'
    },
    'doador': {
        'form': DoadorForm,
        'model': Doador,
        'template': 'registro/doador.html.j2'
    }
}

# id==0 para incluir novo
# @registros.route('/registro', defaults={'table': table, 'id': None}, methods=['GET', 'POST'])
@registros.route('/registro/<table>/<int:id>', methods=['GET', 'POST'])
@auth_required()
def registro(table, id):
    model = tables[table]['model']
    form = tables[table]['form']()
    template = tables[table]['template']
    disabled=False
    if id != 0:
        disabled=True
        stmt = select(model).where(model.id == id)
        query = db_session.scalars(stmt).all()[0]
        # print(query)
        form = tables[table]['form'](obj=query)
        # print(form.errors)
    if form.validate_on_submit():
        # print('validado!!!')
        # print(form.data)
        data = form.data
        data.pop('csrf_token')
        print(data)
        row = tables[table]['model'](**data)
        db_session.add(row)
        db_session.commit()
        return redirect('/') # /success
    return render_template(template_name_or_list=template, form=form, disabled=disabled)