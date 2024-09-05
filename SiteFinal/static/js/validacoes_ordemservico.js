$(document).ready(function(){
    $('#form_ordemservico').submit(function(event){
        let cliente = $('#cliente').val()
        let servico = $('#servico').val()
        let data_inicio = $('#data_inicio').val()
        let data_finalizcao = $('#data_finalizacao').val()
        let status = $('#status').val()

        if(cliente == ''){
            alert('Campo obrigatório!')
            event.preventDefault();
        }

        if(servico == ''){
            alert('Campo obrigatório!')
            event.preventDefault();
        }

        if(data_inicio == ''){
            alert('Campo obrigatório!')
            event.preventDefault();
        }

        if(data_finalizcao == ''){
            alert('Campo obrigatório!')
            event.preventDefault();
        }

        if(status == ''){
            alert('Campo obrigatório!')
            event.preventDefault();
        }
    });
});