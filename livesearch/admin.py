from django.contrib import admin
from livesearch.models import AdvancedSearch, SearchApi

class SearchApiAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(AdvancedSearch)
admin.site.register(SearchApi, SearchApiAdmin)
