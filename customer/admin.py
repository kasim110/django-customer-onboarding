from django.contrib import admin
from .models import CountryModel, DocumentSetModel, CustomerModel, CustomerDocumentModel

@admin.register(CountryModel)
class CountryModelAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(DocumentSetModel)
class DocumentSetModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'has_backside')
    filter_horizontal = ('countries',)

@admin.register(CustomerModel)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'surname', 'nationality', 'gender', 'created_by')

@admin.register(CustomerDocumentModel)
class CustomerDocumentModelAdmin(admin.ModelAdmin):
    list_display = ('customer', 'attached_file', 'created_at')