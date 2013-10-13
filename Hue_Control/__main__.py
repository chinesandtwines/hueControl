from kivy.config import Config
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '300')
Config.set('graphics', 'resizable', 0)
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty

import simplejson as json
import requests
from time import sleep
from urllib2 import urlopen

myhash = "d9ffaca46d5990ec39501bcdf22ee7a1"
appname = "dddd"
num_lights = 3

#####----- Determine bridge IP address -----#####
data = urlopen("http://www.meethue.com/api/nupnp")
web_pg = data.read()

def findOccurences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

char_list = findOccurences(web_pg, '\"')
print char_list
ip = web_pg[char_list[-2]+1:char_list[-1]]



#####----- App Logic -----#####

class hueLayout(BoxLayout):
    pwr1_switch = ObjectProperty()
    switch_toggle = ObjectProperty()
    bri1_slider = ObjectProperty()
    bri2_slider = ObjectProperty()
    bri3_slider = ObjectProperty()

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
##        if light_id == 1:    
##            bri_val = int(self.bri1_slider.value)
##        elif light_id == 2:
##            bri_val = int(self.bri2_slider.value)
##        elif light_id == 3:
##            bri_val = int(self.bri3_slider.value)
        bri_val = int(value)
        huehub = 'http://' + ip + '/api/'+ myhash + "/lights/" + str(light_id)
        reply = requests.get(huehub)
        a=json.loads(reply.text)
        payload = json.dumps({"bri":bri_val})
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
