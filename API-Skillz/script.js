const url = "http://192.168.11.150:8000"

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
            for(let autor of dados){
                txt += `<li>${autor.nome}</li>`
            }
            alert(txt)
        },

        error: function (erro){
            alert('Dados não forma possíveis de carregar')
        }
    })

}


$(function(){
    getSelectAutores()
})