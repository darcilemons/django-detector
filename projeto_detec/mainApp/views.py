from django.shortcuts import render, redirect, get_object_or_404
from .forms import condsForm, FacialForm, DVRForm, OutroForm, RelatoForm
from django.contrib import messages
from .models import Conds, Itens_dvr, Itens_facial, Itens_outro, TipoRelato, CategoriaRelatoAyel, CategoriaRelatoCam, Relatos

def home(request):
    return render(request, 'home.html')

def cad_cond(request):
    if request.method == 'POST':
        form = condsForm(request.POST)
        if form.is_valid():
            condominio = form.save()
            return redirect('equip', condominio_id=condominio.id)
    else:
        form = condsForm()
    
    return render(request, 'conds_cad.html', {'form': form})

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
        return redirect('equip', condominio_id=condominio_id)
    
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            equipamento = form.save(commit=False)
            equipamento.cond_id = condominio
            equipamento.save()
            return redirect('cadastrar_condominio')
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
    return render(request, 'relato/listar_relatos.html', {'relatos': relatos})

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
        messages.error(request, f"Tipo de relato '{tipo_relato}' não encontrado.")
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
            return redirect('home')
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