$(document).ready(function(){
    $('#form_servico').submit(function(event){
        let tipo = $('#tipo').val()
        let valor = $('#valor').val()
        let empresa = $('#empresa').val()
        let categoria = $('#categoria').val()

        if(tipo == ''){
            alert('Campo obrigatório!')
            event.preventDefault();
        }
        
        if(valor == ''){
            alert('Campo obrigatório!')
            event.preventDefault();
        }

        if(empresa == ''){
            alert('Campo obrigatório!')
            event.preventDefault();
        }

        if(categoria == ''){
            alert('Campo obrigatório!')
            event.preventDefault();
        }
    });
});