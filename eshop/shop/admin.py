from django.contrib import admin
from .models import *

class SubcategoryAdmin(admin.ModelAdmin):
    """
    Customizes the display and filtering options for the Subcategory model in the Django admin interface.
    """
    list_display = ('name', 'category')  # Fields displayed in the list view
    list_filter = ('category',)  # Fields available for filtering
    search_fields = ('name',)  # Fields available for searching

# Registers models with the Django admin interface
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(Subcategory, SubcategoryAdmin)  # Registers Subcategory model with custom admin options
