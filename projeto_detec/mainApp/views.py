from django.shortcuts import render, redirect, get_object_or_404
from .forms import condsForm, FacialForm, DVRForm, OutroForm
from .models import Conds, Itens_dvr, Itens_facial, Itens_outro

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
    
    faciais = Itens_facial.objects.filter(cond_id=condominio)
    dvr = Itens_dvr.objects.filter(cond_id=condominio)
    outro = Itens_outro.objects.filter(cond_id=condominio)
    
    return render(request, 'detail_conds.html', {
        'condominio': condominio,
        'faciais': faciais,
        'dvr': dvr,
        'outro': outro
    })