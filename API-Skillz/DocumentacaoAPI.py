from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import get_connection

app = FastAPI(title="Documentação CRUD")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================================
# SCHEMAS (schemas.py)
# Regra: um schema por "forma" de resposta.
#   - XIn  -> o que o cliente ENVIA (sem id)
#   - XOut -> o que a API DEVOLVE (com id e, se for preciso, campos de JOINs)
# Se um campo vem do SELECT mas não está no Out, é descartado em silêncio.
# =====================================================================

class SocioIn(BaseModel):
    nome: str
    cc: int
    numSocio: int
    morada: str
    email: str
    telefone: int
    dataNasc: date
    ativo: int = 1


class SocioOut(SocioIn):
    id: int


# =====================================================================
# PARTE 1 - CRUD COMPLETO (socio)
# Padrão de TODOS os endpoints:
#   1. conn = get_connection(); cursor = conn.cursor(dictionary=True)
#   2. cursor.execute(SQL, (params,))      <- usa sempre %s + tuplo
#   3. fetchall() / fetchone() / commit()  <- leitura vs escrita
#   4. cursor.close(); conn.close()        <- ANTES de qualquer raise
#   5. return
# =====================================================================

# ---- READ (todos) ----------------------------------------------------
@app.get("/socios", response_model=list[SocioOut])
def listar_socios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM socio")
    dados = cursor.fetchall()          # lista de dicionários

    cursor.close()
    conn.close()

    return dados


# ---- READ (um) -------------------------------------------------------
@app.get("/socios/{socio_id}", response_model=SocioOut)
def obter_socio(socio_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM socio WHERE id = %s", (socio_id,))
    dados = cursor.fetchone()          # um dicionário ou None

    cursor.close()
    conn.close()

    if not dados:
        raise HTTPException(status_code=404, detail="Sócio não encontrado")

    return dados


# ---- CREATE ----------------------------------------------------------
@app.post("/socios", response_model=SocioOut, status_code=201)
def criar_socio(dados: SocioIn):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        INSERT INTO socio(nome, cc, numSocio, morada, email, telefone, dataNasc, ativo)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""",
        (dados.nome, dados.cc, dados.numSocio, dados.morada,
         dados.email, dados.telefone, dados.dataNasc, dados.ativo))

    conn.commit()                      # escrita => commit
    novo_id = cursor.lastrowid         # id gerado pelo AUTO_INCREMENT

    cursor.execute("SELECT * FROM socio WHERE id = %s", (novo_id,))
    res = cursor.fetchone()

    cursor.close()
    conn.close()

    return res


# ---- UPDATE ----------------------------------------------------------
@app.put("/socios/{socio_id}", response_model=SocioOut)
def atualizar_socio(socio_id: int, dados: SocioIn):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        UPDATE socio
        SET nome = %s, cc = %s, numSocio = %s, morada = %s,
            email = %s, telefone = %s, dataNasc = %s, ativo = %s
        WHERE id = %s""",
        (dados.nome, dados.cc, dados.numSocio, dados.morada,
         dados.email, dados.telefone, dados.dataNasc, dados.ativo, socio_id))

    conn.commit()

    cursor.execute("SELECT * FROM socio WHERE id = %s", (socio_id,))
    res = cursor.fetchone()

    cursor.close()
    conn.close()

    if not res:
        raise HTTPException(status_code=404, detail="Sócio não encontrado")

    return res


