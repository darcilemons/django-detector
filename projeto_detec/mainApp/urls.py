from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cad_cond/', views.cad_cond, name='cadastrar_condominio'), # cadastro condomínio
    path('home_equip', views.home_equip, name='home_equip'), # tela de cadastrar equipamento vindo do home
    path('equipamento/<int:condominio_id>/', views.equip, name='equip'), # cadastro equipamento no condomínio
    path('cadastrar-equipamento/<int:condominio_id>/<str:tipo>/', views.cad_equip, name='cad_equip'), # tipo do equipamento (dvr, facial ou outro)
    path('listar_conds/', views.listar_conds, name='listar_conds'), # listar os condomínios
    path('listar_relatos/', views.listar_relatos, name='listar_relatos'), # listar relatos
    path('listar_equips/', views.listar_equips, name='listar_equips'), # listar equipamentos
    path('listar_equips/edit_equip/<int:equipamento_id>/<str:tipo>/', views.edit_equip, name='edit_equip'), # editar equipamento
    path('listar_conds/<int:condominio_id>/', views.detail_conds, name='detail_conds'), # detalhar condomínio
    path('main_relato/', views.main_relato, name='main_relato'), # primeira página relato
    path('main_relato/<int:condominio_id>/', views.relato, name='relato'), # escolher app
    path('main_relato/<int:condominio_id>/<str:tipo_relato>/', views.categoria_relato, name='categoria_relato'), # categoria do relato
    path('main_relato/<int:condominio_id>/<str:tipo_relato>/<str:cat_relato>/', views.cad_categoria, name='cad_categoria'), # cadastrar relato
]