from flask import Blueprint, render_template, redirect, request, url_for, render_template_string
from flask_security.decorators import auth_required
from flask_wtf import FlaskForm

from sqlalchemy import select
from app.forms import AssistidoForm, DoadorForm, ColetaForm, EntregaForm
from app.database import db_session
from app.models import Assistido, Doador, Coleta, Instituicao, Entrega, Item, NomeItem

doacao_blueprint = Blueprint('doacao',__name__)

tables = {
    'coleta' : {
        'form': ColetaForm,
        'model': Coleta,
        'pessoa': Doador,
        'nome': 'nome_doador'
    },
    'entrega' : {
        'form': EntregaForm,
        'model': Entrega,
        'pessoa': Assistido,
        'nome': 'nome_assistido'
    }
}

@doacao_blueprint.route('/doacao/<table>', methods= ['GET'])
@auth_required()
def tabela_doacao(table):
    model = tables[table]['model']
    pessoa = tables[table]['pessoa']
    nome = tables[table]['nome']
    try:
        pessoa_id = model.doador_id
    except AttributeError:
        pessoa_id = model.assistido_id
    try:
        filter_pessoa_id = request.args['assistido']
    except KeyError:
        pass
    try:
        filter_pessoa_id = request.args['doador']
    except KeyError:
        pass
    stmt = (
    select(
        model.id, 
        model.data_hora, 
        pessoa.nome.label(nome),
        Instituicao.nome.label("nome_instituicao")
    )
    .join(pessoa, pessoa_id == pessoa.id)
    .join(Instituicao, model.instituicao_id == Instituicao.id)
    )
    try:
        stmt = stmt.where(pessoa_id == filter_pessoa_id) # type: ignore
    except UnboundLocalError:
        pass

    query = db_session.execute(stmt).all()
    print(query[0])
    return render_template(f'doacao/{table}.html.j2',query=query)

# id==0 para incluir novo?
@doacao_blueprint.route('/doacao/<table>/<int:id>', methods=['GET', 'POST'])
@auth_required()
def tabela_itens(table, id): 
    nome_coluna = f'{table}_id' 
    coluna = getattr(Item, nome_coluna)
    
    stmt = (
        select(
            Item.id,
            NomeItem.nome.label("nome_do_item"),
            Doador.nome.label("nome_doador"),
            Instituicao.nome.label("nome_instituicao"),
            Assistido.nome.label("nome_assistido"),
            Item.entrega_id.label("id_entrega"),
            Item.coleta_id.label("id_coleta") 
        )
        .join(NomeItem, Item.nome_id == NomeItem.id)
        .outerjoin(Doador, Item.doador_id == Doador.id)
        .outerjoin(Instituicao, Item.instituicao_id == Instituicao.id)
        .outerjoin(Assistido, Item.assistido_id == Assistido.id)
        .where(coluna == id)
    )

    query = db_session.execute(stmt).all()
    
    print(query)
    
    return render_template(f'doacao/item.html.j2',query=query)
