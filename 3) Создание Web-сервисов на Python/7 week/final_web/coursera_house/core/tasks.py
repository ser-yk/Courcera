from __future__ import absolute_import, unicode_literals
from celery import task
from django.core.mail import send_mail
from django.conf import settings
from .models import Setting
import requests
from copy import deepcopy

@task()
def smart_home_manager():

    control_parameters = (control_leaking, control_cold_water, control_smoke, control_hot_water,
                          control_light, control_temperature)
    try:
        current_values = get_values()
        if current_values:
            new_value = check_parameters_bd(deepcopy(current_values))
            print('Проверил параметры в базе"')
            for parameter in control_parameters:
                parameter(new_value)
            commands = create_commands(current_values, new_value)
            if commands:
                send_command(commands)
    except:
        print('Error in  smart_home_manager')


def send_mail_to_user(theme, content):
    send_mail(theme, content, settings.EMAIL_RECEPIENT, [settings.EMAIL_RECEPIENT], fail_silently=False,)


def control_leaking(values):
    # Если есть протечка воды (leak_detector=true), закрыть холодную (cold_water=false) и горячую (hot_water=false)
    # воду и отослать письмо в момент обнаружения.
    if values['leak_detector']['value']:
        values['cold_water']['value'] = False
        values['hot_water']['value'] = False
        send_mail_to_user('control_leaking', 'Протечка воды, краны перекрыты')


def control_cold_water(values):
    # Если холодная вода (cold_water) закрыта, немедленно выключить бойлер (boiler) и стиральную машину (
    # washing_machine) и ни при каких условиях не включать их, пока холодная вода не будет снова открыта.
    if not values['cold_water']['value']:
        values['boiler']['value'] = False
        values['washing_machine']['value'] = 'off'


def control_hot_water(values):
    # Если горячая вода имеет температуру (boiler_temperature) меньше чем hot_water_target_temperature - 10%,
    # нужно включить бойлер (boiler), и ждать пока она не достигнет температуры hot_water_target_temperature + 10%,
    # после чего в целях экономии энергии бойлер нужно отключить
    try:
        per = 1 - values['boiler_temperature']['value'] / values['hot_water_target_temperature']['value']
        if per > 0.1:
            if values['cold_water']['value'] and not values['smoke_detector']['value']:
                values['boiler']['value'] = True
        elif per < -0.1:
            values['boiler']['value'] = False
    except (TypeError, ZeroDivisionError):
        return


def control_curtains(values):
    # Если шторы частично открыты (curtains == “slightly_open”), то они находятся на ручном управлении - это значит
    # их состояние нельзя изменять автоматически ни при каких условиях.
    if values['curtains']['value'] == 'slightly_open':
        return False
    else:
        return True


def control_light(values):
    # Если на улице (outdoor_light) темнее 50, открыть шторы (curtains), но только если не горит лампа в спальне (
    # bedroom_light). Если на улице (outdoor_light) светлее 50, или горит свет в спальне (bedroom_light),
    # закрыть шторы. Кроме случаев когда они на ручном управлении
    if values['outdoor_light']['value'] < 50 and not values['bedroom_light']['value'] and control_curtains(values):
        values['curtains']['value'] = 'open'
    elif (values['outdoor_light']['value'] > 50 or values['bedroom_light']['value']) and control_curtains(values):
        values['curtains']['value'] = 'close'


def control_smoke(values):
    # Если обнаружен дым (smoke_detector), немедленно выключить следующие приборы [air_conditioner, bedroom_light,
    # bathroom_light, boiler, washing_machine], и ни при каких условиях не включать их, пока дым не исчезнет.
    if values['smoke_detector']['value']:
        values['air_conditioner']['value'] = False
        values['bedroom_light']['value'] = False
        values['bathroom_light']['value'] = False
        values['boiler']['value'] = False
        values['washing_machine']['value'] = 'off'
        # send_mail_to_user('control_smoke', 'Задымление в помещении, приборы отключены')


def control_temperature(values):
    # Если температура в спальне (bedroom_temperature) поднялась выше bedroom_target_temperature + 10% - включить
    # кондиционер (air_conditioner), и ждать пока температура не опустится ниже bedroom_target_temperature - 10%,
    # после чего кондиционер отключить.
    try:
        per = 1 - values['bedroom_temperature']['value'] / values['bedroom_target_temperature']['value']
        if per <= -0.1 and not values['smoke_detector']['value']:
            values['air_conditioner']['value'] = True
        elif per >= 0.1:
            values['air_conditioner']['value'] = False
    except (TypeError, ZeroDivisionError) as exp:
        print(exp)
        return


# Получить все значения контроллеров из дома
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
        return


# Отправить команду на изменение параметров
def send_command(commands):
    try:
        data = {"controllers": [{'name': key, 'value': value} for key, value in commands.items()]}
        print('Отправляю параметры:\n', data)
        response = requests.post(settings.SMART_HOME_API_URL,
                                 headers={"Authorization":  f"Bearer {settings.SMART_HOME_ACCESS_TOKEN}"}, json=data)
        print('Сервер ответил', response.status_code, response.json().get("field_problems", []))
        return response.json().get("data", [])
    except BaseException as exp:
        print(exp)


# Посмотреть, что в БД и внести правки в текущие значения
def check_parameters_bd(values):
    for i in Setting.objects.all():
        if i.value < 2:
            values[i.controller_name]['value'] = bool(i.value)
        else:
            values[i.controller_name] = {'value': i.value}
    return values


# Создаю комманды для сервера, сравнивая два слованя
def create_commands(old_values, new_values):
    recordable_controller = ('air_conditioner', 'bathroom_light', 'curtains', 'boiler',
                             'cold_water', 'hot_water', 'washing_machine', 'bedroom_light')
    commands = {}
    for i in old_values:
        if old_values[i]['value'] != new_values[i]['value'] and i in recordable_controller:
            commands[i] = new_values[i]['value']
    return commands



