from django.shortcuts import render
from .forms import condsForm
from .models import conds

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

def listar_conds(request):
    cond = conds.objects.all()
    return render(request, 'lista.html', {'conds': cond})