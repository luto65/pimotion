import requests
import sys,getopt
from pimotion import PiMotion
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read('settings.cfg')

def post_image(filename, token, channels):
    f = {'file': (filename, open(filename, 'rb'), 'image/png', {'Expires':'0'})}
    response = requests.post(url='https://slack.com/api/files.upload', data= {'token': token, 'channels': channels, 'media': f}, headers={'Accept': 'application/json'}, files=f)
    return response.text

def callback(path):
    try:
	print post_image(filename=sys.argv[1], token=Config.get('slack','token'), channels =Config.get('slack','channels')
        print "Posted to slack stream %s" % Config.get('slack', 'stream')
    except (RequestException), e:
        print 'ERROR:' + e.message

motion = PiMotion(verbose=True, post_capture_callback=callback)
motion.start()
