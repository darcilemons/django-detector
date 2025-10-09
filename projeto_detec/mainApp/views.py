from django.shortcuts import render, redirect, get_object_or_404
from .forms import condsForm, FacialForm, DVRForm, OutroForm, RelatoForm
from django.contrib import messages
from .models import Conds, Itens_dvr, Itens_facial, Itens_outro, TipoRelato, CategoriaRelatoAyel, CategoriaRelatoCam, Relatos
from django.db.models import Count, Q
from django.http.response import Http404, HttpResponse
from django.http import JsonResponse
from django.db.models import Count
from django.views.generic import TemplateView
from datetime import datetime, timedelta
from django.utils import timezone

def home(request):
    return render(request, 'home.html')

def cad_cond(request):
    if request.method == 'POST':
        form = condsForm(request.POST)
        if form.is_valid():
            condominio = form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('listar_conds')
    else:
        form = condsForm()
    
    return render(request, 'conds_cad.html', {'form': form})

def home_equip(request):
    conds = Conds.objects.all()
    return render(request, 'home_equip.html', {'conds': conds})

def equip(request, condominio_id):
    condominio = get_object_or_404(Conds, id=condominio_id)
    
    if request.method == 'POST':
        tipo_equipamento = request.POST.get('tipo_equipamento')
        return redirect('cad_equip', condominio_id=condominio.id, tipo=tipo_equipamento)
    
    return render(request, 'equip.html', {'condominio': condominio})

def cad_equip(request, condominio_id, tipo):
    condominio = get_object_or_404(Conds, id=condominio_id)
    
    if tipo == 'FACIAL':
        form_class = FacialForm
        template = 'equip-forms/cad_facial.html'
    elif tipo == 'DVR':
        form_class = DVRForm
        template = 'equip-forms/cad_dvr.html'
    elif tipo == 'OUTRO':
        form_class = OutroForm
        template = 'equip-forms/cad_outro.html'
    else:
        return redirect('cad_equip', condominio_id=condominio_id)
    
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            equipamento = form.save(commit=False)
            equipamento.cond_id = condominio
            equipamento.save()
            messages.success(request, 'Equipamento cadastrado!')
            return redirect('home_equip')
    else:
        form = form_class()
    
    return render(request, template, {
        'form': form,
        'condominio': condominio,
        'tipo_equipamento': tipo
    })

def listar_conds(request):
    cond = Conds.objects.all()
    return render(request, 'lista_conds.html', {'conds': cond})

def detail_conds(request, condominio_id):
    condominio = get_object_or_404(Conds, id=condominio_id)
    
    #equipamentos
    faciais = Itens_facial.objects.filter(cond_id=condominio)
    dvr = Itens_dvr.objects.filter(cond_id=condominio)
    outro = Itens_outro.objects.filter(cond_id=condominio)
    
    #relatos
    relatos = Relatos.objects.filter(cond_id=condominio)
    
    return render(request, 'detail_conds.html', {
        'condominio': condominio,
        'faciais': faciais,
        'dvr': dvr,
        'outro': outro,
        'relatos': relatos
    })
    
def listar_relatos(request):
    relatos = Relatos.objects.all()
    context = {'relatos': relatos}
    
    return render(request, 'relato/listar_relatos.html', context)

