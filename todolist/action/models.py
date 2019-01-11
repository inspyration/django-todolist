"""# Models"""

from django.db.models import (
    Model,
    CharField,
    PositiveSmallIntegerField,
    ForeignKey,
    SlugField,
    DateField,
    BooleanField,
    DateTimeField,
    TextField,
    ManyToManyField,
    TimeField,
    CASCADE,
    PROTECT,
)
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from polymorphic.models import PolymorphicModel

from project.models import Project


class Action(PolymorphicModel):
    """
    ## Financial action

    This object if the main object of the project.
    """

    PRIORITIES = (
        ("⇈", _("⇈ Very high")),
        ("↑", _("↑ High")),
        ("⇅", _("⇅ Regular")),
        ("↓", _("↓ Low")),
        ("⇊", _("⇊ Very low")),
    )

    STATUSES = (
        ("A", _("Fuzzy")),
        ("B", _("Draft")),
        ("C", _("Planned")),
        ("D", _("In progress")),
        ("E", _("Archived")),
        ("V", _("Dropped (Archived)")),
        ("W", _("Dropped (In progress)")),
        ("X", _("Dropped (Planned)")),
        ("Y", _("Dropped (Draft)")),
        ("Z", _("Dropped (Fuzzy)")),
    )

    TIME_DELTA_UNITS = (
        ("w", _("week(s)")),
        ("d", _("day(s)")),
        ("h", _("hour(s)")),
        ("m", _("minute(s)")),
    )

    @cached_property
    def type(self):
        """Work around to get quickly, efficiently and reliably the polymorphic type of this contact."""
        return self.polymorphic_ctype.name

    project = ForeignKey(
        verbose_name=_("project"),
        related_name="action_set",
        to=Project,
        blank=False,
        null=False,
        db_index=True,
        on_delete=PROTECT,
    )

    priority = CharField(
        _("priority"),
        max_length=1,
        choices=PRIORITIES,
        blank=False,
        default="⇅",
        db_index=True,
    )

    status = CharField(
        _("status"),
        max_length=1,
        choices=STATUSES,
        blank=False,
        default="A",
        db_index=True,
    )

    deadline = DateField(
        verbose_name=_("deadline"),
        blank=True,
        null=True,
        db_index=True,
    )

    label = CharField(
        verbose_name=_("label"),
        max_length=48,
        blank=False,
        null=False,
        db_index=True,
    )

    name = CharField(
        verbose_name=_("name"),
        max_length=128,
        blank=False,
        null=False,
        db_index=True,
    )

    description = TextField(
        verbose_name=_("description"),
        blank=False,
        null=False,
        db_index=True,
    )

    planned_on = DateTimeField(
        verbose_name=_("planned on"),
        blank=True,
        null=True,
        db_index=True,
    )

    estimate = PositiveSmallIntegerField(
        verbose_name=_("estimate"),
        blank=True,
        null=True,
        db_index=True,
    )

    estimate_unit = CharField(
        _("estimate unit"),
        max_length=1,
        choices=TIME_DELTA_UNITS,
        blank=True,
        null=True,
        db_index=True,
    )

    @property
    def estimate_label(self):
        """Human readable information on estimate"""
        if not (self.estimate and self.estimate_unit):
            return '-'
        return f"{self.estimate} {self.get_estimate_unit_display()}"

    duration = PositiveSmallIntegerField(
        verbose_name=_("duration"),
        blank=True,
        null=True,
        db_index=True,
    )

    duration_unit = CharField(
        _("duration unit"),
        max_length=1,
        choices=TIME_DELTA_UNITS,
        blank=True,
        null=True,
        db_index=True,
    )

    @property
    def duration_label(self):
        """Human readable information on duration"""
        if not (self.duration and self.duration_unit):
            return '-'
        return f"{self.duration} {self.get_duration_unit_display()}"

    slug = SlugField(
        unique=True,
        max_length=32,
        editable=True,
        db_index=True,
    )

    dependency_set = ManyToManyField(
        verbose_name=_("dependencies"),
        related_name="subordinate_set",
        to="self",
        symmetrical=False,
        blank=True,
    )

    def __str__(self):
        """Human readable representation"""
        return self.name

    def __repr__(self):
        """Technical representation"""
        return "<{} {}>".format(self._meta.object_name, self.name)

    class Meta:  # pylint: disable=too-few-public-methods
        """Action Meta class"""

        verbose_name = _("action")
        verbose_name_plural = _("actions")
        ordering = ("-planned_on", "-deadline", "name")
        index_together = (
            ("planned_on", "deadline", "name"),
            ("project", "label"),
            ("project", "name"),
        )


