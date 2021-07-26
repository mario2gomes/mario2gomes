from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *

class PostagemResource(resources.ModelResource):
    class Meta:
        model = Postagem

class PostagemAdmin(ImportExportModelAdmin):
    resource_class = PostagemResource

class RespostaResource(resources.ModelResource):
    class Meta:
        model = Resposta

class RespostaAdmin(ImportExportModelAdmin):
    resource_class = RespostaResource

admin.site.register(Postagem, PostagemAdmin)
admin.site.register(Resposta, RespostaAdmin)