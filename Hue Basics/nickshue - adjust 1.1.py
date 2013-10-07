import simplejson as json  
import requests         # submits http requests
from time import sleep  # for future use

# MD5 hash from  http://www.miraclesalad.com/webtools/md5.php
myhash = "d9ffaca46d5990ec39501bcdf22ee7a1"

appname = "dddd"    # name content isnt relevant

light = 1           # this is the Hue bulb we are working with


# --- get status of bulb
huehub = "http://192.168.0.101/api/"+ myhash + "/lights/" + str(light)
print huehub
print

reply= requests.get (huehub)
print reply
print

a=json.loads(reply.text)
print a
print a['state']
if a['state']['on'] == True :
    print "lamp was ON, now turning it off"
    onoff = False
else:
    print "lamp was OFF, now turning it on"
    onoff = True




# --- set new state of bulb

payload= json.dumps({"on":onoff})

sethuehub = huehub + "/state"

reply= requests.put (sethuehub, data=payload)


