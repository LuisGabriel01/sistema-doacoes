from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    StringField,
    DecimalField,
    IntegerField,
    SelectField,
    validators,
)
from app.models import TipoImovel, EstadoCivil


class ContatoForm(FlaskForm):
    nome = StringField(
        "Nome", validators=[validators.InputRequired(), validators.Length(min=3)]
    )
    endereco = StringField("Endereço", validators=[validators.InputRequired()])
    email = StringField(
        "Email", validators=[validators.InputRequired(), validators.Email()]
    )
    telefone = StringField("Telefone", validators=[validators.InputRequired()])

class DoadorForm(ContatoForm):
    pass

class AssistidoForm(ContatoForm, FlaskForm):
    tipo_imovel = SelectField(
        "Tipo de Imóvel",
        choices=[(e.value, e.value) for e in TipoImovel],
        validators=[validators.InputRequired()],
    )
    valor_aluguel = IntegerField("Valor do Aluguel", validators=[validators.Optional()])
    estado_civil = SelectField(
        "Estado Civil",
        choices=[(e.value, e.value) for e in EstadoCivil],
        validators=[validators.InputRequired()],
    )
    numero_adultos = IntegerField(
        "Número de Adultos",
        validators=[validators.InputRequired(), validators.NumberRange(min=0)],
    )
    criancas_pequenas = IntegerField(
        "Crianças Pequenas",
        validators=[validators.InputRequired(), validators.NumberRange(min=0)],
    )
    adolescentes = IntegerField(
        "Adolescentes",
        validators=[validators.InputRequired(), validators.NumberRange(min=0)],
    )
    doentes = BooleanField("Possui Doentes")
    bolsa_familia = BooleanField("Bolsa Família")
    aposentado = BooleanField("Aposentado")
    pensao = BooleanField("Recebe Pensão")
    cesta_basica = BooleanField("Recebe Cesta Básica")
    atividade_remunerada = BooleanField("Atividade Remunerada")
    renda = DecimalField("Renda", validators=[validators.InputRequired()], places=2)
    crianca_escola = BooleanField("Crianças na Escola")
    observacoes = StringField("Observações", validators=[validators.Optional()])

class ColetaForm(FlaskForm):
    pass

class EntregaForm(FlaskForm):
    pass