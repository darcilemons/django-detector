from django.shortcuts import render, redirect, get_object_or_404
from .forms import condsForm, FacialForm, DVRForm, OutroForm
from django.http import JsonResponse
from .models import Conds, Itens_dvr, Itens_facial, Itens_outro

def cadastrar_cond(request):
    cond_form = condsForm()
    equipamento_form = None
    condominio_id = None
    
    if request.method == 'POST':
        if 'condominio_data' in request.POST:
            # Processa formulário do condomínio
            cond_form = condsForm(request.POST)
            if cond_form.is_valid():
                condominio = cond_form.save()
                condominio_id = condominio.id
                # Não redireciona, mantém na mesma página
                
        elif 'equipamento_data' in request.POST:
            # Processa formulário do equipamento
            condominio_id = request.POST.get('condominio_id')
            tipo_equipamento = request.POST.get('tipo_equipamento')
            
            if tipo_equipamento == 'FACIAL':
                form = FacialForm(request.POST)
            elif tipo_equipamento == 'DVR':
                form = DVRForm(request.POST)
            elif tipo_equipamento == 'OUTRO':
                form = OutroForm(request.POST)
            else:
                form = None
                
            if form and form.is_valid() and condominio_id:
                equipamento = form.save(commit=False)
                equipamento.cond_id_id = condominio_id
                equipamento.save()
                return redirect('sucesso')
    
    return render(request, 'conds_cad.html', {
        'cond_form': cond_form,
        'condominio_id': condominio_id
    })
    
def get_form_fields(request):
    """View AJAX que retorna o formulário de equipamento"""
    if request.method == 'GET':
        tipo_equipamento = request.GET.get('tipo')
        condominio_id = request.GET.get('condominio_id')
        
        if tipo_equipamento == 'FACIAL':
            form = FacialForm()
        elif tipo_equipamento == 'DVR':
            form = DVRForm()
        elif tipo_equipamento == 'OUTRO':
            form = OutroForm()
        else:
            return JsonResponse({'error': 'Tipo inválido'})
        
        # Renderiza o formulário como HTML
        form_html = render(request, 'form_equipamento_partial.html', {
            'form': form,
            'tipo_equipamento': tipo_equipamento,
            'condominio_id': condominio_id
        }).content.decode('utf-8')
        
        return JsonResponse({'form_html': form_html})
    
    return JsonResponse({'error': 'Método não permitido'})

def listar_conds(request):
    cond = Conds.objects.all()
    return render(request, 'lista_conds.html', {'conds': cond})