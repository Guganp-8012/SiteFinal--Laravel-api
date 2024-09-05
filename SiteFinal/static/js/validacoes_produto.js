$(document).ready(function(){
    $('#form_produto').submit(function(event){
        let nome = $('#nome').val()
        let valor = $('#valor').val()
        let descricao = $('#descricao').val()

        if(nome == ''){
            alert('Campo obrigatório!')
            event.preventDefault();
        }

        if(valor == ''){
            alert('Campo obrigatório!')
            event.preventDefault();
        }

        if(descricao == ''){
            alert('Campo obrigatório!')
            event.preventDefault();
        }
    });
});