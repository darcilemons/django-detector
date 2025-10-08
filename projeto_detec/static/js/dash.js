window.onload = function(event){
        renderiza_total_geral(TOTAL_RELATOS_URL); // sempre que a tela carregar chama a função e o URL = name da view
    }
    function renderiza_total_geral(url){
        fetch(url, { // faz uma requisição para uma URL
            method: 'get', //método da requisição
        }).then(function(result){ // funciona através de promises, após receber a requisição faz algo com 'then'
            return result.json()
        }).then(function(data){
            document.getElementById('total_geral').innerHTML = data.total
        })
    }