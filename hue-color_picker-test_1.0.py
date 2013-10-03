import simplejson as json  
import requests         # submits http requests
from time import sleep  # for future use
from Tkinter import *
from ttk import Frame, Button, Label, Style, Notebook
import tkColorChooser

# MD5 hash from  http://www.miraclesalad.com/webtools/md5.php
myhash = "d9ffaca46d5990ec39501bcdf22ee7a1"
appname = "dddd"    # name content isnt relevant
num_lights = int(3)

class hueApp(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    

    def initUI(self, *args, **kwds):
        
        # title the app window
        self.parent.title("Hue controller")
        self.style = Style() 

        # create grid layout
        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)
        self.columnconfigure(4, pad=3)
        
        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)

        self.button=[]
        for i in range(0,num_lights):
            self.button.append(Button(self, text='Colour Select'+str(i+1), command=lambda i=i: self.colour_select(i+1)))
            #print i
            self.button[i].grid(row=1, column=i)
        
        self.centerWindow
        self.pack()

    def colour_select(self, light_id):
        print 'light_id:', light_id, type(light_id)
        (rgb, hx) = tkColorChooser.askcolor()
        print '(rgb, hx):', rgb, hx

        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]

        redScale = float(red) / 255.0 #rgb goes from 0-255, this changes it into the 0-1.0 that xy uses
        greenScale = float(green) / 255.0
        blueScale = float(blue) / 255.0

        print 'rgb: ', red, green, blue
        #global huehub
        huehub = "http://192.168.0.100/api/"+ myhash + "/lights/" + str(light_id)
        reply = requests.get(huehub)
        a=json.loads(reply.text)
        #print bri_val
        payload = json.dumps({"bri":bri_val})
        sethuehub = huehub + "/state"
        reply = requests.put(sethuehub, data=payload)

    def centerWindow(self):

        w = 250
        h = 150

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw-w)/2
        y = (sh-h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

def main():
    root=Tk() #the root window is created
    app=hueApp(root) #create an instance of the application class

    root.mainloop()  

if __name__ == '__main__':
        main()
