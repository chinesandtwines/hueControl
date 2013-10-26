from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', 0)
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.image import Image

import simplejson as json
import requests
from time import sleep
from urllib2 import urlopen
from colorpy import colormodels

myhash = "d9ffaca46d5990ec39501bcdf22ee7a1"
appname = "dddd"
num_lights = 3

#####----- Determine bridge IP address -----#####
data = urlopen("http://www.meethue.com/api/nupnp")
web_pg = data.read()

def findOccurences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

char_list = findOccurences(web_pg, '\"')
ip = web_pg[char_list[-2]+1:char_list[-1]]  

#####----- App Logic -----#####

class cieBackground(Image):
    pass

class ColorLoopWidget(Widget):
    xlabel = ObjectProperty
    ylabel = ObjectProperty
    def on_touch_down(self, touch):
        with self.canvas:
            self.canvas.clear()
            d = 10
            Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d,d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))
            self.xlabel.text = 'x: '+str(touch.x)
            self.ylabel.text = 'y: '+str(touch.y)

class hueLayout(BoxLayout):
    pwr1_switch = ObjectProperty()
    pwr2_switch = ObjectProperty()
    pwr3_switch = ObjectProperty()

    bri1_label = ObjectProperty()
    bri2_label = ObjectProperty()
    bri3_label = ObjectProperty()    
    
    bri1_slider = ObjectProperty()
    bri2_slider = ObjectProperty()
    bri3_slider = ObjectProperty()

    color_picker1 = ObjectProperty()
    color_picker2 = ObjectProperty()
    color_picker3 = ObjectProperty()

    hue_label1 = ObjectProperty()
    bri_label1 = ObjectProperty()
    sat_label1 = ObjectProperty()
    ct_label1 = ObjectProperty()
    xy_label1 = ObjectProperty()

    hue_label2 = ObjectProperty()
    bri_label2 = ObjectProperty()
    sat_label2 = ObjectProperty()
    ct_label2 = ObjectProperty()
    xy_label2 = ObjectProperty()

    hue_label3 = ObjectProperty()
    bri_label3 = ObjectProperty()
    sat_label3 = ObjectProperty()
    ct_label3 = ObjectProperty()
    xy_label3 = ObjectProperty()

    light1_label = ObjectProperty()
    light2_label = ObjectProperty()
    light3_label = ObjectProperty()

    colorloopwidget = ObjectProperty()
    xlabel = ObjectProperty()
    ylabel = ObjectProperty()

    def init_lights(self):    
        for light_id in range(1,4):
            #print light_id
            if light_id == 1:
                huehub = 'http://' + ip + '/api/'+ myhash + "/lights/" + str(light_id)
                xy = (0.167, 0.04)
                payload = json.dumps({"xy":xy})
                sethuehub = huehub + "/state"
                reply = requests.put(sethuehub, data=payload)
                reply = requests.get(huehub)
                a=json.loads(reply.text)
                self.light1_label.text = a['name']
            
            if light_id == 2:
                huehub = 'http://' + ip + '/api/'+ myhash + "/lights/" + str(light_id)
                xy = (0.167, 0.04)
                payload = json.dumps({"xy":xy})
                sethuehub = huehub + "/state"
                reply = requests.put(sethuehub, data=payload)
                reply = requests.get(huehub)
                a=json.loads(reply.text)
                self.light2_label.text = a['name']
              
            if light_id == 3:
                huehub = 'http://' + ip + '/api/'+ myhash + "/lights/" + str(light_id)
                xy = (0.167, 0.04)
                payload = json.dumps({"xy":xy})
                sethuehub = huehub + "/state"
                reply = requests.put(sethuehub, data=payload)
                reply = requests.get(huehub)
                a=json.loads(reply.text)
                self.light3_label.text = a['name']            

    def get_state(self, light_id):
        huehub = 'http://' + ip + '/api/'+ myhash + "/lights/" + str(light_id)
        reply= requests.get (huehub)
        a=json.loads(reply.text)       
        if a['state']['on'] == True :
            return True
        else:
            return False

    def pwr_toggle(self, instance, value, light_id):
        light = light_id
        huehub = 'http://' + ip + '/api/'+ myhash + "/lights/" + str(light)
        reply= requests.get (huehub)
        a=json.loads(reply.text)
        
        if a['state']['on'] == True :
            print "%s was ON, now turning it off" % a['name']
            onoff = False
        else:
            print "%s was OFF, now turning it on" % a['name']
            onoff = True

        payload= json.dumps({"on":onoff})
        sethuehub = huehub + "/state"
        reply= requests.put(sethuehub, data=payload)

    def bri_adj(self, instance, value, light_id):
        bri_val = int(value)
        if light_id == 1:    
            self.bri1_label.text = 'Brightness: ' + str(bri_val)
        elif light_id == 2:
            self.bri2_label.text = 'Brightness: ' + str(bri_val)
        elif light_id == 3:
            self.bri3_label.text = 'Brightness: ' + str(bri_val)
        huehub = 'http://' + ip + '/api/'+ myhash + "/lights/" + str(light_id)
        reply = requests.get(huehub)
        a=json.loads(reply.text)
        payload = json.dumps({"bri":bri_val})
        sethuehub = huehub + "/state"
        reply = requests.put(sethuehub, data=payload)

    def color_adj(self, light_id):
        if light_id == 1:    
            rgba = self.color_picker1.wheel.color
        elif light_id == 2:
            rgba = self.color_picker2.wheel.color
        elif light_id == 3:
            rgba = self.color_picker2.wheel.color
        red = rgba[0]
        green = rgba[1]
        blue = rgba[2]

        colormodels.init(
            phosphor_red=colormodels.xyz_color(0.64843, 0.33086),
            phosphor_green=colormodels.xyz_color(0.4091, 0.518),
            phosphor_blue=colormodels.xyz_color(0.167, 0.04))
        xyz = colormodels.irgb_color(red, green, blue)
        xyz = colormodels.xyz_from_rgb(xyz)
        xyz = colormodels.xyz_normalize(xyz)
        #print xyz, '\n'
        xy = [xyz[0], xyz[1]]
        huehub = 'http://' + ip + '/api/'+ myhash + "/lights/" + str(light_id)
        reply = requests.get(huehub)
        a=json.loads(reply.text)
        #print bri_val
        payload = json.dumps({"xy":xy})
        sethuehub = huehub + "/state"
        reply = requests.put(sethuehub, data=payload)

        #Update hue data printout
        reply= requests.get(huehub)
        a=json.loads(reply.text)

        if light_id == 1:    
            self.hue_label1.text = 'Hue :'+str(a['state']['hue'])
            self.bri_label1.text = 'Brightness :'+str(a['state']['bri'])
            self.sat_label1.text = 'Saturation :'+str(a['state']['sat'])
            self.ct_label1.text = 'Colour Temp :'+str(a['state']['ct'])
            self.xy_label1.text = '(x, y) :'+str(a['state']['xy'])
        elif light_id == 2:
            self.hue_label2.text = 'Hue :'+str(a['state']['hue'])
            self.bri_label2.text = 'Brightness :'+str(a['state']['bri'])
            self.sat_label2.text = 'Saturation :'+str(a['state']['sat'])
            self.ct_label2.text = 'Colour Temp :'+str(a['state']['ct'])
            self.xy_label2.text = '(x, y) :'+str(a['state']['xy'])
        elif light_id == 3:
            self.hue_label3.text = 'Hue :'+str(a['state']['hue'])
            self.bri_label3.text = 'Brightness :'+str(a['state']['bri'])
            self.sat_label3.text = 'Saturation :'+str(a['state']['sat'])
            self.ct_label3.text = 'Colour Temp :'+str(a['state']['ct'])
            self.xy_label3.text = '(x, y) :'+str(a['state']['xy'])
        
    def clear_canvas(self):
        self.colorloopwidget.canvas.clear()        

class HueController(App):
              
    def build(self):
        app = hueLayout()
        app.init_lights()
        return app
    
    #Import .kv layout file
    Builder.load_file('hueLayout.kv')

if __name__ == '__main__':    
    Config.write()
    HueController().run()
