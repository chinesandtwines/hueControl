import math, time
from math import radians, tan, sqrt, degrees
from time import sleep
import simplejson as json  
import requests

myhash = "d9ffaca46d5990ec39501bcdf22ee7a1"
appname = "dddd"

h = 1.41218904
k = 0.58682028
r = 1.29822413
angle_init = 65.66
arc_sweep = 35
increment = 0
period = 60
sleep_time = period/arc_sweep

light = 1
huehub = "http://192.168.0.101/api/"+ myhash + "/lights/" + str(light)
reply = requests.get(huehub)
a=json.loads(reply.text)
payload = json.dumps({"xy":[0.22934415, 0.05178395]})
sethuehub = huehub + "/state"
reply = requests.put(sethuehub, data=payload)

#print a

s = raw_input('type \'s\' to start: ')

if s == 's':
    for i in range(arc_sweep):
        angle = 90 - angle_init - increment
        print 'angle = ', angle, '/', 90-angle
        radians = math.radians(angle)
        print 'radians: ', radians
        m = tan(radians)
        print 'm: ', m
        b_int = k - m*h
        print 'b: ', b_int

        a = m**2 + 1
        b = 2*(m*b_int - m*k - h)
        c = k**2 -(r**2) + h**2 - (2*b_int*k) + (b_int**2)
        print 'a: ', a
        print 'b: ', b
        print 'c: ', c
##        print k**2
##        print r**2
##        print h**2
##        print 2*b*k
##        print b**2

        x = round((-b + sqrt(b**2 - 4*a*c))/(2*a), 4)
        print '-b: ', -b
        print 'b**2: ', b**2
        print '4*a*b: ', 4*a*b
        print 'sqrt(b**2 - 4*a*b): ', sqrt(b**2 - 4*a*b)
        print '2*a: ', 2*a
        y = round(m*x+ b_int, 4)
        print '(x, y): ', x, y
        
        x = round((-b - sqrt(b**2 - 4*a*c))/(2*a), 4)
        y = round(m*x+ b_int, 4)
        print '(x, y): ', x, y
        increment = i
        print 'increment: ', increment
        xy = [x, y]

        light = 1
        huehub = "http://192.168.0.101/api/"+ myhash + "/lights/" + str(light)
        reply = requests.get(huehub)
        a=json.loads(reply.text)
        payload = json.dumps({"xy":xy, "transitiontime":1})
        sethuehub = huehub + "/state"
        reply = requests.put(sethuehub, data=payload)

        reply = requests.get(huehub)
        a=json.loads(reply.text)
        print 'xy from light: ', a['state']['xy'], '\n'
            
        sleep(sleep_time)
##        s = raw_input('type anything to continue: ')
##        if len(s) >= 0:
##            pass
