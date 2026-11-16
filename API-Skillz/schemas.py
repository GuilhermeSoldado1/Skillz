from pydantic import BaseModel
from datetime import *


class LivroIn(BaseModel):
    titulo: str
    dataLancamento: date
    sinopse: str
    edicao: str
    editora: str
    genero: str
    categoria: str
    idioma: str
    numPaginas: int
    isbn: str
    estado: int
    qtd: int
    autor_id: int

class LivroOut(LivroIn):
    id: int

class Livro_AutoresOut(BaseModel):
    autor_nome: str
    livro_titulo: str



class AutorIn(BaseModel):
    nome: str
    dataNasc: date
    biografia: str
    outrasInformacoes: str
    facebook: str
    instagram: str
    x: str

class AutorOut(AutorIn):
    id: int


class SocioIn(BaseModel):
    nome: str
    cc: int
    numSocio: int
    morada: str
    email: str
    telefone: int
    dataNasc: date
    ativo: int

class SocioOut(SocioIn):
    id: int



class UtilizadorIn(BaseModel):
    nome: str
    morada: str
    telefone: str
    email: str
    numFunc: int
    dataNasc: date
    tipo: str


class UtilizadorOut(UtilizadorIn):
    id: int


class RequisitacaoIn(BaseModel):
    socio_id: int
    utilizador_id: int
    livro_id: int
    dataRegisto: date
    dataPrevista: date

class RequisitacaoOut(RequisitacaoIn):
    id: int
    socio_nome: str
    utilizador_nome: str
    livro_titulo: str