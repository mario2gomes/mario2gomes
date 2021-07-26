from django.urls import reverse
from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

class Plano(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    inicio = models.DateField()
    fim = models.DateField()
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("plano")
        verbose_name_plural = _("planos")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plano_detail", kwargs={"pk": self.pk})


class Treino(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    plano = models.ForeignKey("Plano", on_delete=models.DO_NOTHING)
    data = models.DateField()
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = _("treino")
        verbose_name_plural = _("treinos")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("treino_detail", kwargs={"pk": self.pk})

class Treino_exercicio(models.Model):
    treino = models.ForeignKey("Treino", on_delete=models.DO_NOTHING)
    exercicio = models.ForeignKey("Exercicio", on_delete=models.DO_NOTHING)
    carga = models.DecimalField(decimal_places=2, max_digits=4)#em quilos
    repeticoes = models.IntegerField()
    #feito = models.IntegerField()#sim ou nÃ£o
    data_hora = models.DateTimeField()
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("treino_exercicio")
        verbose_name_plural = _("treino_exercicios")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("treino_exercicio_detail", kwargs={"pk": self.pk})


class Exercicio(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='fotos/treino', blank=True,null=True)
    grupo_muscular = models.ForeignKey("Grupo_muscular", on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("exercicio")
        verbose_name_plural = _("exercicios")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("exercicio_detail", kwargs={"pk": self.pk})


class Grupo_muscular(models.Model):
    descricao = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("grupo_muscular")
        verbose_name_plural = _("grupo_musculars")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("grupo_muscular_detail", kwargs={"pk": self.pk})