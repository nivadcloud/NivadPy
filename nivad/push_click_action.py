import abc


class ClickAction(abc.ABC):
    @abc.abstractproperty
    def click_action_type(self):
        pass

    @abc.abstractproperty
    def click_action(self):
        pass


class NoAction(ClickAction):
    @property
    def click_action(self):
        return None

    @property
    def click_action_type(self):
        return 'no-action'


class LaunchApplication(ClickAction):

    def __init__(self, package_name=None):
        assert type(package_name) is str
        self.package_name = package_name

    @property
    def click_action(self):
        return self.package_name

    @property
    def click_action_type(self):
        return 'launch_application'


class OpenUrl(ClickAction):

    def __init__(self, url):
        assert url is not None
        assert type(url) == str
        assert len(url) > 0
        self.url = url

    @property
    def click_action(self):
        return self.url

    @property
    def click_action_type(self):
        return 'open_url'


class Telegram(ClickAction):

    def __init__(self, handle):
        assert handle is not None
        assert type(handle) == str
        assert len(handle) > 0

        self.handle = handle

    @property
    def click_action(self):
        return self.handle

    @property
    def click_action_type(self):
        return 'telegram'


class Instagram(ClickAction):
    def __init__(self, handle):
        assert handle is not None
        assert type(handle) == str
        assert len(handle) > 0

        self.handle = handle

    @property
    def click_action(self):
        return self.handle

    @property
    def click_action_type(self):
        return 'instagram'


class _JoinTelegramMixin(ClickAction):

    def __init__(self, link):
        assert link is not None
        assert type(link) == str
        assert len(link) > 0

        self.link = link

    @property
    def click_action_type(self):
        return 'join_telegram'

    @property
    def click_action(self):
        return self.link


class JoinTelegramGroup(_JoinTelegramMixin):
    pass


class JoinTelegramChannel(_JoinTelegramMixin):
    pass