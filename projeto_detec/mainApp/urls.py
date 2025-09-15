from django.urls import path
from . import views

urlpatterns = [
    path('cadcond/', views.cadastrar_cond, name='cadastrar_condominio'),
    path('list_conds/', views.listar_conds, name='listar_conds'),
    path('list_equip/', views.get_form_fields, name='get_form_fields'),
]