from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Ordem, Ativo, Empresa, Usuario, Grafico

class EmpresaResource(resources.ModelResource):
    class Meta:
        model = Empresa

class EmpresaAdmin(ImportExportModelAdmin):
    resource_class = EmpresaResource

class AtivoResource(resources.ModelResource):
    class Meta:
        model = Ativo

class AtivoAdmin(ImportExportModelAdmin):
    resource_class = AtivoResource

class OrdemResource(resources.ModelResource):
    class Meta:
        model = Ordem

class OrdemAdmin(ImportExportModelAdmin):
    resource_class = OrdemResource

admin.site.register(Ordem, OrdemAdmin)
admin.site.register(Ativo, AtivoAdmin)
admin.site.register(Empresa,EmpresaAdmin)
admin.site.register(Grafico)