from django.contrib import admin
from django.contrib.admin.options import forms
from django.shortcuts import Http404, redirect
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django_fsm import can_proceed

from .models import Fund, Subscription


class FundAdminForm(forms.ModelForm):
    class Meta:
        model = Fund
        fields = ['status', 'goal', 'closing_date', 'name']


class FundAdmin(admin.ModelAdmin):
    fields = ['name', 'goal', 'closing_date']
    list_display = ['name', 'goal', 'closing_date']
    list_filter = ['closing_date']
    search_fields = ['name']

    def get_urls(self):
        base_urls = super().get_urls()
        publisher_url = path('<int:pk>/publish',
                             self.admin_site.admin_view(self.publish),
                             name=f'{self.opts.app_label}_{self.opts.model_name}_publish')
        return [publisher_url] + base_urls

    def publish(self, request, pk):
        if request.method != 'POST':
            raise Http404()

        fund_to_publish = Fund.objects.get(id=pk)
        if not can_proceed(fund_to_publish.publish):
            fund_to_publish.status = Fund.Status.PUBLISHED
            adminform = self.__validate_and_prerender_form(request, fund_to_publish)
            response = self.change_view(request, str(pk))
            response.context_data['adminform'] = adminform
            return response

        fund_to_publish.publish()
        fund_to_publish.save()
        # Translators: positive feedback from admin fund publishing action
        self.message_user(request, _('This fund is now published'))
        return redirect('admin:investments_fund_changelist')

    def __validate_and_prerender_form(self, request, fund):
        form = FundAdminForm(data=fund.__dict__, instance=fund)
        return admin.helpers.AdminForm(form,
                                       self.get_fieldsets(request, fund),
                                       self.get_prepopulated_fields(request, fund),
                                       model_admin=self)


admin.site.register(Fund, FundAdmin)
admin.site.register(Subscription)
