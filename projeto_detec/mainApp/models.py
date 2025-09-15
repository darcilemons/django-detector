from django.db import models
from django.utils import timezone

class Conds(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    endereco = models.CharField(max_length=200)
    equipamento = models.CharField(max_length=10, choices=[
        ('FACIAL', 'Facial'),
        ('DVR', 'DVR'),
        ('OUTRO', 'Outro')
    ], default='FACIAL')
    relatos = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name
    
class Itens_facial(models.Model):
    cond_id = models.ForeignKey(Conds, on_delete=models.CASCADE, related_name='itens_facial', verbose_name='Condomínio')
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
        return self.item
    
class Itens_dvr(models.Model):
    cond_id = models.ForeignKey(Conds, on_delete=models.CASCADE, related_name='itens_dvr', verbose_name='Condomínio')
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
        return self.item
    
class Itens_outro(models.Model):
    cond_id = models.ForeignKey(Conds, on_delete=models.CASCADE, related_name='itens_outro', verbose_name='Condomínio')
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
        return self.item