class Event(Action):
    """
    ## Event model

    This object represents an event.
    """

    location = CharField(
        verbose_name=_("location"),
        max_length=64,
        blank=True,
        null=True,
        db_index=True,
    )

    departure_time = TimeField(
        verbose_name=_("time"),
        blank=True,
        null=True,
        db_index=True,
    )

    send_reminder = BooleanField(
        verbose_name=_("Do you want a reminder to be sent ?"),
        default=False,
        db_index=True,
    )

    class Meta(Action.Meta):  # pylint: disable=too-few-public-methods
        """Event Meta class"""

        verbose_name = _("event")
        verbose_name_plural = _("events")


class RecurrentAction(Action):
    """
    ## Recurrent actions model

    This model represent a action that is repeated over a period of time.
    """

    FREQUENCY = (
        ("d", _("daily")),
        ("w", _("weekly")),
        ("m", _("monthly")),
        ("y", _("yearly")),
    )

    frequency = CharField(
        verbose_name=_("frequency"),
        max_length=1,
        blank=False,
        null=False,
        db_index=True,
        choices=FREQUENCY,
    )

    active = BooleanField(
        verbose_name=_("active"),
        db_index=True,
    )

    until = DateTimeField(
        verbose_name=_("until"),
        blank=True,
        null=True,
        db_index=True,
    )

    count = PositiveSmallIntegerField(
        verbose_name=_("count"),
        blank=False,
        null=False,
    )

    class Meta(Action.Meta):  # pylint: disable=too-few-public-methods
        """RecurrentAction Meta class"""

        verbose_name = _("recurrent action")
        verbose_name_plural = _("recurrent actions")


class Note(Model):
    """
    ## Financial transaction

    This object if the main object of the project.
    """

    action = ForeignKey(
        verbose_name=_("action"),
        related_name="note_set",
        to=Action,
        blank=False,
        null=False,
        db_index=True,
        on_delete=CASCADE,
    )

    number = PositiveSmallIntegerField(
        verbose_name=_("number"),
        blank=False,
        null=False,
        db_index=True,
    )

    content = TextField(
        verbose_name=_("content"),
        blank=False,
        null=False,
        db_index=True,
    )

    def __str__(self):
        """Human readable representation"""
        return self.content

    def __repr__(self):
        """Technical representation"""
        return "<{} {}>".format(self._meta.object_name, self.content)

    class Meta:  # pylint: disable=too-few-public-methods
        """Transaction Meta class"""

        verbose_name = _("note")
        verbose_name_plural = _("notes")
        ordering = ("number",)
        index_together = (
            ("action", "number"),
        )


class Step(Model):
    """
    ## Financial transaction

    This object if the main object of the project.
    """

    action = ForeignKey(
        verbose_name=_("action"),
        related_name="step_set",
        to=Action,
        blank=False,
        null=False,
        db_index=True,
        on_delete=CASCADE,
    )

    number = PositiveSmallIntegerField(
        verbose_name=_("number"),
        blank=False,
        null=False,
        db_index=True,
    )

    planned_on = DateTimeField(
        verbose_name=_("planned on"),
        blank=True,
        null=True,
        db_index=True,
    )

    content = TextField(
        verbose_name=_("content"),
        blank=False,
        null=False,
        db_index=True,
    )

    def __str__(self):
        """Human readable representation"""
        return self.content

    def __repr__(self):
        """Technical representation"""
        return "<{} {}>".format(self._meta.object_name, self.content)

    class Meta:  # pylint: disable=too-few-public-methods
        """Transaction Meta class"""

        verbose_name = _("step")
        verbose_name_plural = _("steps")
        ordering = ("planned_on", "id")


class Log(Model):
    """
    ## Financial transaction

    This object if the main object of the project.
    """

    action = ForeignKey(
        verbose_name=_("action"),
        related_name="log_set",
        to=Action,
        blank=False,
        null=False,
        db_index=True,
        on_delete=CASCADE,
    )

    number = PositiveSmallIntegerField(
        verbose_name=_("number"),
        blank=False,
        null=False,
        db_index=True,
    )

    date = DateTimeField(
        verbose_name=_("date"),
        blank=True,
        null=True,
        db_index=True,
    )

    content = TextField(
        verbose_name=_("content"),
        blank=False,
        null=False,
        db_index=True,
    )

    def __str__(self):
        """Human readable representation"""
        return self.content

    def __repr__(self):
        """Technical representation"""
        return "<{} {}>".format(self._meta.object_name, self.content)

    class Meta:  # pylint: disable=too-few-public-methods
        """Transaction Meta class"""

        verbose_name = _("log")
        verbose_name_plural = _("log book")
        ordering = ("date", "id")
