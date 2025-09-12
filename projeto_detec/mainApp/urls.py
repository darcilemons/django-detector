from django.urls import path
from . import views

urlpatterns = [
    path('cad_cond/', views.cadastrar_cond, name='cadastro'),
    path('conds/', views.listar_conds, name='conds'),
]