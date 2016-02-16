'''
    Wrapper to the MPDClient methods calls
    This supports graceful handling of errors
'''
from kivy.logger import Logger
import mpd

class MpcWrapper(object):

    ''' Write the status to Logger.debug on every call
    This will generate a lot of logging info'''
    debug_status = False

    '''MPDClient object'''
    mpc = False

    '''MPD Host'''
    host = '127.0.0.1'

    '''MPD Port'''
    port = 6600

    def __init__(self, **kwargs):
        Logger.info("mpcwrapper: Init")
        super(MpcWrapper, self).__init__()

        self.host = kwargs.get('host', self.host)
        self.port = kwargs.get('port', self.port)
        retries = kwargs.get('retries', 10)
        timeout = kwargs.get('timeout', 1)

        self.connect(retries=retries,timeout=timeout)

    """ 
    Connect to MPD host. Will pause and retry connection if unsuccessful

    :param host: MPD Host. Default 127.0.0.1
    :param port: MPD Port. Default 6600
    :param retry: Retry attempts. Default 10
    :param timeout: Wait timeout between retry attempts. Default 1 (second).
    """
    def connect(self, **kwargs):

        retries = kwargs.get('retires', 10)
        timeout = kwargs.get('timeout', 1)        

        try:
            self.mpc = mpd.MPDClient()
            self.mpc.connect(self.host, self.port)
        except:
            if (retries > 0):
                retries-=1;
                return self.connect(retries=retries, timeout=timeout);
            else:
                Logger.error('mpcwrapper: Failed to connect to MPD server after {} tries.')
                raise

        return True


    """
    Interface to MPDClient.lsinfo

    Returns a list of albums / songs and playlists for the given URI

    :param uri: The resource indicator. Default: /
    """
    def lsinfo(self, item):
        return self.mpc.lsinfo(item)

    def __getattr__(self, key):
        return getattr(self.mpc, key)


