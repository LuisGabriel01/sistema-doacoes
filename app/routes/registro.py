from flask import Blueprint, render_template, redirect
from flask_security.decorators import auth_required

from sqlalchemy import select
from app.forms import AssistidoForm
from app.database import db_session
from app.models import Assistido

registros = Blueprint('registro',__name__)

tables = {
    'assistido': {
        'form': AssistidoForm,
        'model': Assistido,
        'template': 'registro_assistido.html'
    },
    'doador': {
        'form': AssistidoForm,
        'model': Assistido,
        'template': 'registro_assistido.html'
    }
}

@registros.route('/registro/<table>/<int:id>', methods=['GET', 'POST'])
@auth_required()
def registro(table, id):
    form = AssistidoForm()
    if id != 0:
        stmt = select(Assistido).where(Assistido.id == id)
        assist = db_session.scalars(stmt).all()[0]
        ast = Assistido()
        print(assist)
        form = tables[table]['form'](obj=assist)
        print(form.errors)
    if form.validate_on_submit():
        print('validado!!!')
        print(form.data)
        data = form.data
        data.pop('csrf_token')
        print(data)
        row = tables[table]['model'](**data)
        db_session.add(row)
        db_session.commit()
        return redirect('/') # /success
    return render_template(tables[table]['template'], form=form, disabled=True)