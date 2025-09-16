from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cad_cond/', views.cad_cond, name='cadastrar_condominio'),
    path('equipamento/<int:condominio_id>/', views.equip, name='equip'),
    path('cadastrar-equipamento/<int:condominio_id>/<str:tipo>/', views.cad_equip, name='cad_equip'),
    path('listar_conds', views.listar_conds, name='listar_conds'),
    path('listar_conds/<int:condominio_id>/', views.detail_conds, name='detail_conds'),
    path('main_relato/', views.main_relato, name='main_relato'),
    path('main_relato/<int:condominio_id>/', views.relato, name='relato'),
    path('main_relato/<int:condominio_id>/<str:tipo>/', views.categoria_relato, name='categoria_relato'),
    path('main_relato/<int:condominio_id>/<str:tipo>/<str:cat_relato>/', views.cad_categoria, name='cad_categoria'),
    
]