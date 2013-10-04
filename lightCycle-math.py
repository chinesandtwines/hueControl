import math, time
from math import radians, tan, sqrt
from time import sleep
import simplejson as json  
import requests

myhash = "d9ffaca46d5990ec39501bcdf22ee7a1"
appname = "dddd"

h = 0.7082
k = 0.4818
r = 1.2982
angle_init = 65.66
arc_sweep = 33
increment = 0
period = 60
sleep_time = period/arc_sweep

light = 1
huehub = "http://192.168.0.100/api/"+ myhash + "/lights/" + str(light)
reply = requests.get(huehub)
a=json.loads(reply.text)
payload = json.dumps({"xy":[2.093099722, -1.03889538284]})
sethuehub = huehub + "/state"
reply = requests.put(sethuehub, data=payload)

print a

s = raw_input('type \'s\' to start: ')

if s == 's':
    for i in range(arc_sweep):
        angle = 90 - angle_init + increment
        print 'angle = ', angle, '/', 90-angle
        radians = math.radians(angle)
        m = tan(angle)
        b = k - m*h

        a = m**2 + 1
        b = 2*(m*b - m*k - h)
        c = k**2 -r**2 + h**2 - 2*b*k + b**2

        x = round((-b + sqrt(b**2 - 4*a*b))/(2*a), 1)
        y = round(m*x+ b, 1)
        print '(x, y): ', x, y
        increment = i
        xy = [x, y]

        light = 1
        huehub = "http://192.168.0.100/api/"+ myhash + "/lights/" + str(light)
        reply = requests.get(huehub)
        a=json.loads(reply.text)
        payload = json.dumps({"xy":xy, "transitiontime":1})
        sethuehub = huehub + "/state"
        reply = requests.put(sethuehub, data=payload)
            
        #sleep(sleep_time)
        s = raw_input('type anything to continue')
        if len(s) >= 0:
            huehub = "http://192.168.0.100/api/"+ myhash + "/lights/" + str(light)
            reply = requests.get(huehub)
            a=json.loads(reply.text)
            print 'xy from light: ', a['state']['xy']
            pass
