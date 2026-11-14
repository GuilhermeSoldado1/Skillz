const API_KEY = "ab1453#=";

// ---------- Base URL (guardada no localStorage) ----------
(function initBaseUrl() {
  const stored = localStorage.getItem("BASE_URL");
  if (stored) $("#baseUrl").val(stored);
})();

function getBaseUrl() {
  // Normaliza e remove barra extra no fim
  return ($("#baseUrl").val() || "")
    .trim()
    .replace(/\/+$/, "");
}

function guardarBase() {
  const url = getBaseUrl();
  if (!url) { alert("Indica uma Base URL válida."); return; }
  localStorage.setItem("BASE_URL", url);
  alert("Base URL guardada!");
  listarClientes(); // refresca já com a nova base
}

// ---------- Enviar X-API-Key em TODAS as requests ----------
$.ajaxSetup({
  beforeSend: function (xhr) {
    if (API_KEY) {
      xhr.setRequestHeader("X-API-Key", API_KEY);
    }
  }
});

function handleAjaxError(jqXHR) {
  // Tratamento específico para auth
  if (jqXHR.status === 401) { alert("API Key em falta."); return; }
  if (jqXHR.status === 403) { alert("API Key inválida ou inativa."); return; }

  // Tenta extrair mensagem legível do JSON de erro
  let msg = "Erro de comunicação";
  try {
    const json = JSON.parse(jqXHR.responseText);
    msg = json.error || json.message || msg;
  } catch(e) {
    // se não for JSON, tenta usar statusText
    msg = jqXHR.statusText || msg;
  }
  alert(msg);
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
}

// ---------- CRUD ----------

// POST /clientes
function criarCinema() {
    const base = getBaseUrl();
    if (!base) {alert("Defina a Base URL primeiro."); return }

    const nome = $("#nome").val().trim();
    const localidade = $("#localidade").val().trim();
    const telefone = $("#telefone").val().trim();

    if (!nome || !localidade) {
        alert("Preenche nome e localidade.");
        return;
    }

    $.ajax({
        url: `${base}/cinemas`,
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ nome, localidade, telefone })
    })

  .done(function() {
    alert("Cinema criado!");
    // limpa inputs e recarrega a lista
    $("#nome, #localidade, #telefone").val("");
    listarCinemas();
  })

  .fail(handleAjaxError);
}

// GET /clientes

function listarCinemas(){
    const base = getBaseUrl();
    if (!base) {alert("Defina a Base URL primeiro."); return }

    let tr = ''

    const pesquisa = $('#search').val().trim();
    const url = pesquisa ? `${base}/cinemas/${pesquisa}` : `${base}/cinemas`;

    $.ajax({
        url: url,
        method: "GET",
        dataType: "json"
    })

    .done(function(dados) {

      const lista = Array.isArray(dados) ? dados : [dados];

        for (let cinema of lista) {
            tr += `
                <tr>
                    <td>${cinema.id}</td>
                    <td><input id="nome_${cinema.id}" value="${escapeHtml(cinema.nome || "")}" /></td>
                    <td><input id="localidade_${cinema.id}" value="${escapeHtml(cinema.localidade || "")}" /></td>
                    <td><input id="tel_${cinema.id}" value="${escapeHtml(cinema.telefone || "")}" /></td>
                    <td>
                        <button class="primary" onclick="atualizarCinema(${cinema.id})">Guardar</button>
                        <button class="danger" onclick="apagarCinema(${cinema.id})">Apagar</button>
                    </td>
                </tr>
            `;

            $('#tabelaCinemas tbody').html(tr)
        };
    })

    .fail(function(xhr) {
        if (xhr.status === 404 || xhr.status === 422) {
            $('#tabelaCinemas tbody').html(`
                <tr>
                    <td colspan="5" style="text-align: center; color: #666; padding: 20px;">
                        Nenhum resultado encontrado
                    </td>
                </tr>
            `);
        } else {
            handleAjaxError(xhr);
        }
    });
}

function atualizarCinema(id){
    const base = getBaseUrl();
    if (!base) {alert("Defina a Base URL primeiro."); return }

    const nome = $(`#nome_${id}`).val().trim();
    const localidade = $(`#localidade_${id}`).val().trim();
    const telefone = $(`#tel_${id}`).val().trim();

    $.ajax({
        url: `${base}/cinemas/${id}`,
        method: "PUT",
        contentType: "application/json",
        data: JSON.stringify({ nome, localidade, telefone })
    })

    .done(function() {
        alert("Cinema atualizado!");
        listarCinemas();
    })

    .fail(handleAjaxError);
}

function apagarCinema(id){
    const base = getBaseUrl();
    if (!base) {alert("Defina a Base URL primeiro."); return }

    $.ajax({
        url: `${base}/cinemas/${id}`,
        method: "DELETE",
    })

    .done(function() {
        alert("Cinema eliminado!");
        listarCinemas();
    })

    .fail(handleAjaxError);
}

// ---------- Arranque ----------
$(function() {
  // carrega a lista ao abrir a página
  listarCinemas();
  // permitir Enter no campo de pesquisa
  $("#search").on("keydown", function(e) {
    if (e.key === "Enter") listarCinemas();
  });
});

