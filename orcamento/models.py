from django.urls import reverse
from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

class Despesa(models.Model):
    nome = models.CharField(max_length=200)
    estabelecimento = models.ForeignKey('Estabelecimento', on_delete=models.DO_NOTHING, null=True)
    valor = models.DecimalField(max_digits=10,decimal_places=2)
    vencimento = models.IntegerField()
    data_pagamento = models.DateTimeField()
    tipo = models.ForeignKey('tipo', on_delete=models.DO_NOTHING,null=True)
    pagamento = models.ForeignKey('Pagamento', on_delete=models.DO_NOTHING,null=True)
    parcelado = models.IntegerField(default=0) #parcelado ou não
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,null=True)
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ('despesa')
        verbose_name_plural = ('despesas')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('despesa_detail', kwargs={'pk': self.pk})

class Tipo(models.Model):
    descricao = models.CharField(max_length=20)

    class Meta:
        verbose_name = ('tipo')
        verbose_name_plural = ('tipos')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tipo_detail', kwargs={'pk': self.pk})

class Estabelecimento(models.Model):
    nome = models.CharField(max_length=50)
    tipo = models.CharField(choices=(('F','fisico'),('I','internet')), max_length=8)
    endereco = models.CharField(max_length=100)
    cidade = models.CharField(max_length=50)
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ('estabelecimento')
        verbose_name_plural = ('estabelecimentos')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('estabelecimento_detail', kwargs={'pk': self.pk})

class Pagamento(models.Model):
    nome = models.CharField(max_length=50)
    tipo = models.CharField(choices=(('C','CrÃ©dito'),('D','DÃ©bito'),('V','Ã Vista')), max_length=50)
    valor = models.DecimalField(max_digits=4,decimal_places=2)

    class Meta:
        verbose_name = ("pagamento")
        verbose_name_plural = ("pagamentos")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("pagamento_detail", kwargs={"pk": self.pk})


class Feira(models.Model):
    data = models.DateTimeField()
    supermercado = models.ForeignKey("Estabelecimento",on_delete=models.DO_NOTHING,null=True)
    preco_total = models.DecimalField(max_digits=4,decimal_places=2)
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)    

    class Meta:
        verbose_name = ("feira")
        verbose_name_plural = ("feiras")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("feira_detail", kwargs={"pk": self.pk})

class Item(models.Model):
    nome = models.CharField(max_length=50)
    tipo = models.ForeignKey('Tipo_item', on_delete=models.DO_NOTHING,null=True)
    preco = models.DecimalField(max_digits=4,decimal_places=2)
    quantidade = models.IntegerField()
    medida = models.ForeignKey('Medida', on_delete=models.DO_NOTHING,null=True)
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)    
    
    class Meta:
        verbose_name = ("item")
        verbose_name_plural = ("items")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"pk": self.pk})

class Tipo_item(models.Model):
    nome = models.CharField(max_length=50)    

    class Meta:
        verbose_name = ("tipo_item")
        verbose_name_plural = ("tipo_items")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tipo_item_detail", kwargs={"pk": self.pk})

class Medida(models.Model):
    nome = models.CharField(max_length=50)    

    class Meta:
        verbose_name = _("medida")
        verbose_name_plural = _("medidas")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("medida_detail", kwargs={"pk": self.pk})
