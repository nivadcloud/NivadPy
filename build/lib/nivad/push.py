import json
import logging

import re

from .push_click_action import NoAction, ClickAction

logger = logging.getLogger("nivad")


class NotificationObject:
    def __init__(self, title, text, **kwargs):
        self.title = title
        self.text = text
        self.full_title = str(kwargs.get('full_title', ''))
        self.full_text = str(kwargs.get('full_text', ''))
        self.status_bar_text = str(kwargs.get('status_bar_text', ''))
        self.vibration = kwargs.get('vibration', None)
        self.click_action = kwargs.get('click_action', NoAction())
        self.led_color = kwargs.get('led_color', None)

    def is_valid(self):
        """
        Checks fields values

        :return:
        """
        assert isinstance(self.click_action, ClickAction)

        if self.led_color:
            if type(self.led_color) == int:
                self.led_color = format(self.led_color, 'x')
            if not type(self.led_color) == str:
                self.led_color = None
                logger.warning('Invalid LED color type. should be string or integer')
            else:
                if len(self.led_color) == 7:
                    self.led_color = '0{}'.format(self.led_color)
                else:
                    self.led_color = '{}{}'.format('0' * (max(0, 6 - len(self.led_color))), self.led_color)

                if not re.match(r'[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?', self.led_color):
                    logger.warning('Invalid LED color')
                    self.led_color = None

        if self.vibration:
            if type(self.vibration) != bool:
                logger.warning('Invalid vibration value')
                self.vibration = None

        if not self.title or not self.text:
            logger.Error('Both Title and Text values are required')
            return False

        return True

    def to_dict(self):
        """
        Convert this notification message object to REST API compatible dictionary

        :return:
        """
        return_value = dict()
        for item in ['title', 'text', 'full_title', 'full_text', 'status_bar_text', 'vibration', 'led_color']:
            item_value = getattr(self, item, None)
            if item_value:
                return_value[item] = item_value

        return_value['click_action_type'] = self.click_action.click_action_type
        return_value['click_action'] = self.click_action.click_action
        if not return_value['click_action']:
            del return_value['click_action']

        return return_value


class NivadNotificationAPI:
    """
    Wrapper for notifications API Endpoint
    """
    URLS = {
        'send_notification': 'notification/'
    }

    def __init__(self, nivad_api):
        self.api = nivad_api

    def send(self, notification_object):
        """
        Send a notification to all devices

        :param notification_object:
        :return:
        """
        assert notification_object.is_valid(), 'Notification object is invalid'

        response = self.api.post(
            NivadNotificationAPI.URLS['send_notification'],
            data=json.dumps(notification_object.to_dict()),
            token_type='push_api'
        )

        return json.loads(response.data.decode('utf-8'))

    def get_info(self, notification_id):
        assert notification_id is not None and type(notification_id) == int

        response = json.loads(self.api.get(
            NivadNotificationAPI.URLS['send_notification'],
            data={'notification_id': str(notification_id)},
            token_type='push_api'
        ).data.decode('utf-8'))
        if not response['success']:
            raise ValueError('Invalid notification id')

        return NotificationInfo(response)


class NotificationInfo:

    def __init__(self, response_data):
        self._response_data = response_data

    def __getattr__(self, item):
        if item in self._response_data and item != 'message':
            return self._response_data[item]
        else:
            if 'message' in item:
                if len(item) < len('message_'):
                    raise AttributeError("Unknown attribute: '%s'" % item)
                item = item[len('message_'):]
                if item not in self._response_data['message']:
                    raise AttributeError("Unknown attribute: 'message_%s'" % item)
                else:
                    return self._response_data['message'][item]
            raise AttributeError("Unknown attribute: '%s'" % item)


class NotificationLEDColor:
    white = 'ffffff'
    red = 'ff0000'
    orange = 'fe9400'
    yellow = 'ffff00'
    pink = 'f90368'
    blue = '0000ff'
    purple = '8600ff'
    cyan = '00ffe6'
    green = '00ff00'
    lime = 'd2ff00'

"""
import nivad
from nivad.push_click_action import *
from nivad.push import *

api = nivad.NivadAPI('5d9dc126-8583-4d0e-b325-b76d107a8d32', push_api_secret='YmMolkX2PweqqkTeIOjDQMX4KuITTZeTr3JcV6bFz9jXoDrUrYSDHnM9RKTNvfUV')
notification = api.get_notification_api()
message = NotificationObject('title', 'text', full_title='full title', full_text='full text', vibration=False, status_bar_text='sb text', led_color=NotificationLEDColor.red)
notification.send(message)

"""