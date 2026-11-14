
class LoginIn(BaseModel):
    email: str
    password: str


utilizador_logado = {}



@app.post('/login')
def login(dados: LoginIn):
    global utilizador_logado

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        'select * from utilizador where email = %s and password = %s',
        (dados.email, dados.password)
    )

    utilizador = cursor.fetchone()

    cursor.close()
    conn.close()

    if not utilizador:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    utilizador_logado = utilizador

    return utilizador_logado

# --------------------------------------------------
# 4. VERIFICAÇÃO DE PERMISSÕES
# --------------------------------------------------


@app.get('/utilizadores')
def listar_utilizadores():

    if not utilizador_logado or utilizador_logado['tipo'] != 'admin':
        raise HTTPException(status_code=403, detail="Acesso negado")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('select * from utilizador')
    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados

#Caso não haja tabela geral de utilizadores
@app.post('/login')
def login(dados: LoginIn):
    global utilizador_logado

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Procurar na tabela admin
    cursor.execute(
        'select * from admin where email = %s and password = %s',
        (dados.email, dados.password)
    )
    utilizador = cursor.fetchone()

    if utilizador:
        tipo = 'admin'

    else:
        # Procurar na tabela funcionario
        cursor.execute(
            'select * from funcionario where email = %s and password = %s',
            (dados.email, dados.password)
        )
        utilizador = cursor.fetchone()

        if utilizador:
            tipo = 'funcionario'

        else:
            # Procurar na tabela cliente
            cursor.execute(
                'select * from cliente where email = %s and password = %s',
                (dados.email, dados.password)
            )
            utilizador = cursor.fetchone()

            if utilizador:
                tipo = 'cliente'

    cursor.close()
    conn.close()

    if not utilizador:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Guardar apenas os dados necessários
    utilizador_logado = {
        'id': utilizador['id'],
        'nome': utilizador['nome'],
        'tipo': tipo
    }

    return utilizador_logado