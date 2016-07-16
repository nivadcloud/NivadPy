import abc


class PushFilter(abc.ABC):

    @abc.abstractmethod
    def to_json(self):
        pass


class NoFilter(PushFilter):

    def to_json(self):
        return {}


class DeviceFilter(PushFilter):

    def __init__(self, devices):
        """
        A list of device ids or a single device id
        :param devices:
        """
        if type(devices) not in {list, tuple}:
            devices = [devices]

        self.devices = list(devices)

    def to_json(self):
        device_list = list()
        for device in self.devices:
            device_list.append({'device_id': str(device)})

        return {
            'device': device_list
        }


class TagFilter(PushFilter):

    def __init__(self, tags):
        """
        A single tag or a list of tags. if you provide a tag list, push notification will be sent to devices which have
        all of the tags

        :param tags:
        """
        if type(tags) not in {list, tuple}:
            tags = [tags]

        self.tags = tags

    def to_json(self):
        return {
            'tag': self.tags
        }
