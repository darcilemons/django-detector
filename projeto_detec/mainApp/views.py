from django.shortcuts import render
from .forms import condsForm
from .models import Conds, Itens_dvr, Itens_facial, Itens_outro

def cadastrar_cond(request):
    if request.method == 'POST':
        form = condsForm(request.POST)
        if form.is_valid():
            form.save()
            form = condsForm()
            mensagem = "Condomínio cadastrado com sucesso!"
            return render(request, 'conds_cad.html', {
                'form': form,
                'mensagem': mensagem
            })
    else:
        form = condsForm()
    
    return render(request, 'conds_cad.html', {'form': form})

def cad_item(request):
    if request.meethod == 'POST':
        form = itemForm(request.POST)
        if form.is_valid():
            form.save()
            form = itemForm()
            mensagem = "Equipamento cadastrado!"
            return render(request, 'itens_cad.html', {
                'itemForm':form,
                'mensagem':mensagem
            })

def listar_itens(request):
    facial = Itens_facial.objects.all()
    dvr = Itens_dvr.objects.all()
    outro = Itens_outro.objects.all()
    return render(request, 'lista_itens.html', {'facial':facial}, {'dvr':dvr}, {'outro':outro})

def listar_conds(request):
    cond = Conds.objects.all()
    return render(request, 'lista_conds.html', {'conds': cond})