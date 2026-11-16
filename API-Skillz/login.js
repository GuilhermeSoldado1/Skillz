let url = "http://192.168.1.76:8000"

function login(){
    let nome = $('#nome').val()
    let password = $('#pass').val()

    $.ajax({
        url: url + `/login/logar`,
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

function isLogado(callback) {
    $.ajax({
        url: url + "/login/is_logado",
        method: "GET",
        success: function(resp) {
            callback(resp);
        }
    });
}

function getTipoUser(){
    $.ajax({
        url: url + `/login/tipo`,
        method: "GET",
        success: function (resp) {
            return resp
        }
    })
}