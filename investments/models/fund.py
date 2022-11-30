from datetime import date
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _, pgettext_lazy
from djmoney.models.fields import MoneyField

from django_fsm import FSMField, transition
import moneyed


class Fund(models.Model):
    class Status(models.TextChoices):
        BEING_CREATED = 'being created', _('Being created')
        PUBLISHED = 'published', _('Published')
        CLOSED = 'closed', pgettext_lazy('Fund Status. E.g.: "This fund is now closed"', 'Closed')

    name = models.CharField(_('Fund name'), max_length=100, unique=True)
    closing_date = models.DateField(pgettext_lazy('Bring a fund to a close', 'Closing date'),
                                    blank=True,
                                    null=True)
    goal = MoneyField(_('Goal'),
                      max_digits=10,
                      decimal_places=2,
                      default_currency=moneyed.Currency('EUR'),
                      blank=True, null=True)
    status = FSMField(default=Status.BEING_CREATED, choices=Status.choices)

    def can_publish(self):
        if self.closing_date is None or self.goal is None:
            return False
        return True

    @transition(field=status,
                source=[Status.BEING_CREATED, Status.CLOSED],
                target=Status.PUBLISHED,
                conditions=[can_publish])
    def publish(self):
        pass

    def can_close(self):
        if self.closing_date <= date.today():
            return True
        return False

    @transition(field=status, source=Status.PUBLISHED, target=Status.CLOSED, conditions=[can_close])
    def close(self):
        pass

    def clean(self):
        self.__validate_required_fields_for_status()

    def __str__(self):
        return self.name

    def __validate_required_fields_for_status(self):
        if self.status == self.Status.PUBLISHED:
            if self.closing_date is None and self.goal is None:
                raise ValidationError({
                    'closing_date': ValidationError(
                        pgettext_lazy('Bring a fund to a close', 'Closing date field is required'),
                        code='required'
                    ),
                    'goal': ValidationError(_('Goal field is required'), code='required')
                })
            if self.closing_date is None:
                raise ValidationError(
                    {'closing_date': pgettext_lazy('Bring a fund to a close',
                                                   'Closing date field is required')},
                    code='required'
                )
            if self.goal is None:
                raise ValidationError({'goal': _('Goal field is required')}, code='required')
        if self.status == self.Status.CLOSED:
            if self.closing_date >= date.today():
                raise ValidationError({'closing_date': _('Closing date has not expired yet')})

    class Meta:
        verbose_name = _('fund')
        verbose_name_plural = _('funds')
