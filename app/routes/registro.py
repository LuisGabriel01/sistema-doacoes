from flask import Blueprint, render_template, redirect
from flask_security.decorators import auth_required

from app.forms import AssistidoForm
from app.database import db_session
from app.models import Assistido

registros = Blueprint('registro',__name__)

@registros.route('/registro', methods=['GET', 'POST'])
@auth_required()
def registro():
    form = AssistidoForm()
    print(form.errors)
    if form.validate_on_submit():
        print('validado!!!')
        print(form.data)
        data = form.data
        data.pop('csrf_token')
        print(data)
        row = Assistido(**data)
        db_session.add(row)
        db_session.commit()
        return redirect('/') # /success
    return render_template('registro_assistido.html', form=form)