def listar_equips(request):
    from itertools import chain
    
    faciais = Itens_facial.objects.all().order_by('-data')
    dvrs = Itens_dvr.objects.all().order_by('-data')
    outros = Itens_outro.objects.all().order_by('-data')
    
    all_items = sorted(
        chain(faciais, dvrs, outros),
        key=lambda instance: instance.data,
        reverse=True
    )
    
    itens_data = []
    for equipamento in all_items:
        if hasattr(equipamento, 'item'):
            if isinstance(equipamento, Itens_facial):
                tipo_modelo = 'Facial'
                tipo_display = 'Controlador Facial'
            elif isinstance(equipamento, Itens_dvr):
                tipo_modelo = 'DVR'
                tipo_display = 'DVR/NVR'
            elif isinstance(equipamento, Itens_outro):
                tipo_modelo = 'Outro'
                tipo_display = 'Outro'
            else:
                tipo_modelo = 'Equipamento'
                tipo_display = 'Equipamento'
            
            itens_data.append({
                'item': equipamento.item,
                'tipo': tipo_display,
                'tipo_modelo': tipo_modelo,
                'cond_id': equipamento.cond_id,
                'data': equipamento.data,
                'id': equipamento.id
            })
    
    context = {
        'faciais': faciais,
        'dvrs': dvrs,
        'outros': outros,
        'itens': itens_data
    }
    
    return render(request, 'equip-forms/listar_equips.html', context)

def edit_equip(request, equipamento_id, tipo):
    
    tipo_map = {
        'Facial': {'modelo': Itens_facial, 'form': FacialForm, 'template': 'equip-forms/editar_facial.html'},
        'DVR': {'modelo': Itens_dvr, 'form': DVRForm, 'template': 'equip-forms/editar_dvr.html'},
        'Outro': {'modelo': Itens_outro, 'form': OutroForm, 'template': 'equip-forms/editar_outro.html'},
    }
    
    # Validar tipo
    if tipo not in tipo_map:
        messages.error(request, 'Tipo de equipamento inválido.')
        return redirect('listar_equips')
    
    # Obter configurações baseadas no tipo
    config = tipo_map[tipo]
    equipamento = get_object_or_404(config['modelo'], id=equipamento_id)
    
    if request.method == 'POST':
        form = config['form'](request.POST, instance=equipamento)
        if form.is_valid():
            # ATUALIZA A DATA automaticamente
            equipamento_editado = form.save(commit=False)
            from django.utils import timezone
            equipamento_editado.data = timezone.now()  # Atualiza a data
            equipamento_editado.save()
            
            messages.success(request, f'Equipamento {equipamento.item} atualizado com sucesso!')
            return redirect('listar_equips')
        else:
            messages.error(request, 'Erro ao atualizar equipamento. Verifique os dados.')
    else:
        form = config['form'](instance=equipamento)
    
    context = {
        'form': form,
        'equipamento': equipamento,
        'tipo': tipo,
        'condominio': equipamento.cond_id
    }
    
    return render(request, config['template'], context)

def main_relato(request):
    cond = Conds.objects.all()
    return render(request, 'relato/main_relato.html', {'conds': cond})

def relato(request, condominio_id):
    condominio = get_object_or_404(Conds, id=condominio_id)
    tipos_relato = TipoRelato.objects.all()
    
    if request.method == 'POST':
        tipo_relato_id = request.POST.get('tipo_relato')
        try:
            # Busca pelo ID, não pelo nome
            tipo_relato = TipoRelato.objects.get(id=tipo_relato_id)
            
            request.session['tipo_relato_id'] = tipo_relato_id
            
            # Redireciona usando o NOME do tipo (que está na URL)
            return redirect('categoria_relato', 
                           condominio_id=condominio.id, 
                           tipo_relato=tipo_relato.nome)  # Usa tipo_relato.nome aqui
            
        except TipoRelato.DoesNotExist:
            messages.error(request, "Tipo de relato não encontrado.")
            return render(request, 'relato/relato.html', {
                'condominio': condominio,
                'tipos_relato': tipos_relato
            })
    
    return render(request, 'relato/relato.html', {
        'condominio': condominio,
        'tipos_relato': tipos_relato})

