from django.urls import reverse
from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

class Viagem(models.Model):
    nome = models.CharField(max_length=50)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    inicio = models.DateField()
    fim = models.DateField()
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)    

    class Meta:
        #verbose_name = _("viagem")
        verbose_name = ("viagem")
        #verbose_name_plural = _("viagems")
        verbose_name_plural = ("viagems")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("viagem_detail", kwargs={"pk": self.pk})

class Acompanhante(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    viagem = models.ForeignKey('Viagem', on_delete=models.DO_NOTHING)
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        #verbose_name = _("acompanhante")
        verbose_name = ("acompanhante")
        #verbose_name_plural = _("acompanhantes")
        verbose_name_plural = ("acompanhantes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("acompanhante_detail", kwargs={"pk": self.pk})

class Gasto(models.Model):
    nome = models.CharField(max_length=50)
    viagem = models.ForeignKey('Viagem', on_delete=models.DO_NOTHING)
    tipo_gasto = models.ForeignKey('Tipo_gasto', on_delete=models.DO_NOTHING)
    valor = models.DecimalField(max_digits=6,decimal_places=2)
    data_pagamento = models.DateTimeField()
    moeda = models.CharField(max_length=100)
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        #verbose_name = _("gastos")
        verbose_name = ("gastos")
        #verbose_name_plural = _("gastoss")
        verbose_name_plural = ("gastoss")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("gastos_detail", kwargs={"pk": self.pk})

class Tipo_gasto(models.Model):
    descricao = models.CharField(max_length=100)
    viagem = models.ForeignKey('Viagem', on_delete=models.DO_NOTHING)

    class Meta:
        #verbose_name = _("tipo_gasto")
        verbose_name = ("tipo_gasto")
        #verbose_name_plural = _("tipo_gastos")
        verbose_name_plural = ("tipo_gastos")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tipo_gasto_detail", kwargs={"pk": self.pk})

class Transporte(models.Model):
    nome = models.CharField(max_length=50)
    viagem = models.ForeignKey('Viagem', on_delete=models.DO_NOTHING)
    gasto = models.ForeignKey('Gasto', on_delete=models.DO_NOTHING)
    observacao = models.CharField(max_length=100)
    data_saida = models.DateTimeField()
    data_chegada = models.DateTimeField()
    local_saida = models.CharField(max_length=100)
    local_chegada = models.CharField(max_length=100)
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        #verbose_name = _("transporte")
        verbose_name = ("transporte")
        #verbose_name_plural = _("transportes")
        verbose_name_plural = ("transportes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("transporte_detail", kwargs={"pk": self.pk})

class Hospedagem(models.Model):
    nome = models.CharField(max_length=50)
    viagem = models.ForeignKey('Viagem', on_delete=models.DO_NOTHING)
    gasto = models.ForeignKey('Gasto', on_delete=models.DO_NOTHING)
    observacao = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    checkin = models.DateTimeField()
    checkout =models.DateTimeField()
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        #verbose_name = _("hospedagem")
        verbose_name = ("hospedagem")
        #verbose_name_plural = _("hospedagems")
        verbose_name_plural = ("hospedagems")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("hospedagem_detail", kwargs={"pk": self.pk})


class Roteiro(models.Model):
    viagem = models.ForeignKey('Viagem', on_delete=models.DO_NOTHING)
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        #verbose_name = _("roteiro")
        verbose_name = ("roteiro")
        #verbose_name_plural = _("roteiros")
        verbose_name_plural = ("roteiros")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("roteiro_detail", kwargs={"pk": self.pk})

class Atracao(models.Model):
    nome = models.CharField(max_length=50)
    roteiro = models.ForeignKey('Roteiro', on_delete=models.DO_NOTHING)
    data = models.DateTimeField()
    gasto = models.ForeignKey('Gasto', on_delete=models.DO_NOTHING)
    observacao = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)
    feito = models.CharField(max_length=100)#sim ou nÃ£o
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        #verbose_name = _("atracao")
        verbose_name = ("atracao")
        #verbose_name_plural = _("atracaos")
        verbose_name_plural = ("atracaos")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("atracao_detail", kwargs={"pk": self.pk})


class Mala(models.Model):
    viagem = models.ForeignKey('Viagem', on_delete=models.DO_NOTHING)
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        #verbose_name = _("mala")
        verbose_name = ("mala")
        #verbose_name_plural = _("malas")
        verbose_name_plural = ("malas")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("mala_detail", kwargs={"pk": self.pk})

class Item(models.Model):
    nome = models.CharField(max_length=50)
    mala = models.ForeignKey('Mala', on_delete=models.DO_NOTHING)
    peso = models.DecimalField(max_digits=4,decimal_places=2)
    tipo_item = models.ForeignKey('Tipo_item', on_delete=models.DO_NOTHING)
    observacao = models.CharField(max_length=100)
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        #verbose_name = _("item")
        verbose_name = ("item")
        #verbose_name_plural = _("items")
        verbose_name_plural = ("items")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"pk": self.pk})

#eletronico, roupa, higiene, presente, reliquia, etc
class Tipo_item(models.Model):
    mala = models.ForeignKey('Mala', on_delete=models.DO_NOTHING)
    descricao = models.CharField(max_length=100)
    consumo = models.CharField(max_length=100)#sim ou nÃ£o

    class Meta:
        #verbose_name = _("tipo_item")
        verbose_name = ("tipo_item")
        #verbose_name_plural = _("tipo_items")
        verbose_name_plural = ("tipo_items")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tipo_item_detail", kwargs={"pk": self.pk})


class Album(models.Model):
    nome = models.CharField(max_length=50, null=True)
    viagem = models.ForeignKey('Viagem', on_delete=models.DO_NOTHING)
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        #verbose_name = _("album")
        verbose_name = ("album")
        #verbose_name_plural = _("albums")
        verbose_name_plural = ("albums")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("album_detail", kwargs={"pk": self.pk})

class Foto(models.Model):
    album = models.ForeignKey('Album', on_delete=models.DO_NOTHING)
    imagem = models.ImageField(upload_to='fotos/viajei', blank=True,null=True)
    data = models.DateTimeField()
    criacao = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    atualizacao = models.DateTimeField(auto_now=True, blank=True,null=True)

    class Meta:
        #verbose_name = _("foto")
        verbose_name = ("foto")
        #verbose_name_plural = _("fotos")
        verbose_name_plural = ("fotos")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("foto_detail", kwargs={"pk": self.pk})