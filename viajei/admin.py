from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *

class ViagemResource(resources.ModelResource):
    class Meta:
        model = Viagem

class ViagemAdmin(ImportExportModelAdmin):
    resource_class = ViagemResource


class GastoResource(resources.ModelResource):
    class Meta:
        model = Gasto

class GastoAdmin(ImportExportModelAdmin):
    resource_class = GastoResource


class TransporteResource(resources.ModelResource):
    class Meta:
        model = Transporte

class TransporteAdmin(ImportExportModelAdmin):
    resource_class = TransporteResource


class HospedagemResource(resources.ModelResource):
    class Meta:
        model = Hospedagem

class HospedagemAdmin(ImportExportModelAdmin):
    resource_class = HospedagemResource


class RoteiroResource(resources.ModelResource):
    class Meta:
        model = Roteiro

class RoteiroAdmin(ImportExportModelAdmin):
    resource_class = RoteiroResource


class AtracaoResource(resources.ModelResource):
    class Meta:
        model = Atracao

class AtracaoAdmin(ImportExportModelAdmin):
    resource_class = AtracaoResource


class MalaResource(resources.ModelResource):
    class Meta:
        model = Mala

class MalaAdmin(ImportExportModelAdmin):
    resource_class = MalaResource


class ItemResource(resources.ModelResource):
    class Meta:
        model = Item

class ItemAdmin(ImportExportModelAdmin):
    resource_class = ItemResource


class AlbumResource(resources.ModelResource):
    class Meta:
        model = Album

class AlbumAdmin(ImportExportModelAdmin):
    resource_class = AlbumResource


class FotoResource(resources.ModelResource):
    class Meta:
        model = Foto

class FotoAdmin(ImportExportModelAdmin):
    resource_class = FotoResource


class Tipo_itemResource(resources.ModelResource):
    class Meta:
        model = Tipo_item

class Tipo_itemAdmin(ImportExportModelAdmin):
    resource_class = Tipo_itemResource


class Tipo_gastoResource(resources.ModelResource):
    class Meta:
        model = Tipo_gasto

class Tipo_gastoAdmin(ImportExportModelAdmin):
    resource_class = Tipo_gastoResource

admin.site.register(Viagem, ViagemAdmin)
admin.site.register(Tipo_gasto, Tipo_gastoAdmin)
admin.site.register(Tipo_item, Tipo_itemAdmin)
admin.site.register(Foto, FotoAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Mala, MalaAdmin)
admin.site.register(Atracao, AtracaoAdmin)
admin.site.register(Roteiro, RoteiroAdmin)
admin.site.register(Gasto, GastoAdmin)
admin.site.register(Hospedagem, HospedagemAdmin)
admin.site.register(Transporte, TransporteAdmin)