def categoria_relato(request, condominio_id, tipo_relato):
    condominio = get_object_or_404(Conds, id=condominio_id)
    
    # Buscar o objeto TipoRelato - forma segura
    try:
        tipo_relato_obj = TipoRelato.objects.get(nome=tipo_relato)
    except TipoRelato.DoesNotExist:
        messages.error(request, f"Tipo de relato '{tipo_relato}' não encontrado.")
        return redirect('relato', condominio_id=condominio_id)
    
    categorias_ayel = None
    categorias_cam = None
    
    if tipo_relato_obj.nome == 'ayel':
        categorias_ayel = CategoriaRelatoAyel.objects.all()
    elif tipo_relato_obj.nome == 'ayel_cameras':
        categorias_cam = CategoriaRelatoCam.objects.all()
    else:
        messages.error(request, "Tipo de relato inválido.")
        return redirect('relato', condominio_id=condominio_id)
    
    if request.method == 'POST':
        categoria_id = request.POST.get('cat_relato')
        
        if not categoria_id:
            messages.error(request, "Selecione uma categoria.")
            
            return render(request, 'relato/categoria_relato.html', {
                'condominio': condominio,
                'tipo_relato': tipo_relato_obj,
                'categorias_ayel': categorias_ayel,
                'categorias_cam': categorias_cam
            })
        
        # Salva a escolha da categoria na sessão
        request.session['categoria_id'] = categoria_id
        
        return redirect('cad_categoria', 
                       condominio_id=condominio.id, 
                       tipo_relato=tipo_relato_obj.nome,
                       cat_relato=categoria_id)
    
    return render(request, 'relato/categoria_relato.html', {
        'condominio': condominio,
        'tipo_relato': tipo_relato_obj,
        'categorias_ayel': categorias_ayel,
        'categorias_cam': categorias_cam
    })
    
def cad_categoria(request, condominio_id, tipo_relato, cat_relato):
    condominio = get_object_or_404(Conds, id=condominio_id)
    
    try:
        tipo_relato_obj = TipoRelato.objects.get(nome=tipo_relato)
    except TipoRelato.DoesNotExist:
        return redirect('main_relato')
    
    # Recupera os objetos das categorias baseado no tipo
    if tipo_relato == 'ayel':
        try:
            categoria_obj = CategoriaRelatoAyel.objects.get(id=cat_relato)
        except CategoriaRelatoAyel.DoesNotExist:
            messages.error(request, "Categoria Ayel não encontrada.")
            return redirect('categoria_relato', condominio_id=condominio_id, tipo_relato=tipo_relato)
    elif tipo_relato == 'ayel_cameras':
        try:
            categoria_obj = CategoriaRelatoCam.objects.get(id=cat_relato)
        except CategoriaRelatoCam.DoesNotExist:
            messages.error(request, "Categoria Câmeras não encontrada.")
            return redirect('categoria_relato', condominio_id=condominio_id, tipo_relato=tipo_relato)
    else:
        messages.error(request, "Tipo de relato inválido.")
        return redirect('main_relato')
    
    if request.method == 'POST':
        # Cria um dicionário com os dados do POST + os campos fixos
        post_data = request.POST.copy()
        
        # Garante que os campos ForeignKey estão corretos
        post_data['tipo_relato'] = tipo_relato_obj.id
        if tipo_relato == 'ayel':
            post_data['cat_rel_ayel_id'] = categoria_obj.id
            post_data['cat_rel_cam_id'] = ''  # Limpa o campo
        else:
            post_data['cat_rel_cam_id'] = categoria_obj.id
            post_data['cat_rel_ayel_id'] = ''  # Limpa o campo
        
        form = RelatoForm(post_data)
        
        if form.is_valid():
            relato_obj = form.save(commit=False)
            
            relato_obj.cond_id = condominio
            relato_obj.save()
            
            # Limpa a sessão
            if 'tipo_relato_id' in request.session:
                del request.session['tipo_relato_id']
            if 'categoria_id' in request.session:
                del request.session['categoria_id']
            
            messages.success(request, "Relato salvo com sucesso!")
            return redirect('listar_relatos')
        else:
            # DEBUG: Mostra erros do formulário
            print("Erros do formulário:", form.errors)
            messages.error(request, f"Erro no formulário: {form.errors}")
    else:
        # Preenche o formulário com dados iniciais
        initial_data = {
            'tipo_relato': tipo_relato_obj.id,
        }
        
        if tipo_relato == 'ayel':
            initial_data['cat_rel_ayel'] = categoria_obj.id
            initial_data['cat_rel_cam'] = None
        else:
            initial_data['cat_rel_cam'] = categoria_obj.id
            initial_data['cat_rel_ayel'] = None
        
        form = RelatoForm(initial=initial_data)
    
    return render(request, 'relato/relatoform.html', {
        'form': form,
        'condominio': condominio,
        'tipo_relato': tipo_relato_obj,
        'categoria': categoria_obj
    })

