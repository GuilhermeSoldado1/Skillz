//Modal do sweetalert que chama uma function
Swal.fire({
  title: 'Título do Modal',
  html: '<p>Conteúdo HTML aqui...</p>',
  showCancelButton: true,
  confirmButtonText: 'Executar Ação',
  cancelButtonText: 'Fechar'
}).then((result) => {
  if (result.isConfirmed) {
    minhaFuncao(); 
  }
});