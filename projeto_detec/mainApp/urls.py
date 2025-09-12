from django.urls import path
from . import views

urlpatterns = [
    path('', views.cadastrar_cond, name='cadastro'),
    path('lista/', views.listar_conds, name='lista'),
]