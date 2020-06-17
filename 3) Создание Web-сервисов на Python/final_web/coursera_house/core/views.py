from django.urls import reverse_lazy
from django.views.generic import FormView
from django.http import HttpResponse
from django.conf import settings
import requests

from .tasks import send_command
from .models import Setting
from .form import ControllerForm
import time


class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    def __init__(self):
        self.main_params = ('bedroom_target_temperature', 'hot_water_target_temperature',
                            'bedroom_light', 'bathroom_light')
        self.current_values = get_values()

        super(ControllerView, self).__init__()


    def get_context_data(self, **kwargs):
        context = super(ControllerView, self).get_context_data()
        context['data'] = {}
        try:
            for control, c_data in self.current_values.items():
                context['data'][control] = c_data['value']
                # .replace("_", " ").capitalize()
            return context
        except:
            context['data']['Error'] = 'No data'
            return context


    def get_initial(self):
        res = dict()
        for i in self.main_params:
            try:
                if i in ('bedroom_target_temperature', 'hot_water_target_temperature'):
                    p = Setting.objects.get(controller_name=i)
                    value = p.value
                    res[i] = value if value > 1 else bool(value)
                else:
                    res[i] = self.current_values[i]['value']
            except Setting.DoesNotExist:
                pass
        return res


    def form_valid(self, form):
        new_values = dict()
        commands = dict()
        for i in form.cleaned_data:
            if isinstance(form.cleaned_data[i], int):
                new_values[i] = form.cleaned_data[i]
            else:
                new_values[i] = int(form.cleaned_data[i])
        for key, value in new_values.items():
            try:
                c = Setting.objects.get(controller_name=key)
                if c.value != value:
                    c.value = value
                    c.save()
                    if key in ('bedroom_light', 'bathroom_light'):
                        commands[key] = value
            except Setting.DoesNotExist:
                Setting.objects.create(controller_name=key, value=value, label=f'{"update:"} {time.time()}')
        if commands and not get_values()['smoke_detector']['value']:
            send_command(commands)
        return super(ControllerView, self).form_valid(form)



def get_values():
    try:
        response = requests.get(settings.SMART_HOME_API_URL,
                                headers={"Authorization":  f"Bearer {settings.SMART_HOME_ACCESS_TOKEN}"})
        parameters = response.json().get("data", [])
        if parameters:
            values = dict()
            for parameter in parameters:
                values[parameter['name']] = {'value': parameter['value']}
            return values
    except:
        return HttpResponse(status=502)