const url = 'url'

function registarDados(){
    let campo1 = $("#campo1").val()
    let campo2 = $("#campo2").val()
    let campo3 = $("#campo3").val()
    let campo4 = $("#campo4").val()

    $.ajax({
        url: url + '/campo',
        method: 'POST',
        contentType: "application/json",
        data: JSON.stringify({ campo1, campo2, campo3, campo4 }),

        success: function(dados){
            alert('Sucesso')
            $("#formCreate")[0].reset()
            getTabela()
        },

        error: function (erro){
            alert('Não foi possível registar')
        }
    })
}

function getTabela(){
    $.ajax({
        url: url + '/campo',
        method: 'GET',

        success: function(dados){
            let txt = ''

            for(let dado of dados){
                txt += `<tr>
                        <td>${dado.id}</td>
                        <td>
                            <button type="button" class="btn btn-success btn-sm" onclick="editarCampo()">Editar</button>
                            <button type="button" class="btn btn-danger btn-sm" onclick="removerCampo()">Remover</button>
                        </td>
                        </tr>`
            }

            $("#tabelaCorpo").html(txt)
        },

        error: function (erro){
            alert('Dados não foram possíveis de carregar')
        }
    })
}

function editarCampo(id){

    $.ajax({
        url: url + `/campo/${id}`,
        method: 'GET',

        success: function(dado){

            Swal.fire({
                title: 'Editar',
                html: `
                    <input id="campo1_edit" class="swal2-input" placeholder="campo1" value=""
                `,
                didOpen: () => {
                    $("#campo3_edit").val(dado.campo3)
                },
                showCancelButton: true,
                confirmButtonText: 'Guardar',
                preConfirm: () => {
                    return {
                        campo1: $("#campo1_edit").val()
                    }
                }
            }).then(r => {
                if(r.isConfirmed){
                    guardarEdicao(id, r.value)
                }
            })
        },

        error: function (erro){
            alert('Dados não foram possíveis de carregar')
        }
    })
}

function guardarEdicao(id, campos){
    $.ajax({
        url: url + `/campo/${id}`,
        method: 'PUT',
        contentType: "application/json",
        data: JSON.stringify(campos),

        success: function(dados){
            alert('Sucesso')
            getTabela()
        },

        error: function (erro){
            alert('Não foi possível editar')
        }
    })
}


$(function () {
    renderNavbar()
    getTabela()

    $("#formCreate").on("submit", function(e){
        e.preventDefault()
        registarDados()
    })
})