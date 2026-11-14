from pydantic import BaseModel

class CampoIn(BaseModel):
    nome: str
    morada: str | None
    cidade: str | None
    capacidade: int | None


class CampoOut(CampoIn):
    id: int

