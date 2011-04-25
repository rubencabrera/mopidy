from mopidy import settings
from mopidy.gstreamer import BaseOutput

class LocalOutput(BaseOutput):
    def describe_bin(self):
        if settings.LOCALOUTPUT_OVERRIDE:
            return settings.LOCALOUTPUT_OVERRIDE
        return 'autoaudiosink'

class NullOutput(BaseOutput):
    def describe_bin(self):
        return 'fakesink'

class ShoutcastOutput(BaseOutput):
    def describe_bin(self):
        if settings.SHOUTCAST_OVERRIDE:
            return settings.SHOUTCAST_OVERRIDE

        return 'audioconvert ! %s ! shout2send name=shoutcast' \
            % settings.SHOUTCAST_ENCODER

    def modify_bin(self, output):
        shoutcast = output.get_by_name('shoutcast')
        properties = {
            u'ip': settings.SHOUTCAST_SERVER,
            u'mount': settings.SHOUTCAST_MOUNT,
            u'port': settings.SHOUTCAST_PORT,
            u'username': settings.SHOUTCAST_USER,
            u'password': settings.SHOUTCAST_PASSWORD,
        }

        for key, value in properties.items():
            if value:
                shoutcast.set_property(key, value)
