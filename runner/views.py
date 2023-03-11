from django.shortcuts import render
from .models import Configuration
from django.views.generic.edit import FormView
from django import forms

def index(request):
    configuration: Configuration = Configuration.get_solo()

    return render(request, 'base.html', context={
        'is_running': configuration.should_run,
        'file_path': configuration.runner_file.url,
        'total_count': configuration.total_count,
        'skip_traced': configuration.skip_traced,
    })



class ConfigurationForm(forms.ModelForm):
    class Meta:
         model = Configuration
         fields = ['should_run', 'runner_file']

class ContactFormView(FormView):
    template_name = 'base.html'
    form_class = ConfigurationForm
    success_url = '/runner/'

    def form_valid(self, form: forms.ModelForm):
        value = super().form_valid(form)
        configuration: Configuration = Configuration.get_solo()

        should_run = form.data.get('should_run')
        if should_run:
            configuration.should_run = True if should_run == 'true' else False
            configuration.save()

        runner_file = form.files.get('runner_file')
        if runner_file:
            configuration.runner_file = runner_file
            configuration.total_count = 0
            configuration.skip_traced = 0
            configuration.save()

        return value