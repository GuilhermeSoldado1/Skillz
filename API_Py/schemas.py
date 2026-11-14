# Esquemas Pydantic: definem o formato do JSON da API.
# São diferentes do models.py:
#   - models.py  ->  tabela MySQL (SQLAlchemy)
#   - schemas.py ->  dados que entram e saem na API (Pydantic)

from pydantic import BaseModel


# Dados que o cliente envia para criar ou actualizar um livro (JSON de entrada)
class CinemaIn(BaseModel):
    nome: str
    localidade: str
    telefone: int | None = None  # o ano é opcional


# Dados que a API devolve (os mesmos campos + o id gerado pela base de dados)
class CinemaOut(CinemaIn):
    id: int

    # Permite converter um objecto Book (SQLAlchemy) para este modelo Pydantic
    model_config = {"from_attributes": True}


class TetoIn(BaseModel):
    cinema_id: int
    caiu: bool
    # Dados que a API devolve (os mesmos campos + o id gerado pela base de dados)


class TetoOut(TetoIn):
    id: int

    # Permite converter um objecto Book (SQLAlchemy) para este modelo Pydantic
    model_config = {"from_attributes": True}