def dashboard(request):
    return render(request, 'dashboard.html')

def total_relatos(request):
    total = Relatos.objects.all().aggregate(Count('id'))['id__count']
    return JsonResponse({'total': total})

def dash_relatos_ano(request):
    # quantidade de relatos no ano atual
    x = Relatos.objects.all()
    
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    data = []
    labels = []
    mes = datetime.now().month + 1
    ano = datetime.now().year
    for i in range(12):
        mes -= 1
        if mes == 0:
            mes = 12
            ano -= 1
            
        y = len([i.id for i in x if i.data.month == mes and i.data.year == ano]) # conta a quantidade de elementos por mês
        labels.append(meses[mes-1]) # -1 porque a lista começa com 0
        data.append(y)
        
    data_json = {'data': data[::-1], 'labels': labels[::-1]}
    
    return JsonResponse(data_json)

def relato_cond(request):
    # 3 conds com mais relatos
    conds = Conds.objects.all()
    label = []
    data = []
    
    for cond in conds: # passa por cada item
        relatos = Relatos.objects.filter(cond_id=cond).aggregate(Count('id')) # seleciona no bd de relatos apenas os relatos com o id do condomínio
        
        label.append(cond.name)
        data.append(relatos['id__count'])
    
    x = list(zip(label, data)) # junta em uma lista - vira tupla

    x.sort(key=lambda x: x[1], reverse=True) # 'reverse=True' significa que vai organizar do maior para o menor
    
    x = list(zip(*x)) # separa a lista, uma com apenas os nomes e outra com a quantidade

    return JsonResponse({'labels': x[0][:3], 'data': x[1][:3]}) # [:3] = seleciona apenas os 3 primeiros da lista

def relatorio_categoria(request):
    # ordenar quantidade de relatos por categoria e por app
    relatos_ayel = Relatos.objects.filter(tipo_relato_id=1)
    relatos_cam = Relatos.objects.filter(tipo_relato_id=2)
    
    ayel_label = []
    ayel_data = []
    
    cam_label = []
    cam_data = []
    
    #AYEL
    ayel_count = relatos_ayel.values('cat_rel_ayel_id', 'cat_rel_ayel__nome_display_ayel').annotate(total=Count('id'))
    
    for cat in ayel_count:
        ayel_label.append(cat['cat_rel_ayel__nome_display_ayel'] or f"Categoria {cat['cat_rel_ayel__nome_display_ayel']}") # pega o nome da categoria e cria um fallback para se a categoria for None
        ayel_data.append(cat['total']) # soma e adiciona ao array 'total'
        
    x = list(zip(ayel_label, ayel_data))
    x.sort(key=lambda x: x[1], reverse=True)
    x = list(zip(*x))
    
    # AYEL CÂMERAS
    cam_count = relatos_cam.values('cat_rel_cam_id', 'cat_rel_cam__nome_display_cam').annotate(total=Count('id')).order_by('cat_rel_cam_id')

    
    for cat in cam_count:
        cam_label.append(cat['cat_rel_cam__nome_display_cam'] or f"Categoria {cat['cat_rel_cam__nome_display_cam']}")
        cam_data.append(cat['total'])
    y = list(zip(cam_label, cam_data))
    y.sort(key=lambda y: y[1], reverse=True)
    y = list(zip(*y))
    
    return JsonResponse({'ayel_labels': x[0], 'ayel_data': x[1],
                         'cam_labels': y[0], 'cam_data': y[1]})