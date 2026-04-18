from datetime import datetime
from flask import Blueprint, render_template, redirect, request, url_for, render_template_string
from flask_security.decorators import auth_required
from flask_wtf import FlaskForm

from sqlalchemy import select
from app.forms import AssistidoForm, DoadorForm, ColetaForm, EntregaForm
from app.database import db_session
from app.models import Assistido, Doador, Coleta, Instituicao, Entrega, Item, NomeItem, CategoriaItem

doacao_blueprint = Blueprint('doacao',__name__)

tables = {
    'coleta' : {
        'form': ColetaForm,
        'model': Coleta,
        'pessoa': Doador,
        'pessoa_id': 'doador_id',
        'nome': 'nome_doador'
    },
    'entrega' : {
        'form': EntregaForm,
        'model': Entrega,
        'pessoa': Assistido,
        'pessoa_id': 'assistido_id',
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
        if table == 'coleta':
            pessoa_id = model.doador_id
            filter_pessoa_id = request.args['doador']
        elif table == 'entrega':
            pessoa_id = model.assistido_id
            filter_pessoa_id = request.args['assistido']
    except (AttributeError, KeyError):
        pass
    stmt = (
    select(
        model.id, 
        model.data_hora, 
        pessoa.nome.label(nome),
        Instituicao.nome.label("nome_instituicao")
    )
    .join(pessoa, pessoa_id == pessoa.id) # type: ignore
    .join(Instituicao, model.instituicao_id == Instituicao.id)
    )
    try:
        stmt = stmt.where(pessoa_id == filter_pessoa_id) # type: ignore
    except UnboundLocalError:
        pass

    query = db_session.execute(stmt).all()
    return render_template(f'doacao/tabela/{table}.html.j2',query=query)

# id==0 para incluir novo?
@doacao_blueprint.route('/doacao/<table>/<int:id>', methods=['GET', 'POST'])
@auth_required()
def tabela_itens(table, id): 
    if id == 0:
        model = tables[table]['model']
        pessoa = tables[table]['pessoa']
        nome = tables[table]['nome']
        pessoa_id = tables[table]['pessoa_id']
        try:
            if table == 'coleta':
                # pessoa_id = model.doador_id
                filter_pessoa_id = request.args['doador']
            elif table == 'entrega':
                # pessoa_id = model.assistido_id
                filter_pessoa_id = request.args['assistido']
        except (AttributeError, KeyError):
            pass
        new_doacao = model(**{
            'data_hora': datetime.now(),
            pessoa_id: filter_pessoa_id, # type: ignore
            'instituicao_id': 1,
        })
        db_session.add(new_doacao)
        db_session.commit()
        return redirect(url_for('doacao.tabela_itens', **{'table': table, 'id': new_doacao.id, pessoa_id: filter_pessoa_id})) # type: ignore
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
    
    return render_template(f'doacao/tabela/item.html.j2',query=query)

@doacao_blueprint.route('/doacao/<table>/<int:id>/adicionar', methods=['GET', 'POST'])
@auth_required()
def tabela_adicionar_item(table, id): 
    nome_coluna = f'{table}_id' 
    coluna = getattr(Item, nome_coluna)
    model = tables[table]['model']
    nome_id = request.args.get('nome_item_id')
    try:
        if table == 'coleta':
            pessoa_id = model.doador_id
            filter_pessoa_id = 'doador_id'
        elif table == 'entrega':
            pessoa_id = model.assistido_id
            filter_pessoa_id = 'assistido_id'
    except (AttributeError, KeyError):
        pass

    stmt = (
        select(
            model.id,
            pessoa_id.label('pessoa_id'), # type: ignore
        )
        .where(model.id == id)
    )

    query = db_session.execute(stmt).all()

    if not query:
        from flask import abort
        abort(404)
    new_item = Item(**{
        filter_pessoa_id: query[0].pessoa_id, #type: ignore
        'nome_id': nome_id,
        f'{table}_id': id,
    })
    db_session.add(new_item)
    db_session.commit()
    
    return redirect(url_for('doacao.tabela_itens', **{'table': table, 'id': id})) # type: ignore

@doacao_blueprint.route('/doacao/<table>/<int:id>/escolher', methods=['GET', 'POST'])
@auth_required()
def tabela_escolher_item(table, id): 
    if id == 0:
        model = tables[table]['model']
        pessoa = tables[table]['pessoa']
        nome = tables[table]['nome']
        pessoa_id = tables[table]['pessoa_id']
        try:
            if table == 'coleta':
                # pessoa_id = model.doador_id
                filter_pessoa_id = request.args['doador']
            elif table == 'entrega':
                # pessoa_id = model.assistido_id
                filter_pessoa_id = request.args['assistido']
        except (AttributeError, KeyError):
            pass
        new_doacao = model(**{
            'data_hora': datetime.now(),
            pessoa_id: filter_pessoa_id, # type: ignore
            'instituicao_id': 1,
        })
        db_session.add(new_doacao)
        db_session.commit()
        return redirect(url_for('doacao.tabela_itens', **{'table': table, 'id': new_doacao.id, pessoa_id: filter_pessoa_id})) # type: ignore
    nome_coluna = f'{table}_id' 
    coluna = getattr(Item, nome_coluna)
    
    stmt = (
        select(
            NomeItem.id,
            NomeItem.nome,
            # NomeItem.categoria_id,
            CategoriaItem.nome.label('categoria_nome'),
        )
        .join(CategoriaItem, NomeItem.categoria_id == CategoriaItem.id)
    )

    query = db_session.execute(stmt).all()
    
    return render_template(f'doacao/tabela/escolher_item.html.j2',query=query)