url = "http://192.168.1.76:8000"

function getSelectAutores() {
    $.ajax({
        url: url + "/autores",
        method: "GET",
        success: function (dados) {
            let txt = ''
            
            txt += "<option value = '-1' selected disabled> Escolha uma opção"
            for (let autor of dados){
                txt += `<option value = ${autor.id}> ${autor.nome}</option>`
            }

            $("#autores_dos_livros").html(txt)
        },

        error: function (erro) {
            const msgErro = `Erro ${erro.status}: ${erro.statusText || "Falha ao carregar"}`;
            console.log(msgErro)
        }
    });
}

function getErros(){
    $.ajax({
        url: url + "/livros/" + livroId,
        method: "GET",
        success: function(dados) {
            // Usa os dados normalmente
        },
        error: function(xhr) {
            // 1. Lê o código do erro (ex: 401, 404, 500)
            console.log("Código:", xhr.status);

            // 2. Lê a mensagem do 'detail' que enviaste do Python
            let mensagem = xhr.responseJSON ? xhr.responseJSON.detail : "Erro inesperado no servidor.";
            
            alert(mensagem); // Vai mostrar: "Precisas de iniciar sessão."

            // Se for erro de sessão (401), podes redirecionar logo
            if (xhr.status === 401) {
                window.location.href = "index.html";
            }
        }
    });
}

function teste() {
    isLogado(function(logado) {
        if (logado) {

        } else {

        }
    });
}





function getModal(){

    let txt = ''
    let id = 1

    $.ajax({
        url: url + `/livro_autores/${id}`,
        method: "GET",
        success: function (dados) {
            for(let dado of dados){
                txt += `<li>${dado.autor_nome}</li>`
            }
            Swal.fire({
                title: 'Autores do livro',
                html: txt,
                confirmButtonText: 'Fechar'
            });
        },

        error: function (erro){
            alert('Dados não forma possíveis de carregar')
        }
    })
    
}


$(function(){
    getSelectAutores()
    teste2()
})