from django.db import models
from django.conf import settings
from django.urls import reverse 

class Postagem(models.Model):
    titulo = models.CharField(max_length=50)
    url = models.SlugField(max_length=20, unique=True)#usa o slug do model na barra de endereço como um valor pra complementar a url
    texto = models.CharField(max_length=10000)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    categoria = models.ForeignKey('Categoria', on_delete=models.DO_NOTHING, null=False) 
    publico = models.IntegerField()
    imagem = models.ImageField(upload_to='fotos', blank=True,null=True)
    criacao = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    atualizacao = models.DateTimeField(auto_now=True, blank=True,null=True)   

    class Meta:
        #verbose_name = _("postagem")
        #//verbose_name_plural = _("postagens")
        verbose_name = ("postagem")
        verbose_name_plural = ("postagens")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("postagem_detail", kwargs={"pk": self.pk})

class Resposta(models.Model):
    postagem = models.ForeignKey('Postagem', on_delete=models.DO_NOTHING, null=False)
    texto = models.CharField(max_length=500)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    publico = models.IntegerField()
    criacao = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    atualizacao = models.DateTimeField(auto_now=True, blank=True,null=True)    
    
    class Meta:
        #verbose_name = _("resposta")
        #verbose_name_plural = _("respostas")
        verbose_name = ("resposta")
        verbose_name_plural = ("respostas")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("resposta_detail", kwargs={"pk": self.pk})

class Categoria(models.Model):
    descricao = models.CharField(max_length=50)

    class Meta:
        #verbose_name = _("Categoria")
        #verbose_name_plural = _("Categorias")
        verbose_name = ("categoria")
        verbose_name_plural = ("categorias")

    def __str__(self):
        return self.descricao
                