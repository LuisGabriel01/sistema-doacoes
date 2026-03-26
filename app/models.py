import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, declared_attr
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from flask_security.models import sqla


class StatusItem(enum.Enum):
    AGUARDA_COLETA = "AGUARDA_COLETA"
    EM_ESTOQUE = "EM_ESTOQUE"
    ENTREGUE = "ENTREGUE"


class TipoImovel(enum.Enum):
    ALUGADO = "ALUGADO"
    PROPRIO = "PROPRIO"


class EstadoCivil(enum.Enum):
    SOLTEIRO = "SOLTEIRO"
    CASADO = "CASADO"
    DIVORCIADO = "DIVORCIADO"
    VIUVO = "VIUVO"
    UNIAO_ESTAVEL = "UNIAO_ESTAVEL"


Base = declarative_base()
sqla.FsModels.set_db_info(base_model=Base)


class Role(Base, sqla.FsRoleMixin):
    __tablename__ = "role"


class User(Base, sqla.FsUserMixin):
    __tablename__ = "user"


class ContatoMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)
    endereco: Mapped[str] = mapped_column()
    email: Mapped[Optional[str]] = mapped_column()
    telefone: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"table={self.__class__.__name__}, id={self.id}, nome={self.nome}\n"


class Instituicao(Base, ContatoMixin):
    __tablename__ = "instituicao"

    itens: Mapped[List["Item"]] = relationship(back_populates="instituicao")


class Doador(Base, ContatoMixin):
    __tablename__ = "doador"

    itens: Mapped[List["Item"]] = relationship(back_populates="doador")


class Assistido(Base, ContatoMixin):
    __tablename__ = "assistido"

    itens: Mapped[List["Item"]] = relationship(back_populates="assistido")
    tipo_imovel: Mapped[Optional[TipoImovel]] = mapped_column()
    valor_aluguel: Mapped[Optional[int]] = mapped_column()
    estado_civil: Mapped[Optional[EstadoCivil]] = mapped_column()
    numero_adultos: Mapped[Optional[int]] = mapped_column()
    criancas_pequenas: Mapped[Optional[int]] = mapped_column()
    adolescentes: Mapped[Optional[int]] = mapped_column()
    doentes: Mapped[Optional[bool]] = mapped_column()
    bolsa_familia: Mapped[Optional[bool]] = mapped_column()
    aposentado: Mapped[Optional[bool]] = mapped_column()
    pensao: Mapped[Optional[bool]] = mapped_column()
    cesta_basica: Mapped[Optional[bool]] = mapped_column()
    atividade_remunerada: Mapped[Optional[int]] = mapped_column()
    renda: Mapped[Optional[float]] = mapped_column()
    crianca_escola: Mapped[Optional[bool]] = mapped_column()
    observacoes: Mapped[Optional[str]] = mapped_column()


class CategoriaItem(Base):
    __tablename__ = "categoria_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)


class NomeItem(Base):
    __tablename__ = "nome_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categoria_item.id"))


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome_id: Mapped[int] = mapped_column(ForeignKey("nome_item.id"))
    coleta_id: Mapped[Optional[int]] = mapped_column(ForeignKey("coleta.id"))
    entrega_id: Mapped[Optional[int]] = mapped_column(ForeignKey("entrega.id"))

    doador_id: Mapped[Optional[int]] = mapped_column(ForeignKey("doador.id"))
    instituicao_id: Mapped[Optional[int]] = mapped_column(ForeignKey("instituicao.id"))
    assistido_id: Mapped[Optional[int]] = mapped_column(ForeignKey("assistido.id"))

    doador: Mapped["Doador"] = relationship(back_populates="itens")
    instituicao: Mapped["Instituicao"] = relationship(back_populates="itens")
    assistido: Mapped["Assistido"] = relationship(back_populates="itens")

    status: Mapped[StatusItem] = mapped_column(default=StatusItem.AGUARDA_COLETA)


class DoacaoMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
    data_hora: Mapped[datetime] = mapped_column()
    instituicao_id: Mapped[int] = mapped_column(ForeignKey("instituicao.id"))

    # itens: Mapped[List["Item"]] = relationship()


class Coleta(Base, DoacaoMixin):
    __tablename__ = "coleta"

    doador_id: Mapped[Optional[int]] = mapped_column(ForeignKey("doador.id"))


class Entrega(Base, DoacaoMixin):
    __tablename__ = "entrega"

    assistido_id: Mapped[Optional[int]] = mapped_column(ForeignKey("assistido.id"))
