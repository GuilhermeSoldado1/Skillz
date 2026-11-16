const url = "http://172.1.1.68:8000"

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

function login(){
    let nome = $('#nome').val()
    let password = $('#pass').val()

    $.ajax({
        url: url + `/login`,
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ nome, password }),
        success: function (dados) {
            if (dados){
                alert('Bem vindo')
            }
        },

        error: function (erro){
            alert('Dados não foram possíveis de carregar')
        }
    })
}


$(function(){
    getSelectAutores()
})