from pimotion import PiMotion
from cloudapp import CloudAppAPI
from m2x.client import M2XClient
from m2x.errors import APIError
from requests.exceptions import HTTPError
import ConfigParser


Config = ConfigParser.ConfigParser()
Config.read('settings.cfg')


def callback(path):
    api = CloudAppAPI(Config.get('cloudapp', 'username'), Config.get('cloudapp', 'password'))
    url = api.upload(path)
    print 'Public URL: ' + url

    try:
        client = M2XClient(Config.get('m2x', 'api_key'))
        feed = client.feeds.details(Config.get('m2x', 'feed_id'))
        result = feed.add_values({Config.get('m2x', 'stream'): [{'value': url}]})
        print "Posted URL to M2X channel %s" % Config.get('m2x', 'stream')
    except HTTPError, e:
        print 'ERROR' + e.message
    except APIError, e:
        errors = ', '.join("%s: %r" % (key, val) for (key, val) in e.errors.iteritems())
        print "ERROR: %s - %s" % (e.message, errors)

motion = PiMotion(verbose=True, post_capture_callback=callback)
motion.start()