# ---- DELETE ----------------------------------------------------------
@app.delete("/socios/{socio_id}", status_code=204)
def apagar_socio(socio_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id FROM socio WHERE id = %s", (socio_id,))
    existe = cursor.fetchone()

    if not existe:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Sócio não encontrado")

    cursor.execute("DELETE FROM socio WHERE id = %s", (socio_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return None


# =====================================================================
# PARTE 2 - CAMPO QUE SÓ EXISTE COMO FOREIGN KEY (JOIN)
#
# A tabela `requisitacao` só guarda socio_id, livro_id e utilizador_id.
# Para mostrar o NOME do sócio, o TÍTULO do livro, etc., faz-se JOIN
# às tabelas referenciadas e dá-se um alias (AS) a cada coluna nova.
#
# Regras:
#   - O schema Out tem de ter os campos com o nome do ALIAS.
#   - JOIN       -> só devolve linhas onde a FK tem correspondência.
#   - LEFT JOIN  -> devolve sempre a linha base, com None se não houver
#                   correspondência. Usa LEFT JOIN quando a FK pode ser
#                   NULL (como aqui, todas as FKs são "DEFAULT NULL").
#   - Colunas com o mesmo nome em tabelas diferentes (nome, id...) têm
#     SEMPRE de levar alias, senão uma sobrepõe a outra.
# =====================================================================

class RequisitacaoOut(BaseModel):
    id: int
    socio_id: int | None = None
    utilizador_id: int | None = None
    livro_id: int | None = None
    dataRegisto: date | None = None
    dataPrevista: date | None = None
    # campos vindos dos JOINs:
    socio_nome: str | None = None
    utilizador_nome: str | None = None
    livro_titulo: str | None = None


SQL_REQUISITACOES = """
    SELECT r.id, r.socio_id, r.utilizador_id, r.livro_id,
           r.dataRegisto, r.dataPrevista,
           s.nome   AS socio_nome,
           u.nome   AS utilizador_nome,
           l.titulo AS livro_titulo
    FROM requisitacao r
    LEFT JOIN socio s       ON s.id = r.socio_id
    LEFT JOIN utilizador u  ON u.id = r.utilizador_id
    LEFT JOIN livro l       ON l.id = r.livro_id
"""


@app.get("/requisitacoes", response_model=list[RequisitacaoOut])
def listar_requisitacoes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(SQL_REQUISITACOES)
    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


@app.get("/requisitacoes/{requisitacao_id}", response_model=RequisitacaoOut)
def obter_requisitacao(requisitacao_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # o mesmo SELECT + WHERE (a condição vai no fim, depois dos JOINs)
    cursor.execute(SQL_REQUISITACOES + " WHERE r.id = %s", (requisitacao_id,))
    dados = cursor.fetchone()

    cursor.close()
    conn.close()

    if not dados:
        raise HTTPException(status_code=404, detail="Requisitação não encontrada")

    return dados


# =====================================================================
# PARTE 3 - BOTÃO QUE ABRE UMA LISTA ASSOCIADA AO OBJETO
#
# A listagem principal fica leve (sem a lista). Cria-se um endpoint
# aninhado  /<coisa>/{id}/<lista>  que o frontend só chama ao clicar.
#
# Dois casos:
#   A) 1:N  (um sócio tem várias requisitações)
#            -> filtra a tabela "filha" pela FK:  WHERE filha.socio_id = %s
#   B) N:N  (um livro tem vários autores, via autoreslivros)
#            -> JOIN pela tabela de ligação e filtra pelo id do livro
#
# Se não houver nada associado, devolve [] (não é erro).
# =====================================================================

class AutorOut(BaseModel):
    id: int
    nome: str
    dataNasc: date
    biografia: str
    outrasInformacoes: str
    facebook: str | None = None
    instagram: str | None = None
    x: str | None = None


class RequisitacaoDoSocioOut(BaseModel):
    id: int
    livro_id: int | None = None
    livro_titulo: str | None = None
    dataRegisto: date | None = None
    dataPrevista: date | None = None


# ---- A) 1:N  ->  requisitações de um sócio ---------------------------
@app.get("/socios/{socio_id}/requisitacoes", response_model=list[RequisitacaoDoSocioOut])
def requisitacoes_do_socio(socio_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT r.id, r.livro_id, l.titulo AS livro_titulo,
               r.dataRegisto, r.dataPrevista
        FROM requisitacao r
        LEFT JOIN livro l ON l.id = r.livro_id
        WHERE r.socio_id = %s""", (socio_id,))

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


# ---- B) N:N  ->  autores de um livro (tabela de ligação) -------------
@app.get("/livros/{livro_id}/autores", response_model=list[AutorOut])
def autores_do_livro(livro_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT a.*
        FROM autor a
        JOIN autoreslivros al ON al.autor_id = a.id
        WHERE al.livro_id = %s""", (livro_id,))

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados

