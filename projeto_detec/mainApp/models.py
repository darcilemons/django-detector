from django.db import models
from django.utils import timezone

class Conds(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    endereco = models.CharField(max_length=200)
    
    def total_equipamentos(self):
        return (self.itens_facial.count() + 
                self.itens_dvr.count() + 
                self.itens_outro.count())
    
    def equipamentos_por_tipo(self):
        return {
            'faciais': self.itens_facial.count(),
            'dvr': self.itens_dvr.count(),
            'outro': self.itens_outro.count(),
            'total': self.total_equipamentos()
        }
        
    @classmethod
    def total_equipamentos_geral(cls):
        from .models import Itens_facial, Itens_dvr, Itens_outro
        
        total_facial = Itens_facial.objects.count()
        total_dvr = Itens_dvr.objects.count()
        total_outro = Itens_outro.objects.count()
        
        return {
            'faciais': total_facial,
            'dvrs': total_dvr,
            'outros': total_outro,
            'total_geral': total_facial + total_dvr + total_outro
        }
        
    def __str__(self):
        return self.name
    
class Itens_facial(models.Model):
    cond_id = models.ForeignKey(Conds, on_delete=models.CASCADE, related_name='itens_facial', verbose_name="Condomínio")
    item = models.CharField(max_length=100, verbose_name="Item")
    iplocal = models.CharField(max_length=15, verbose_name="IP Local")
    link = models.CharField(max_length=100, verbose_name="Link de acesso")
    mac = models.CharField(max_length=17, default="n/a", verbose_name="Endereço MAC")
    http = models.PositiveIntegerField(default="n/a", verbose_name="Porta HTTP")
    user = models.CharField(max_length=50, default="n/a", verbose_name="Usuário")
    senha = models.CharField(max_length=50, default="n/a", verbose_name="Senha")
    desc = models.CharField(max_length=100, default="n/a", verbose_name="Descrição")
    data = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.item} - {self.cond_id.name}"
    
class Itens_dvr(models.Model):
    cond_id = models.ForeignKey(Conds, on_delete=models.CASCADE, related_name='itens_dvr', verbose_name="Condomínio")
    item = models.CharField(max_length=100, verbose_name="Item")
    iplocal = models.CharField(max_length=15, verbose_name="IP Local")
    link = models.CharField(max_length=100, verbose_name="Link de acesso")
    mac = models.CharField(max_length=17, default="n/a", verbose_name="Endereço MAC")
    rtsp = models.PositiveIntegerField(default="n/a", verbose_name="Porta RTSP")
    http = models.PositiveIntegerField(default="n/a", verbose_name="Porta HTTP")
    user = models.CharField(max_length=50, default="n/a", verbose_name="Usuário")
    senha = models.CharField(max_length=50, default="n/a", verbose_name="Senha")
    desc = models.CharField(max_length=100, default="n/a", verbose_name="Descrição")
    data = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.item} - {self.cond_id.name}"
    
class Itens_outro(models.Model):
    cond_id = models.ForeignKey(Conds, on_delete=models.CASCADE, related_name='itens_outro', verbose_name="Condomínio")
    item = models.CharField(max_length=100, verbose_name="Item")
    iplocal = models.CharField(max_length=15, verbose_name="IP Local")
    link = models.CharField(max_length=100, verbose_name="Link de acesso")
    mac = models.CharField(max_length=17, default="n/a", verbose_name="Endereço MAC")
    rtsp = models.PositiveIntegerField(default="n/a", verbose_name="Porta RTSP")
    http = models.PositiveIntegerField(default="n/a", verbose_name="Porta HTTP")
    user = models.CharField(max_length=50, default="n/a", verbose_name="Usuário")
    senha = models.CharField(max_length=50, default="n/a", verbose_name="Senha")
    desc = models.CharField(max_length=100, default="n/a", verbose_name="Descrição")
    data = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.item} - {self.cond_id.name}"
    
class TipoEquip(models.Model):
    TIPOS_EQUIPAMENTOS = [
        ('FACIAL', 'Controladora Facial'),
        ('DVR', 'DVR/NVR'),
        ('OUTRO', 'Outro Equipamento'),
    ]
    
    nome = models.CharField(max_length=10, choices=TIPOS_EQUIPAMENTOS, unique=True)
    descricao = models.CharField(max_length=100)
    
    def __str__(self):
        return self.descricao

class TipoRelato(models.Model):
    TIPOS_RELATOS = [
        ('ayel', 'App Ayel'),
        ('ayel_cameras', 'App Ayel Câmeras')
    ]

    nome = models.CharField(max_length=15, choices=TIPOS_RELATOS, unique=True)

    def __str__(self):
        return self.nome
    
class CategoriaRelatoAyel(models.Model):
    CATEGORIA_AYEL = [
        ('aberturas', 'Aberturas'),
        ('cameras', 'Câmeras'),
        ('cadastroApp', 'Cadastro'),
        ('interfonia', 'Interfonia')
    ]
    
    nome = models.CharField(max_length=20, choices=CATEGORIA_AYEL, unique=True)
    
    def __str__(self):
        return self.nome
    
class CategoriaRelatoCam(models.Model):
    CATEGORIA_CAM = [
        ('login', 'Login'),
        ('cameras', 'Câmeras'),
        ('cadastroApp', 'Cadastro')
    ]
    
    nome = models.CharField(max_length=20, choices=CATEGORIA_CAM, unique=True)
    
    def __str__(self):
        return self.nome 

class Relatos(models.Model):
    cond_id = models.ForeignKey(Conds, on_delete=models.CASCADE, related_name='relatos', verbose_name='Condomínio')
    relato = models.CharField(max_length=100, verbose_name='Relato')
    tipo_relato = models.ForeignKey(TipoRelato, on_delete=models.CASCADE, related_name='tipo_relato', verbose_name='Tipo do Relato')
    cat_rel_ayel = models.ForeignKey(CategoriaRelatoAyel, on_delete=models.CASCADE, related_name='cat_rel_ayel', verbose_name='Categoria do Relato', null=True, blank=True)
    cat_rel_cam = models.ForeignKey(CategoriaRelatoCam, on_delete=models.CASCADE, related_name='cat_rel_ayel', verbose_name='Categoria do Relato', null=True, blank=True)
    data = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.cond_id.name} - {self.tipo_relato} - {self.relato}"
    
    def data_local(self):   # para exibir no template <td>{{ relato.data_local }}</td>
        from django.utils.timezone import localtime
        return localtime(self.data).strftime("%d/%m/%Y %H:%M:%S")
    
    