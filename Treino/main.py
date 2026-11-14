
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database import get_connection
from schemas import *


app = FastAPI(title="API Teste")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 1. LISTAR TODOS (READ)
@app.get("/campos", response_model=list[CampoOut])
def listar():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM campo")

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


# 2. OBTER APENAS UM (READ BY ID)
@app.get("/campos/{campo_id}", response_model=CampoOut)
def obter(campo_id: int):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f"SELECT * FROM campo WHERE id = {campo_id}")

    dados = cursor.fetchone()

    cursor.close()
    conn.close()

    if not dados:
        raise HTTPException(status_code=404, detail="Campo não encontrado")

    return dados


# 3. CRIAR (CREATE)
@app.post("/campos", response_model=CampoOut, status_code=201)
def criar(dados: CampoIn):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f"""
        INSERT INTO campo (nome, morada, cidade, capacidade)
        VALUES ('{dados.nome}', '{dados.morada}', '{dados.cidade}', {dados.capacidade})
    """)

    conn.commit()

    novo_id = cursor.lastrowid

    cursor.execute(f"SELECT * FROM campo WHERE id = {novo_id}")

    novo_campo = cursor.fetchone()

    cursor.close()
    conn.close()

    return novo_campo


# 4. ATUALIZAR (UPDATE)
@app.put("/campos/{campo_id}", response_model=CampoOut)
def actualizar(campo_id: int, dados: CampoIn):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f"SELECT * FROM campo WHERE id = {campo_id}")

    existente = cursor.fetchone()

    if not existente:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Campo não encontrado")

    cursor.execute(f"""
        UPDATE campo
        SET nome = '{dados.nome}',
            morada = '{dados.morada}',
            cidade = '{dados.cidade}',
            capacidade = {dados.capacidade}
        WHERE id = {campo_id}
    """)

    conn.commit()

    cursor.execute(f"SELECT * FROM campo WHERE id = {campo_id}")

    dados = cursor.fetchone()

    cursor.close()
    conn.close()

    return dados


# 5. APAGAR (DELETE)
@app.delete("/campos/{campo_id}", status_code=204)
def apagar(campo_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT id FROM campo WHERE id = {campo_id}")

    dados = cursor.fetchone()

    if not dados:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Campo não encontrado")

    cursor.execute(f"DELETE FROM campo WHERE id = {campo_id}")

    conn.commit()

    cursor.close()
    conn.close()

    return None
