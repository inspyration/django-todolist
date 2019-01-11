"""# Admin IHM"""


from datetime import date

from django.contrib.admin import SimpleListFilter, StackedInline
from django.contrib.admin.decorators import register
from django.utils.translation import ugettext_lazy as _
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin

from action.models import Action, Event, RecurrentAction, Note, Step, Log


def month_list_filter_factory(field_name, title, parameter_name, duration_unit):
    """## Month filter factory"""
    class MonthListFilter(SimpleListFilter):
        """
        Month filter for some action's attributes used for list IHM

        This objects allow to filter actions according to any month effectively used in at least one action.
        This is an action specific filter.
        """

        def lookups(self, request, model_admin):
            """Generator that get used months and format it"""
            for month in model_admin.get_queryset(request).dates(field_name, duration_unit, order="DESC"):
                yield (month.strftime("%m-%Y"), month.strftime("%B %Y"))

        def queryset(self, request, queryset):
            """Query set to get actually used months"""
            value = self.value()
            if value is None:
                return queryset

            try:
                start_month, start_year = map(int, value.split("-"))
            except ValueError:
                return queryset

            if duration_unit == "month":
                if start_month == 12:
                    end_month, end_year = 1, start_year + 1
                else:
                    end_month, end_year = start_month + 1, start_year

                return queryset.filter(date__gte=date(start_year, start_month, 1),
                                       date__lt=date(end_year, end_month, 1))

            return queryset

    # Human-readable title which will be displayed in the right admin sidebar just above the filter options.
    MonthListFilter.title = title

    # Parameter for the filter that will be used in the URL query.
    MonthListFilter.parameter_name = parameter_name

    return MonthListFilter


class NoteInline(StackedInline):
    """Note inline configuration class"""

    model = Note
    fields = ("number", "content")
    readonly_fields = ("number",)
    min_num = 0
    extra = 1


class StepInline(StackedInline):
    """Step inline configuration class"""

    model = Step
    fieldsets = (
        (None, {
            "fields": (
                ("number", "planned_on"),
                ("content",),
            )
        }),
    )
    min_num = 0
    extra = 0


class LogInline(StackedInline):
    """Log inline configuration class"""

    model = Log
    fieldsets = (
        (None, {
            "fields": (
                ("number", "date"),
                ("content",),
            )
        }),
    )
    min_num = 0
    extra = 1


class ActionMixin:
    """Mixing to avoid repeating property twice"""

    @staticmethod
    def project_category(obj):
        """Shortcut to the category of the source, for list view"""
        return obj.project.category.name
    project_category.short_description = _("category")

    @staticmethod
    def dependency_status(obj):
        """Shortcut to the category of the source, for list view"""
        return "{todo}/{dropped}{total}//{subordinate}".format(
            todo=obj.dependency_set.filter(status__in=["E", "F"]).count(),
            dropped=obj.dependency_set.filter(status__in=["V", "W", "X", "Y", "Z"]).count(),
            total=obj.dependency_set.all().count(),
            subordinate=obj.subordinate_set.all().count(),
        )
    dependency_status.short_description = _("dependency status")  # "todo/dropped/total/subordinate"

    base_model = Action
    inlines = [NoteInline, StepInline, LogInline]
    search_fields = ("project__category__name", "project__name", "label", "deadline", "planned_on")
    autocomplete_fields = ("project", "dependency_set")
    list_filter = (
        "project__category",
        "project",
        month_list_filter_factory("deadline", _("deadline"), "deadline", "month"),
        month_list_filter_factory("planned_on", _("planned_on"), "planned_on", "month"),
        "duration_unit",
        "estimate_unit",
    )
    list_display = (
        "project_category",
        "project",
        "type",
        "label",
        "deadline",
        "planned_on",
        "estimate_label",
        "duration_label",
        "dependency_status",
        "priority",
        "status",
    )

    def has_module_permission(self, request):  # pylint: disable=no-self-use,unused-argument
        """Can be accessed from home page"""
        return True

    def has_add_permission(self, request):  # pylint: disable=no-self-use,unused-argument
        """Can add an object"""
        return True

    def has_delete_permission(self, request, obj=None):  # pylint: disable=no-self-use,unused-argument
        """Can delete an object"""
        return True

    def has_change_permission(self, request, obj=None):  # pylint: disable=no-self-use,unused-argument
        """Can update an object"""
        return True

    def has_view_permission(self, request, obj=None):  # pylint: disable=no-self-use,unused-argument
        """Can view an object"""
        return True


class ActionChildAdmin(ActionMixin, PolymorphicChildModelAdmin):
    """
    ## Action base admin IHM

    This object if the main object of the project.
    This object can be created / updated / deleted.
    This IHM can be used as is and with the polymorphic child objects. Those would work the same way.
    """


@register(Event)
class EventAdmin(ActionChildAdmin):
    """
    ## Event specific admin IHM

    This object represents a action that is an actual event.
    """

    base_model = Event
    show_in_index = True
    readonly_fields = ("slug", "name")
    fieldsets = (
        (None, {
            "fields": (
                ("project", "label", "priority", "status"),
                ("name", "deadline", "planned_on"),
                ("location", "departure_time", "send_reminder"),
                ("estimate", "estimate_unit", "duration", "duration_unit"),
                ("description",),
            )
        }),
        (_("Technical information"), {
            "fields": (
                ("slug",),
                ("dependency_set",),
            )
        }),
    )


@register(RecurrentAction)
class RecurrentActionAdmin(ActionChildAdmin):
    """
    ## Recurrent action specific admin IHM

    This object represents a action that is an anticipation of a planned and recurrent event.
    """

    base_model = RecurrentAction
    show_in_index = True
    readonly_fields = ("slug", "name")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("project", "label", "priority", "status"),
                    ("name", "deadline", "planned_on"),
                    ("estimate", "estimate_unit", "duration", "duration_unit"),
                    ("description",),
                )
            }),
        (_("Recurring features"), {
            "fields": (
                ("active", "frequency", "count", "until"),
            )
        }),
        (_("Technical information"), {
            "fields": (
                ("slug",),
                ("dependency_set",),
            )
        }),
    )


@register(Action)
class ContactParentAdmin(ActionMixin, PolymorphicParentModelAdmin):
    """
    ## Actual IHM for actions and theirs polymorphic children

    Some features need to be repeated here to work for the action object itself
    (childs objects use Child model admin).
    """

    readonly_fields = ("slug", "name")
    fieldsets = (
        (None, {
            "fields": (
                ("project", "label", "priority", "status"),
                ("name", "deadline", "planned_on"),
                ("estimate", "estimate_unit", "duration", "duration_unit"),
                ("description",),
            )
        }),
        (_("Technical information"), {
            "fields": (
                ("slug",),
                ("dependency_set",),
            )
        }),
    )
    child_models = (Action, Event, RecurrentAction)
