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


class AssistidoForm(FlaskForm):
    nome = StringField(
        "Nome", validators=[validators.DataRequired(), validators.Length(min=3)]
    )
    endereco = StringField("Endereço", validators=[validators.DataRequired()])
    # email = StringField(
        # "Email", validators=[validators.DataRequired(), validators.Email()]
    # )
    telefone = StringField("Telefone", validators=[validators.DataRequired()])
    # tipo_imovel = SelectField(
        # "Tipo de Imóvel",
        # choices=[(e.value, e.value) for e in TipoImovel],
        # validators=[validators.DataRequired()],
    # )
    # valor_aluguel = IntegerField("Valor do Aluguel", validators=[validators.Optional()])
    # estado_civil = SelectField(
    #     "Estado Civil",
    #     choices=[(e.value, e.value) for e in EstadoCivil],
    #     validators=[validators.DataRequired()],
    # )
    # numero_adultos = IntegerField(
    #     "Número de Adultos",
    #     validators=[validators.DataRequired(), validators.NumberRange(min=0)],
    # )
    # criancas_pequenas = IntegerField(
    #     "Crianças Pequenas",
    #     validators=[validators.DataRequired(), validators.NumberRange(min=0)],
    # )
    # adolescentes = IntegerField(
    #     "Adolescentes",
    #     validators=[validators.DataRequired(), validators.NumberRange(min=0)],
    # )
    # doentes = BooleanField("Possui Doentes")
    # bolsa_familia = BooleanField("Bolsa Família")
    # aposentado = BooleanField("Aposentado")
    # pensao = BooleanField("Recebe Pensão")
    # cesta_basica = BooleanField("Recebe Cesta Básica")
    # atividade_remunerada = IntegerField(
    #     "Atividade Remunerada",
    #     validators=[validators.Optional(), validators.NumberRange(min=0)],
    # )
    # renda = DecimalField("Renda", validators=[validators.DataRequired()], places=2)
    # crianca_escola = BooleanField("Crianças na Escola")
    # observacoes = StringField("Observações", validators=[validators.Optional()])
