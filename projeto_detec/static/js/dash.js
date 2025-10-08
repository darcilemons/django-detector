function gera_cor(qtd=1){
    var bg_color = []
    var border_color = []
    for(let i = 0; i < qtd; i++){
        let r = Math.random() * 255;
        let g = Math.random() * 255;
        let b = Math.random() * 255;
        bg_color.push(`rgba(${r}, ${g}, ${b}, ${0.2})`)
        border_color.push(`rgba(${r}, ${g}, ${b}, ${1})`)
    }

    return [bg_color, border_color];
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

function renderiza_relatos_anual(url){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){

        const ctx = document.getElementById('relatos_anual').getContext('2d');
        var cores_relato_anual = gera_cor(qtd=12)
        const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: "Relatos",
                    data: data.data,
                    backgroundColor: cores_relato_anual[0],
                    borderColor: cores_relato_anual[1],
                    borderWidth: 0.2,
                    fill: {
                        below: cores_relato_anual[0]
                    }
                }]
            }
        })
    })
}

function renderiza_relatos_cond(url){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){

        const ctx = document.getElementById('relatos_cond').getContext('2d');
        var cores_relatos_cond = gera_cor(qtd=12)
        const myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    label: "Condomínios | Relatos",
                    data: data.data,
                    backgroundColor: cores_relatos_cond[0],
                    borderColor: cores_relatos_cond[1],
                    borderWidth: 1
                }]
            }
        })
    })
}

function renderiza_relatos_por_cat_ayel(url){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){

        const ctx = document.getElementById('relato_cat_ayel').getContext('2d');
        var cores_relatos_por_cat_ayel = gera_cor(qtd=12)
        const myChart = new Chart(ctx, {
            type: 'polarArea',
            data: {
                labels: data.ayel_labels,
                datasets: [{
                    label: "APP Ayel",
                    data: data.ayel_data,
                    backgroundColor: cores_relatos_por_cat_ayel[0],
                    borderColor: cores_relatos_por_cat_ayel[1],
                    borderWidth: 1
                }]
            }
        })
    })
}

function renderiza_relatos_por_cat_cam(url){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){

        const ctx = document.getElementById('relato_cat_cam').getContext('2d');
        var cores_relatos_por_cat_cam = gera_cor(qtd=12)
        const myChart = new Chart(ctx, {
            type: 'polarArea',
            data: {
                labels: data.cam_labels,
                datasets: [{
                    label: "APP Ayel",
                    data: data.cam_data,
                    backgroundColor: cores_relatos_por_cat_cam[0],
                    borderColor: cores_relatos_por_cat_cam[1],
                    borderWidth: 1
                }]
            }
        })
    })
}