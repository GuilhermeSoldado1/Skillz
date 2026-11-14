// Estrutura do Modal

function verLivro(id) {

    const url = getBaseUrl();
    if (!url) {alert("Defina a Base URL primeiro."); return }
    
    $('#bookId').val(id);

    $.ajax({
        url: `${url}/books/${id}`,
        method: "GET",
        contentType: "application/json",
        data: id
    })

  .done(function(dados) {
    $('#inputTitle').val(dados.title)
    $('#inputAuthor').val(dados.author)
    $('#inputYear').val(dados.year)

  })

  .fail(handleAjaxError);

    const modalElement = document.getElementById('bookModal');
    const bookModalInstance = bootstrap.Modal.getOrCreateInstance(modalElement);
    bookModalInstance.show();
}

function atualizarLivro() {
    const base = getBaseUrl();

    if (!base) { 
        alert("Defina a Base URL primeiro."); 
        return; 
    }

    const id = $('#bookId').val();
    const title = $('#inputTitle').val();
    const year = $('#inputYear').val();
    const author = $('#inputAuthor').val();

    $.ajax({
        url: `${base}/books/${id}`,
        method: "PUT",
        contentType: "application/json",
        data: JSON.stringify({ title, author, year })
    })
    .done(function() {
        alert("Livro atualizado com sucesso!");
        
        const modalElement = document.getElementById('bookModal');
        const bookModalInstance = bootstrap.Modal.getInstance(modalElement);
        bookModalInstance.hide();

        listarLivros();
    })
    .fail(handleAjaxError);
}

let txt = 
    `<div class="modal fade" id="bookModal" tabindex="-1" aria-labelledby="bookModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title" id="bookModalLabel">Ver Livro</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
        </div>
        <div class="modal-body">
            <form id="bookForm">

            <input type="hidden" id="bookId" name="bookId">

            <div class="mb-3">
                <label for="inputTitle" class="form-label">Título</label>
                <input type="text" class="form-label form-control" id="inputTitle" value="">
            </div>
            <div class="mb-3">
                <label for="inputYear" class="form-label">Ano</label>
                <input type="number" class="form-control" id="inputYear" value="">
            </div>
            <div class="mb-3">
                <label for="inputAuthor" class="form-label">Autor</label>
                <input type="text" class="form-control" id="inputAuthor" value="">
            </div>
            </form>
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" onclick = "atualizarLivro()">Guardar</button>
        </div>
        </div>
    </div>
    </div> `


// GET SINGLE SE PRECISAR

function getCinema(){
    const id = $('#id').val().trim();

    const base = getBaseUrl();
    if (!base) {alert("Defina a Base URL primeiro."); return }

    $.ajax({
        url: `${base}/cinemas/${id}`,
        method: "GET",
        dataType: "json"
    })

    .done(function(dados) {
        let txt = ''

        txt += `<ul>
                    <li>Nome: ${dados.nome}</li>
                    <li>Localidade: ${dados.localidade}</li>
                    <li>Telefone: ${dados.telefone}</li>
                </ul>`
        $('#getCinema').html(txt);
    })

  .fail(function(xhr) {
        if (xhr.status === 404 || xhr.status === 422) {
            $('#getCinema').html(`
                <ul>
                    <li colspan="5" style="text-align: center; color: #666; padding: 20px;">
                        Nenhum resultado encontrado
                    </li>
                </ul>
            `);
        } else {
            handleAjaxError(xhr);
        }
    });
}