from django.shortcuts import render
from .models import Configuration
from django.views.generic.edit import FormView
from django import forms
from django.conf import settings
from django.http import FileResponse
from django.urls import reverse


def scrapper_file(request):
    file = open(settings.BASE_DIR / 'searchpeoplefree.csv', 'rb')
    response = FileResponse(file, content_type="text/csv")
    # https://docs.djangoproject.com/en/1.11/howto/outputting-csv/#streaming-large-csv-files
    response['Content-Disposition'] = 'attachment; filename="searchpeoplefree.csv"'

    return response

def index(request):
    configuration: Configuration = Configuration.get_solo()

    return render(request, 'base.html', context={
        'is_running': configuration.should_run,
        'file_path': reverse('runner:scrapper'),
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
            with open(settings.BASE_DIR / 'searchpeoplefree.csv', 'wb') as file:
                file.write(runner_file.read())
                configuration.total_count = 0
                configuration.skip_traced = 0
                configuration.save()

        return value