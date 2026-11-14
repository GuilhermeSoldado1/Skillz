# API REST de cinemas (CRUD).
# CRUD = Create, Read, Update, Delete (criar, ler, actualizar, apagar).
# Sem autenticação / sem API key: qualquer cliente pode chamar os endpoints.

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Cinema, Teto
from schemas import CinemaIn, CinemaOut, TetoIn, TetoOut
from fastapi_offline import FastAPIOffline

# Cria a tabela "cinemas" no MySQL se ainda não existir.
# Não apaga dados: só cria a estrutura em falta.

# Aplicação FastAPI. A documentação automática fica em /docs
app = FastAPIOffline(title="API do shopping")

# CORS: permite que uma página web noutro endereço (ex.: localhost:5500)
# faça pedidos a esta API. Sem isto, o browser bloqueia a comunicação.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # aceita pedidos de qualquer origem (útil em aula)
    allow_credentials=False,    # sem cookies / credenciais (combina com origins="*")
    allow_methods=["*"],        # GET, POST, PUT, DELETE, OPTIONS, ...
    allow_headers=["*"],        # aceita quaisquer cabeçalhos HTTP
)



# GET /cinemas  ->  lista todos os cinemas
@app.get("/cinemas", response_model=list[CinemaOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Cinema).all()


# GET /cinemas/3  ->  devolve o cinema com id 3, ou 404 se não existir
@app.get("/cinemas/{cinema_id}", response_model=CinemaOut)
def obter(cinema_id: int, db: Session = Depends(get_db)):
    cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not cinema:
        raise HTTPException(status_code=404, detail="cinema não encontrado")
    return cinema


# POST /Cinemas  ->  cria um cinema novo e devolve-o com o id (código 201)
@app.post("/cinemas", response_model=CinemaOut, status_code=201)
def criar(dados: CinemaIn, db: Session = Depends(get_db)):
    cinema = Cinema(**dados.model_dump())  # passa o JSON para um objecto Cinema
    db.add(cinema)                       # prepara a inserção
    db.commit()                         # grava na base de dados
    db.refresh(cinema)                   # lê o id gerado pelo MySQL
    return cinema


# PUT /cinemas/3  ->  substitui os dados do cinema 3
@app.put("/cinemas/{cinema_id}", response_model=CinemaOut)
def actualizar(cinema_id: int, dados: CinemaIn, db: Session = Depends(get_db)):
    cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not cinema:
        raise HTTPException(status_code=404, detail="cinema não encontrado")
    cinema.nome = dados.nome
    cinema.localidade = dados.localidade
    cinema.telefone = dados.telefone
    db.commit()
    db.refresh(cinema)
    return cinema

# DELETE /cinemas/3  ->  apaga o cinema 3 (código 204 = sucesso sem conteúdo)

@app.delete("/cinemas/{cinema_id}", status_code=204)
def apagar(cinema_id: int, db: Session = Depends(get_db)):
    cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not cinema:
        raise HTTPException(status_code=404, detail="cinema não encontrado")
    db.delete(cinema)
    db.commit()


#TETOS


# GET /tetos/3  ->  devolve o teto com id 3, ou 404 se não existir
@app.get("/tetos/{teto_id}", response_model=TetoOut)
def obter(teto_id: int, db: Session = Depends(get_db)):
    teto = db.query(Teto).filter(Teto.id == teto_id).first()
    if not teto:
        raise HTTPException(status_code=404, detail="teto não encontrado")
    return teto


# POST /Tetos  ->  cria um teto novo e devolve-o com o id (código 201)
@app.post("/tetos", response_model=TetoOut, status_code=201)
def criar(dados: TetoIn, db: Session = Depends(get_db)):
    teto = Teto(**dados.model_dump())  # passa o JSON para um objecto Teto
    db.add(teto)  # prepara a inserção
    db.commit()  # grava na base de dados
    db.refresh(teto)  # lê o id gerado pelo MySQL
    return teto


# PUT /tetos/3  ->  substitui os dados do teto 3
@app.put("/tetos/{teto_id}", response_model=TetoOut)
def actualizar(teto_id: int, dados: TetoIn, db: Session = Depends(get_db)):
    teto = db.query(Teto).filter(Teto.id == teto_id).first()
    if not teto:
        raise HTTPException(status_code=404, detail="teto não encontrado")
    teto.nome = dados.nome
    teto.localidade = dados.localidade
    teto.telefone = dados.telefone
    db.commit()
    db.refresh(teto)
    return teto


# DELETE /tetos/3  ->  apaga o teto 3 (código 204 = sucesso sem conteúdo)
@app.delete("/tetos/{teto_id}", status_code=204)
def apagar(teto_id: int, db: Session = Depends(get_db)):
    teto = db.query(Teto).filter(Teto.id == teto_id).first()
    if not teto:
        raise HTTPException(status_code=404, detail="teto não encontrado")
    db.delete(teto)
    db.commit()


