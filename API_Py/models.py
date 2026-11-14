# Modelo da tabela "books".
# Aqui descrevemos as colunas. O SQLAlchemy usa isto para criar a tabela
# e para traduzir cada linha da base de dados num objecto Python.

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Cinema(Base):
    # Nome real da tabela no MySQL
    __tablename__ = "cinema"

    # Chave primária: número inteiro gerado automaticamente (1, 2, 3, ...)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Título e autor são obrigatórios (não podem ficar vazios na base de dados)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    localidade: Mapped[str] = mapped_column(String(255), nullable=False)
    telefone: Mapped[int | None] = mapped_column(Integer, nullable=True)

class Teto(Base):
    # Nome real da tabela no MySQL
    __tablename__ = "teto"

    # Chave primária: número inteiro gerado automaticamente (1, 2, 3, ...)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Título e autor são obrigatórios (não podem ficar vazios na base de dados)
    cinema_id: Mapped[int] = mapped_column(Integer, ForeignKey("cinema.id"))
    caiu: Mapped[bool] = mapped_column(Boolean, nullable=False)

    
