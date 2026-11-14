from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fastapi.exceptions import ResponseValidationError, RequestValidationError
from fastapi.responses import JSONResponse

from schemas import LivroIn
from database import get_connection
from schemas import *

app = FastAPI(title="API Módulo 3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Erros de validação dos dados recebidos pela API (POST, PUT, etc.)
@app.exception_handler(RequestValidationError)
async def erro_validacao_request(request, exc):
    erros = []

    for erro in exc.errors():
        campo = erro['loc'][-1]
        mensagem = erro['msg']

        erros.append(f"{campo}: {mensagem}")

    return JSONResponse(
        status_code=422,
        content={
            "erro": "Dados inválidos",
            "detalhes": erros
        }
    )

# Erros de validação dos dados devolvidos pela API (response_model)
@app.exception_handler(ResponseValidationError)
async def erro_validacao_response(request, exc):
    erros = []

    for erro in exc.errors():
        campo = erro['loc'][-1]
        mensagem = erro['msg']

        erros.append(f"{campo}: {mensagem}")

    return JSONResponse(
        status_code=500,
        content={
            "erro": "Erro na resposta da API",
            "detalhes": erros
        }
    )

#CRUD - LIVROS

@app.get("/livros", response_model=list[LivroOut])
def listar_livros():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('SELECT * FROM livro')

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados

@app.get('/livros/{livro_id}', response_model=LivroOut)
def obter_livro(livro_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f'SELECT * FROM livro WHERE id = {livro_id}')

    dados = cursor.fetchone()

    cursor.close()
    conn.close()

    if not dados:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    return dados

@app.post('/livros', response_model=LivroOut, status_code=201)
def post_livro(dados: LivroIn):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
    INSERT INTO livro(titulo, dataLancamento, sinopse, edicao, editora, genero, categoria, idioma, numPaginas, isbn, estado, qtd) 
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
    (dados.titulo, dados.dataLancamento, dados.sinopse, dados.edicao, dados.editora, dados.genero, dados.categoria, dados.idioma, dados.numPaginas, dados.isbn, dados.estado, dados.qtd))

    livro_id = cursor.lastrowid
    cursor.execute(f'insert into autoreslivros(autor_id, livro_id) values(%s, %s)', (dados.autor_id, livro_id))

    conn.commit()

    cursor.execute("""
    select livro.*, autor.nome
    from livro, autor, autoreslivros
    where livro.id = autoreslivros.livro_id and autor.id = autoreslivros.autor_id and
    livro.id = %s """, (livro_id,))

    res = cursor.fetchone()

    cursor.close()
    conn.close()

    return res

@app.put('/livros/{livro_id}', response_model=LivroOut)
def atualizar_livro(livro_id: int, dados: LivroIn):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    update livro set titulo = %s, dataLancamento = %s, sinopse = %s, edicao = %s, editora = %s, genero = %s, categoria = %s, idioma = %s, numPaginas = %s, isbn = %s, estado = %s, qtd = %s
    where id = %s""",
    (dados.titulo, dados.dataLancamento, dados.sinopse, dados.edicao, dados.editora, dados.genero, dados.categoria, dados.idioma, dados.numPaginas, dados.isbn, dados.estado, dados.qtd, livro_id))

    conn.commit()

    cursor.execute(f'select * from livro where id = {livro_id}')

    res = cursor.fetchone()

    cursor.close()
    conn.close()

    return res

@app.delete('/livros/{livro_id}', status_code=204)
def apagar_livro(livro_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f'select id from livro where id = {livro_id}')

    dados = cursor.fetchone()

    if not dados:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    cursor.execute(f'delete from livro where id = {livro_id}')

    conn.commit()

    cursor.close()
    conn.close()

    return None


# CRUD AUTORES

@app.get("/autores", response_model=list[AutorOut])
def listar_autores():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('SELECT * FROM autor')

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados

@app.get('/autores/{autor_id}', response_model=AutorOut)
def obter_livro(autor_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f'SELECT * FROM autor WHERE id = {autor_id}')

    dados = cursor.fetchone()

    cursor.close()
    conn.close()

    if not dados:
        raise HTTPException(status_code=404, detail="Autor não encontrado")

    return dados

@app.post('/autores', response_model=AutorOut, status_code=201)
def post_autor(dados: AutorIn):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
    INSERT INTO autor(nome, dataNasc, biografia, outrasInformacoes, facebook, instagram, x) 
    VALUES(%s, %s, %s, %s, %s, %s, %s)''',
    (dados.nome, dados.dataNasc, dados.biografia, dados.outrasInformacoes, dados.facebook, dados.instagram, dados.x))

    conn.commit()

    novo_id = cursor.lastrowid
    cursor.execute(f'SELECT * FROM autor WHERE id = {novo_id}')

    res = cursor.fetchone()

    cursor.close()
    conn.close()

    return res

@app.put('/autores/{autor_id}', response_model=AutorOut)
def atualizar_autor(autor_id: int, dados: AutorIn):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    update autor set nome = %s, dataNasc = %s, biografia = %s, outrasInformacoes = %s, facebook = %s, instagram = %s, x = %s
    where id = %s""",
    (dados.nome, dados.dataNasc, dados.biografia, dados.outrasInformacoes, dados.facebook, dados.instagram, dados.x, autor_id))

    conn.commit()

    cursor.execute(f'select * from autor where id = {autor_id}')

    res = cursor.fetchone()

    cursor.close()
    conn.close()

    return res

