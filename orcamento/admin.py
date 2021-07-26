from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *


class DespesaResource(resources.ModelResource):
    class Meta:
        model = Despesa

class DespesaAdmin(ImportExportModelAdmin):
    resource_class = DespesaResource

class TipoResource(resources.ModelResource):
    class Meta:
        model = Tipo

class TipoAdmin(ImportExportModelAdmin):
    resource_class = TipoResource

class EstabelecimentoResource(resources.ModelResource):
    class Meta:
        model = Estabelecimento

class EstabelecimentoAdmin(ImportExportModelAdmin):
    resource_class = EstabelecimentoResource

class PagamentoResource(resources.ModelResource):
    class Meta:
        model = Pagamento

class PagamentoAdmin(ImportExportModelAdmin):
    resource_class = PagamentoResource

class FeiraResource(resources.ModelResource):
    class Meta:
        model = Feira

class FeiraAdmin(ImportExportModelAdmin):
    resource_class = FeiraResource

class ItemResource(resources.ModelResource):
    class Meta:
        model = Item

class ItemAdmin(ImportExportModelAdmin):
    resource_class = ItemResource

class Tipo_itemResource(resources.ModelResource):
    class Meta:
        model = Tipo_item

class Tipo_itemAdmin(ImportExportModelAdmin):
    resource_class = Tipo_itemResource


class MedidaResource(resources.ModelResource):
    class Meta:
        model = Medida

class MedidaAdmin(ImportExportModelAdmin):
    resource_class = MedidaResource

admin.site.register(Despesa, DespesaAdmin)
admin.site.register(Medida, MedidaAdmin)
admin.site.register(Tipo_item, Tipo_itemAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Feira, FeiraAdmin)
admin.site.register(Pagamento, PagamentoAdmin)
admin.site.register(Estabelecimento, EstabelecimentoAdmin)
admin.site.register(Tipo, TipoAdmin)