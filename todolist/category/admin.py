"""# Admin IHM"""


from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register
from django.utils.translation import ugettext_lazy as _

from category.models import Category


@register(Category)
class CategoryAdmin(ModelAdmin):
    """
    ## Category admin IHM

    This object cannot be modified after being created.
    So we can only create or view this object.
    """

    model = Category
    fields = ("name", "slug")
    list_display = ("name", "project_names")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

    @staticmethod
    def project_names(obj):
        """Human readable project set formatted for list_display"""
        return ", ".join(s.name for s in obj.project_set.all())
    project_names.short_description = _("projects")

    def get_prepopulated_fields(self, request, obj=None):
        """Do not pre-populate fields on a simple view page"""
        if obj is not None:
            return {}
        return super().get_prepopulated_fields(request, obj)

    def has_module_permission(self, request):
        """Can be accessed from home page"""
        return True

    def has_add_permission(self, request):
        """Can add an object"""
        return True

    def has_delete_permission(self, request, obj=None):
        """Cannot delete an object"""
        return False

    def has_change_permission(self, request, obj=None):
        """Cannot change an object"""
        return False

    def has_view_permission(self, request, obj=None):
        """Can view an object"""
        return True
