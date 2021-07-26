from django.db import models
from django.conf import settings
from django.urls import reverse

class Item(models.Model):
    nome = models.CharField(max_length=100,null=False)
    descricao = models.CharField(max_length=1000,blank=True,null=True)
    preco = models.DecimalField(max_digits=10,decimal_places=2,null=False)
    estabelecimento = models.ForeignKey('Estabelecimento', on_delete=models.DO_NOTHING, null=False)
    categoria = models.ForeignKey('Categoria', on_delete=models.DO_NOTHING, blank=True,null=True)
    em_estoque = models.IntegerField()
    medida = models.CharField(max_length=100, blank=True,null=True)
    unidade = models.DecimalField(max_digits=4,decimal_places=0, blank=True,null=True)
    observacao = models.CharField(max_length=1000, blank=True,null=True)
    imagem = models.ImageField(upload_to='fotos', blank=True,null=True)
    criacao = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    atualizacao = models.DateTimeField(auto_now=True, blank=True,null=True)


    #class Meta:
        #verbose_name = _("item")
        #verbose_name_plural = _("itens")

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"pk": self.pk})

class Estabelecimento(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=100, null=False)
    endereco = models.CharField(max_length=300, blank=True,null=True)
    telefone = models.CharField(max_length=300, blank=True,null=True)
    instagram = models.CharField(max_length=300, blank=True,null=True)
    email = models.CharField(max_length=300, blank=True,null=True)
    facebook = models.CharField(max_length=300, blank=True,null=True)
    outra_midia = models.CharField(max_length=300, blank=True,null=True)
    observacao = models.CharField(max_length=1000, blank=True,null=True)
    criacao = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    atualizacao = models.DateTimeField(auto_now=True, blank=True,null=True)

    #class Meta:
        #verbose_name = _("estabelecimento")
        #verbose_name_plural = _("estabelecimentos")

    def __str__(self):
        return self.nome

    #quando clicar no estabelecimento em admin traz esse retorno
    def get_absolute_url(self):
        return reverse("editar_estabelecimento", kwargs={"pk": self.pk})
        

class Categoria(models.Model):
    nome = models.CharField(max_length=100, null=False)
    estabelecimento = models.ForeignKey('Estabelecimento', on_delete=models.DO_NOTHING, null=False)
    observacao = models.CharField(max_length=1000, blank=True,null=True)
    criacao = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    atualizacao = models.DateTimeField(auto_now=True, blank=True,null=True)

    #class Meta:
        #verbose_name = _("categoria")
        #verbose_name_plural = _("categorias")

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse("categoria_detail", kwargs={"pk": self.pk})

class Medida(models.Model):
    nome = models.CharField(max_length=100, null=False)
    estabelecimento = models.ForeignKey('Estabelecimento', on_delete=models.DO_NOTHING, blank=True,null=True)
    tipo = models.CharField(max_length=100, blank=True,null=True)
    criacao = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    atualizacao = models.DateTimeField(auto_now=True, blank=True,null=True)

    #class Meta:
        #verbose_name = _("medida")
        #verbose_name_plural = _("medidas")

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse("medida_detail", kwargs={"pk": self.pk})

