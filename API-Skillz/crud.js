

function registarDados(){
    let campo1 = $("#campo1").val()
    let campo2 = $("#campo2").val()
    let campo3 = $("#campo3").val()
    let campo4 = $("#campo4").val()

    console.log(campo3)
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

function abrirModal(){
    Swal.fire({
    title: "Are you sure?",
    text: "You won't be able to revert this!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes, delete it!"
    }).then((result) => {
    if (result.isConfirmed){
        console.log('yo!')
    };
    });
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
    isLogado(function(logado) {
        if (!logado) {
            window.location.href = "index.html"
        } 
    });
    renderNavbar()
    getTabela()
    
})