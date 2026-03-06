import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database import db
from flask_security.models import sqla as sqla


class StatusItem(enum.Enum):
    AGUARDA_COLETA = "aguarda_coleta"
    EM_ESTOQUE = "em_estoque"
    ENTREGUE = "entregue"


class TipoImovel(enum.Enum):
    ALUGADO = "alugado"
    PROPRIO = "proprio"


class EstadoCivil(enum.Enum):
    SOLTEIRO = "solteiro"
    CASADO = "casado"
    DIVORCIADO = "divorciado"
    VIUVO = "viuvo"
    UNIAO_ESTAVEL = "uniao_estavel"


class Role(db, sqla.FsRoleMixin):
    __tablename__ = "role"


class User(db, sqla.FsUserMixin):
    __tablename__ = "user"


class ContatoMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)
    endereco: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    telefone: Mapped[str] = mapped_column()


class Instituicao(db, ContatoMixin):
    __tablename__ = "instituicao"

    itens: Mapped[List["Item"]] = relationship(back_populates="instituicao")


class Doador(db, ContatoMixin):
    __tablename__ = "doador"

    itens: Mapped[List["Item"]] = relationship(back_populates="doador")


class Assistido(db, ContatoMixin):
    __tablename__ = "assistido"

    itens: Mapped[List["Item"]] = relationship(back_populates="assistido")
    tipo_imovel: Mapped[TipoImovel] = mapped_column()
    valor_aluguel: Mapped[int] = mapped_column()
    estado_civil: Mapped[EstadoCivil] = mapped_column()
    numero_adultos: Mapped[int] = mapped_column()
    criancas_pequenas: Mapped[int] = mapped_column()
    adolescentes: Mapped[int] = mapped_column()
    doentes: Mapped[bool] = mapped_column()
    bolsa_familia: Mapped[bool] = mapped_column()
    apose: Mapped[bool] = mapped_column()
    pensao: Mapped[bool] = mapped_column()
    cesta_basica: Mapped[bool] = mapped_column()
    atividade_remunerada: Mapped[int] = mapped_column()
    renda: Mapped[float] = mapped_column()
    crianca_escola: Mapped[bool] = mapped_column()
    obs: Mapped[str] = mapped_column()


class CategoriaItem(db):
    __tablename__ = "categoria_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)


class NomeItem(db):
    __tablename__ = "nome_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categoria_item.id"))


class Item(db):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome_id: Mapped[int] = mapped_column(ForeignKey("nome_item.id"))
    coleta_id: Mapped[Optional[int]] = mapped_column(ForeignKey("coleta.id"))
    entrega_id: Mapped[Optional[int]] = mapped_column(ForeignKey("entrega.id"))
    status: Mapped[StatusItem] = mapped_column(default=StatusItem.AGUARDA_COLETA)

    doador_id: Mapped[Optional[int]] = mapped_column(ForeignKey("doador.id"))
    instituicao_id: Mapped[Optional[int]] = mapped_column(ForeignKey("instituicao.id"))
    assistido_id: Mapped[Optional[int]] = mapped_column(ForeignKey("assistido.id"))

    doador: Mapped["Doador"] = relationship(back_populates="itens")
    instituicao: Mapped["Instituicao"] = relationship(back_populates="itens")
    assistido: Mapped["Assistido"] = relationship(back_populates="itens")


class DoacaoMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
    data_hora: Mapped[datetime] = mapped_column()
    instituicao_id: Mapped[int] = mapped_column(ForeignKey("instituicao.id"))
    itens: Mapped[List["Item"]] = relationship()


class Coleta(db, DoacaoMixin):
    __tablename__ = "coleta"

    id: Mapped[int] = mapped_column(primary_key=True)
    data_hora: Mapped[datetime] = mapped_column()
    instituicao_id: Mapped[int] = mapped_column(ForeignKey("instituicao.id"))
    doador_id: Mapped[Optional[int]] = mapped_column(ForeignKey("doador.id"))


class Entrega(db, DoacaoMixin):
    __tablename__ = "entrega"

    id: Mapped[int] = mapped_column(primary_key=True)
    data_hora: Mapped[datetime] = mapped_column()
    instituicao_id: Mapped[int] = mapped_column(ForeignKey("instituicao.id"))
    assistido_id: Mapped[Optional[int]] = mapped_column(ForeignKey("assistido.id"))
