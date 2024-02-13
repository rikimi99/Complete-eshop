from django.contrib import admin
from .models import *

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(Subcategory, SubcategoryAdmin)