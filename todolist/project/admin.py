"""# Admin IHM"""


from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register

from project.models import Project


@register(Project)
class ProjectAdmin(ModelAdmin):
    """
    ## Project admin IHM

    This object cannot be modified after being created.
    So we can only create or view this object.
    """

    model = Project
    fields = ("category", "name", "slug")
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("category__name", "name")
    autocomplete_fields = ("category",)

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
