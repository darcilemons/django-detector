from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cad_cond/', views.cad_cond, name='cadastrar_condominio'),
    path('equipamento/<int:condominio_id>/', views.equip, name='equip'),
    path('cadastrar-equipamento/<int:condominio_id>/<str:tipo>/', views.cad_equip, name='cad_equip'),
    path('listar_conds', views.listar_conds, name='listar_conds'),
    path('listar_conds/<int:condominio_id>/', views.detail_conds, name='detail_conds')
]