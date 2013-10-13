from kivy.config import Config
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '400')
Config.set('graphics', 'resizable', 0)
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty

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

    #def get_value(

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
        rgba = self.color_picker1.wheel.color
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
        print xyz, '\n'
        xy = [xyz[0], xyz[1]]
        huehub = 'http://' + ip + '/api/'+ myhash + "/lights/" + str(light_id)
        reply = requests.get(huehub)
        a=json.loads(reply.text)
        #print bri_val
        payload = json.dumps({"xy":xy})
        sethuehub = huehub + "/state"
        reply = requests.put(sethuehub, data=payload)

class HueController(App):
    def build(self):
        return hueLayout()
    #Import .kv layout file
    Builder.load_file('hueLayout.kv')

if __name__ == '__main__':
    
    Config.write()
    HueController().run()
