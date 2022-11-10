from django.contrib import admin
from django.contrib.admin.options import messages
from django.shortcuts import Http404, get_object_or_404, redirect, reverse
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django_fsm import can_proceed

from .models import Fund, Subscription


class FundAdmin(admin.ModelAdmin):
    fields = ['name', 'goal', 'closing_date']
    list_display = ['name', 'goal', 'closing_date']
    list_filter = ['closing_date']
    search_fields = ['name']

    def get_urls(self):
        base_urls = super().get_urls()
        close_url = path('<int:pk>/close',
                         self.admin_site.admin_view(self.close),
                         name=f'{self.opts.app_label}_{self.opts.model_name}_close')
        publisher_url = path('<int:pk>/publish',
                             self.admin_site.admin_view(self.publish),
                             name=f'{self.opts.app_label}_{self.opts.model_name}_publish')
        return [close_url, publisher_url] + base_urls

    def close(self, request, pk):
        if request.method != 'POST':
            raise Http404()

        fund_to_close = get_object_or_404(Fund, id=pk)
        if not can_proceed(fund_to_close.close):
            self.__give_status_validation_feedback(request, fund_to_close, Fund.Status.CLOSED)
            return redirect(reverse('admin:investments_fund_change', args=[pk]))

        fund_to_close.close()
        fund_to_close.save()
        # Translators: successful feedback from admin fund close action
        self.message_user(request, _('This fund is now closed'))

        return redirect('admin:investments_fund_changelist')

    def publish(self, request, pk):
        if request.method != 'POST':
            raise Http404()

        fund_to_publish = get_object_or_404(Fund, id=pk)
        if not can_proceed(fund_to_publish.publish):
            self.__give_status_validation_feedback(request, fund_to_publish, Fund.Status.PUBLISHED)
            return redirect(reverse('admin:investments_fund_change', args=[pk]))

        fund_to_publish.publish()
        fund_to_publish.save()
        # Translators: successful feedback from admin fund publishing action
        self.message_user(request, _('This fund is now published'))
        return redirect('admin:investments_fund_changelist')

    def __give_status_validation_feedback(self, request, fund, status):
        fund.status = status
        form = self.get_form(request, fund, change=True)(data=fund.__dict__.copy(), instance=fund)
        for field_name, error in form.errors.items():
            messages.error(request, f'{field_name}: {error.as_text()}')


admin.site.register(Fund, FundAdmin)
admin.site.register(Subscription)
