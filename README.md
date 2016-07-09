# Nivad REST API


Python wrapper for [nivad cloud](https://nivad.cloud/) REST API.

## Setup

    pip install nivad

or

    git clone https://github.com/nivadcloud/NivadPy && cd NivadPy
    python setup.py install

## Usage

    import nivad
    api = nivad.NivadAPI('<Application ID>', push_api_secret='<Push API Secret>')

Supply as many secret keys as you need. Valid keys are:
* push_api
* push
* billing
* master (Use with caution!)

all postfixed by `_secret`

### Push notification API

You will need to provide `push_api_secret` or `master_secret` to `NivadAPI` constructor method in order to use these endpoints

    push = api.get_notification_api()

provides you with a configured `NivadNotificationAPI` instance.

#### Send a notification to all devices

    from nivad.push import NotificationObject, NotificationLEDColor
    from nivad.push_click_action import OpenURL

    message = NotificationObject(
        'title',
        'text',
        full_title='full title',
        full_text='full text',
        vibration=False,
        status_bar_text='sb text',
        led_color=NotificationLEDColor.red
        click_action=OpenURL('https://nivad.cloud/')
    )
    result = push.send(message)
    if result['success']:
        print('Succeeded, notification id:', result['notification_id'])
    else:
        print('Error.', result['errors'])

##### Notification click actions
You can specify the action to perform in user's device when (s)he clicks on notification message.
supported actions in current version of API are:
* Open URL
* Open Application (self or other applications by package name)
* Open an Instagram page
* Join a Telegram chat (group and channel)
* Open a Telegram chat (By handle)

Future actions will be:
* Run a `Service` in background to execute arbitrary pre defined code.
* Open an `Activity`.

Both will have the ability to specify `Intent` extra data. These actions are available through web interface and will be available in REST API soon.

##### Notification LED Colors
Use `NotificationLEDColor` to specify device LED blinking color upon arrival of this push notification message.

#### Get notification data

    info = push.get_info(<notification_id>)

    info.success  # True,
    info.notification_id  # 4529
    info.status  # ارسال شده
    info.device_count  # 676230
    info.send_time  # 2016-07-08T18:48:30.735854+00:00
    info.message_title  # Message Title
    info.message_text  # Message Text
    # And more `info.message_***' stuff

