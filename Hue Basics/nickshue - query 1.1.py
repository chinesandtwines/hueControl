import simplejson as json
import requests
import pprint

myhash = "d9ffaca46d5990ec39501bcdf22ee7a1"
appname = "dddd"
light = 1

huehub = "http://192.168.0.102/api/"+ myhash + "/lights/" + str(light)

reply= requests.get (huehub)


#print reply.text
#print '--------------'


a=json.loads(reply.text)



print "name:  " + a['name']

if a['state']['on'] == True :
    print "lamp is ON"
else:
    print "lamp is OFF"

print "hue: " + str(a['state']['hue'])
print "brightness: " + str(a['state']['bri'])
print "saturation: " + str(a['state']['sat'])
print "colour temp: " + str(a['state']['ct'])
print
print "alert:  " + a['state']['alert']
print "effect:  " + a['state']['effect']
#print "transition time:   " + str(a['state']['transitiontime'])
print "xy:   " + str(a['state']['xy'])