@app.delete('/autores/{autor_id}', status_code=204)
def apagar_livro(autor_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f'select id from autor where id = {autor_id}')

    dados = cursor.fetchone()

    if not dados:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Autor não encontrado")

    cursor.execute(f'delete from autor where id = {autor_id}')

    conn.commit()

    cursor.close()
    conn.close()

    return None


# CRUD SOCIOS

@app.get("/socios", response_model=list[SocioOut])
def listar_socios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('SELECT * FROM socio')

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados

@app.get('/socios/{socio_id}', response_model=SocioOut)
def obter_socio(socio_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f'SELECT * FROM socio WHERE id = {socio_id}')

    dados = cursor.fetchone()

    cursor.close()
    conn.close()

    if not dados:
        raise HTTPException(status_code=404, detail="Sócio não encontrado")

    return dados

@app.post('/socios', response_model=SocioOut, status_code=201)
def post_autor(dados: SocioIn):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
    INSERT INTO socio(nome, cc, numSocio, morada, email, telefone, dataNasc, ativo) 
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)''',
    (dados.nome, dados.cc, dados.numSocio, dados.morada, dados.email, dados.telefone, dados.dataNasc, dados.ativo))

    conn.commit()

    novo_id = cursor.lastrowid
    cursor.execute(f'SELECT * FROM socio WHERE id = {novo_id}')

    res = cursor.fetchone()

    cursor.close()
    conn.close()

    return res

@app.put('/socios/{socio_id}', response_model=SocioOut)
def atualizar_autor(socio_id: int, dados: SocioIn):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    update socio set nome = %s, cc = %s, numSocio = %s, morada = %s, email = %s, telefone = %s, dataNasc = %s, ativo = %s
    where id = %s""",
    (dados.nome, dados.cc, dados.numSocio, dados.morada, dados.email, dados.telefone, dados.dataNasc, dados.ativo, socio_id))

    conn.commit()

    cursor.execute(f'select * from socio where id = {socio_id}')

    res = cursor.fetchone()

    cursor.close()
    conn.close()

    return res

@app.delete('/socios/{socio_id}', status_code=204)
def apagar_livro(socio_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f'select id from socio where id = {socio_id}')

    dados = cursor.fetchone()

    if not dados:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Sócio não encontrado")

    cursor.execute(f'delete from socio where id = {socio_id}')

    conn.commit()

    cursor.close()
    conn.close()

    return None


# CRUD - UTILIZADORES

@app.get('/utilizadores', response_model=list[UtilizadorOut])
def listar_utilizadores():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('select * from utilizador')
    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados

@app.get('/utilizadores/{utilizador_id}', response_model=UtilizadorOut)
def obter_utilizador(utilizador_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('select * from utilizador where id = %s', (utilizador_id,))
    dados = cursor.fetchone()

    cursor.close()
    conn.close()

    if not dados:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")

    return dados

@app.post('/utilizadores', response_model=UtilizadorOut, status_code=201)
def post_utilizador(dados: UtilizadorIn):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        insert into utilizador(nome, morada, telefone, email, numFunc, dataNasc, tipo)
        values(%s, %s, %s, %s, %s, %s, %s)
    """, (dados.nome, dados.morada, dados.telefone, dados.email,
          dados.numFunc, dados.dataNasc, dados.tipo))

    utilizador_id = cursor.lastrowid

    conn.commit()

    cursor.execute('select * from utilizador where id = %s', (utilizador_id,))
    res = cursor.fetchone()

    cursor.close()
    conn.close()

    return res


@app.put('/utilizadores/{utilizador_id}', response_model=UtilizadorOut)
def atualizar_utilizador(utilizador_id: int, dados: UtilizadorIn):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        update utilizador set nome = %s, morada = %s, telefone = %s,
        email = %s, numFunc = %s, dataNasc = %s, tipo = %s
        where id = %s
    """, (dados.nome, dados.morada, dados.telefone, dados.email,
          dados.numFunc, dados.dataNasc, dados.tipo, utilizador_id))

    conn.commit()

    cursor.execute('select * from utilizador where id = %s', (utilizador_id,))
    res = cursor.fetchone()

    cursor.close()
    conn.close()

    if not res:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")

    return res


@app.delete('/utilizadores/{utilizador_id}', status_code=204)
def apagar_utilizador(utilizador_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('select id from utilizador where id = %s', (utilizador_id,))
    dados = cursor.fetchone()

    if not dados:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")

    cursor.execute('delete from utilizador where id = %s', (utilizador_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return None


# CRUD - REQUISITACAO

@app.get('/requisitacoes', response_model=list[RequisitacaoOut])
def listar_requisitacoes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""select requisitacao.*, socio.nome as socio_nome, utilizador.nome as utilizador_nome, livro.titulo as livro_titulo 
                      from requisitacao, socio, utilizador, livro
                    where requisitacao.socio_id = socio.id
                   and requisitacao.utilizador_id = utilizador.id
                   and requisitacao.livro_id = livro.id""")
    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados

@app.get('/requisitacoes/{requisitacao_id}', response_model=RequisitacaoOut)
def obter_requisitacao(requisitacao_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""select requisitacao.*, socio.nome as socio_nome, utilizador.nome as utilizador_nome, livro.titulo as livro_titulo 
                      from requisitacao, socio, utilizador, livro
                    where requisitacao.socio_id = socio.id
                   and requisitacao.utilizador_id = utilizador.id
                   and requisitacao.livro_id = livro.id
                   and requisitacao.id = %s""", (requisitacao_id,))
    dados = cursor.fetchone()

    cursor.close()
    conn.close()

    if not dados:
        raise HTTPException(status_code=404, detail="Requisitação não encontrado")

    return dados

@app.post('/requisitacoes', response_model=RequisitacaoOut, status_code=201)
def post_requisitacao(dados: RequisitacaoIn):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        insert into requisitacao(socio_id, utilizador_id, livro_id, dataRegisto, dataPrevista)
        values(%s, %s, %s, NOW(), %s)
    """, (dados.socio_id, dados.utilizador_id, dados.livro_id, dados.dataPrevista))

    requisitacao_id = cursor.lastrowid

    conn.commit()

    cursor.execute("""select requisitacao.*,
                             socio.nome      as socio_nome,
                             utilizador.nome as utilizador_nome,
                             livro.titulo    as livro_titulo
                      from requisitacao,
                           socio,
                           utilizador,
                           livro
                      where requisitacao.socio_id = socio.id
                        and requisitacao.utilizador_id = utilizador.id
                        and requisitacao.livro_id = livro.id
                        and requisitacao.id = %s""", (requisitacao_id,))
    res = cursor.fetchone()

    cursor.close()
    conn.close()

    return res


@app.put('/requisitacoes/{requisitacao_id}', response_model=RequisitacaoOut)
def atualizar_requisitacao(requisitacao_id: int, dados: RequisitacaoIn):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        update requisitacao set socio_id = %s, utilizador_id = %s, livro_id = %s, dataRegisto = %s, dataPrevista = %s
        where id = %s """, (dados.socio_id, dados.utilizador_id, dados.livro_id, dados.dataRegisto, dados.dataPrevista, requisitacao_id))

    conn.commit()

    cursor.execute("""select requisitacao.*,
                             socio.nome      as socio_nome,
                             utilizador.nome as utilizador_nome,
                             livro.titulo    as livro_titulo
                      from requisitacao,
                           socio,
                           utilizador,
                           livro
                      where requisitacao.socio_id = socio.id
                        and requisitacao.utilizador_id = utilizador.id
                        and requisitacao.livro_id = livro.id
                        and requisitacao.id = %s""", (requisitacao_id,))
    res = cursor.fetchone()

    cursor.close()
    conn.close()

    if not res:
        raise HTTPException(status_code=404, detail="Requisitação não encontrado")

    return res


@app.delete('/requisitacoes/{requisitacao_id}', status_code=204)
def apagar_requisitacao(requisitacao_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('select id from requisitacao where id = %s', (requisitacao_id,))
    dados = cursor.fetchone()

    if not dados:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Requisitação não encontrado")

    cursor.execute('delete from requisitacao where id = %s', (requisitacao_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return None



