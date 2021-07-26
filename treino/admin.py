from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *


class PlanoResource(resources.ModelResource):
    class Meta:
        model = Plano

class PlanoAdmin(ImportExportModelAdmin):
    resource_class = PlanoResource


class TreinoResource(resources.ModelResource):
    class Meta:
        model = Treino

class TreinoAdmin(ImportExportModelAdmin):
    resource_class = TreinoResource


class Treino_exercicioResource(resources.ModelResource):
    class Meta:
        model = Treino_exercicio

class Treino_exercicioAdmin(ImportExportModelAdmin):
    resource_class = Treino_exercicioResource


class ExercicioResource(resources.ModelResource):
    class Meta:
        model = Exercicio

class ExercicioAdmin(ImportExportModelAdmin):
    resource_class = ExercicioResource


class Grupo_muscularResource(resources.ModelResource):
    class Meta:
        model = Grupo_muscular

class Grupo_muscularAdmin(ImportExportModelAdmin):
    resource_class = Grupo_muscularResource

admin.site.register(Plano, PlanoAdmin)
admin.site.register(Grupo_muscular, Grupo_muscularAdmin)
admin.site.register(Exercicio, ExercicioAdmin)
admin.site.register(Treino_exercicio, Treino_exercicioAdmin)
admin.site.register(Treino, TreinoAdmin)