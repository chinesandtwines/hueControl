import math, time
from math import radians, tan, sqrt, degrees
from time import sleep
import simplejson as json  
import requests

import matplotlib.pyplot as plt
myhash = "d9ffaca46d5990ec39501bcdf22ee7a1"
appname = "dddd"

h = 1.41218904
k = 0.58682028
r = 1.29822413
angle_init = 65.66
arc_sweep = 35
increment = 0
period = 30
sleep_time = period/arc_sweep

light = 1
huehub = "http://192.168.0.101/api/"+ myhash + "/lights/" + str(light)
reply = requests.get(huehub)
huedata=json.loads(reply.text)
payload = json.dumps({"xy":[0.229, 0.0518]})
sethuehub = huehub + "/state"
reply = requests.put(sethuehub, data=payload)

#print a

s = raw_input('type \'s\' to start: ')

if s == 's':
    curve_data_x = []
    curve_data_y = []
    for i in range(arc_sweep+1):
        angle = 90 - angle_init - increment        
        radians = math.radians(angle)        
        m = tan(radians)        
        b_int = k - m*h
        
        a = m**2 + 1
        b = 2*(m*b_int - m*k - h)
        c = k**2 -(r**2) + h**2 - (2*b_int*k) + (b_int**2)        
        x = round((-b - sqrt(b**2 - 4*a*c))/(2*a), 3)        
        y = round(m*x+ b_int, 3)
        curve_data_x.append(x)
        curve_data_y.append(y)
        print '(x, y): ', x, y
        
        increment = i
        print 'increment: ', increment, '/', arc_sweep, '\n'
        xy = [x, y]
        

        light = 1
        huehub = "http://192.168.0.101/api/"+ myhash + "/lights/" + str(light)
        reply = requests.get(huehub)
        huedata=json.loads(reply.text)
        payload = json.dumps({"xy":xy, "transitiontime":1})
        sethuehub = huehub + "/state"
        reply = requests.put(sethuehub, data=payload)

        reply = requests.get(huehub)
        huedata=json.loads(reply.text)
        if round(xy[0],1) != round(huedata['state']['xy'][0], 1) and \
                 round(xy[1], 1) != round(huedata['state']['xy'][1], 1):
            print 'angle = ', angle, '/', 90-angle
            print 'radians: ', radians
            print 'm: ', m
            print 'b: ', b_int
            print 'a: ', a
            print 'b: ', b
            print 'c: ', c
            print '-b: ', -b
            print 'b**2: ', b**2
            print '4*a*b: ', 4*a*b
            print 'sqrt(b**2 - 4*a*b): ', sqrt(b**2 - 4*a*b)
            print '2*a: ', 2*a
            print '(x, y): ', x, y
            print 'xy from light: ', huedata['state']['xy'], '\n'
        sleep(sleep_time)

        if i == arc_sweep:
            print 'done'
            #print curve_data_x, '\n'
            #print curve_data_y, '\n'
            im = plt.imread('C:\Users\Nick\Documents\Git\hueControl\Hue_Control\cie-colorspace_cropped.png')
            implot = plt.imshow(im)
            plt.plot(curve_data_x, curve_data_y)
            plt.show()
            break
