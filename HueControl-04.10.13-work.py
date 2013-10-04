import simplejson as json
import requests
from time import sleep
from Tkinter import *
from ttk import Frame, Button, Label, Style, Notebook
import ttk, tkColorChooser, warnings
from colorpy import colormodels

myhash = "d9ffaca46d5990ec39501bcdf22ee7a1"
appname = "dddd"
num_lights = 3

#----------------------------------------------

class hueApp(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):

        self.parent.title("Hue Controller")
        self.createMenu(self.parent)

        Frame.__init__(self, name='test')
        self.pack(expand=Y, fill=BOTH)

        # create frame that will hold the notebook
        nbFrame = Frame(self, name='nbframe')
        nbFrame.pack(side=TOP, fill=BOTH, expand=Y)
        nb = ttk.Notebook(nbFrame, name='notebook')
        nb.enable_traversal()
        nb.pack(fill=BOTH, expand=Y, padx=2, pady=3)

        self.master_tab(nb)
        self.create_light_tabs(nb)
        self.centerWindow
        
#####----- Widget creation -----#####
        
    def createMenu(self, parent):
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar, tearoff=0)

        fileMenu.add_separator()
        
        menubar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label='Reset Brightness', command=self.onBriReset)
        fileMenu.add_command(label='Quit', command=self.onQuit)

    def showMenu(self, e):
        self.menu.post(e.x_root, e.y_root)

    def master_tab(self, nb):
        frame = ttk.Frame(nb, name='descrip')
        nb.add(frame, text='Description', underline=0, padding=2)

        self.button=[]
        for i in range(num_lights):
            self.button.append(Button(frame, text='Pwr #'+str(i+1),
                                      command=lambda i=i: self.pwr_toggle(i+1)))
            #print i
            self.button[i].grid(row=1, column=i, pady=4)

        self.brightness_label=[]
        for i in range(num_lights):
            self.brightness_label.append(Label(frame, text='Brightness'))
            self.brightness_label[i].grid(row=2,column=i)

        self.scale=[]
        for i in range(num_lights):
            self.scale.append(Scale(frame, from_=255, to_=0, variable=i,
                                    command=lambda arg=i, arg2=i+1:
                                    self.brightness_adj(arg, arg2)))
            self.scale[i].set(150)
            self.scale[i].grid(row=3, column=i)

    

    def create_light_tabs(self, nb):

        #create lists for widgets that require a light_id be passed through with command
        self.tabs=[]
        self.colourSelectButton=[]
        self.refreshButton=[]
        self.dataDisplay=[]
        self.periodText=[]
        self.colourStartSelect=[]
        self.startCycle=[]
        
        #create Tab and widgets for each light
        for i in range(num_lights):
            frame = ttk.Frame(nb)
            nb.add(frame, text='Light '+str(i+1))

            try:
                self.colourSelectButton.append(Button(frame, text='Select Colour',
                                      command=lambda i=i: self.colour_select(i+1)))
            except TypeError:
                #ignore error that is raised when window closed instead of choosing a colour
                pass

            self.colourSelectButton[i].grid(row=1, column=0, padx=(4,0), pady=4)
            self.refreshButton.append(Button(frame, text='Refresh',
                                             command=lambda i=i: self.lightDataRefresh(i+1)))
            self.refreshButton[i].grid(row=1, column=1, pady=4, padx=(4,0), sticky=W)
            
            #create Text widget to display light state data
            self.dataDisplay.append(Text(frame, width=20, height=5))
            self.dataDisplay[i].insert('1.0', 'Hue: '+'\n') #+str(a['state']['hue']
            self.dataDisplay[i].insert('2.0', 'Brightness: '+'\n') #+str(a['state']['bri']
            self.dataDisplay[i].insert('3.0', 'Saturation: '+'\n') #+str(a['state']['sat']
            self.dataDisplay[i].insert('4.0', 'Colour Temp: '+'\n') #+str(a['state']['ct']
            self.dataDisplay[i].insert('5.0', '(x, y): ') #+str(a['state']['xy']
            self.dataDisplay[i].grid(row=2, column=0, pady=4, padx=4, columnspan=2)
            self.dataDisplay[i].config(state='disabled')

            #create a divider Frame widget to seperate Colour Selection from Colour Cycle
            div = Frame(frame, width=3, height=110, relief=GROOVE)
            div.grid(row=1, column=3, rowspan=2, padx=5)

            #create widgets to select Period of Colour Cycle
            periodLabel = Label(frame, text='Cycle period (s): ')
            periodLabel.grid(row=1, column=4)
            self.periodText.append(Text(frame, width=3, height=1))
            self.periodText[i].grid(row=1, column=5, padx=(0,6))
            self.periodText[i].insert('1.0', '60')

            #create Listbox widget to display initial colour choices for Colour Cycle
            self.colourStartSelect.append(Listbox(frame, height=5))
            self.colourStartSelect[i].grid(row=2, column=4, columnspan=2)
            self.colourStartSelect[i].bind("<<ListboxSelect>>", self.onSelect)
            self.var = StringVar()
            colourChoices = ['Red', 'Green', 'Blue']
            for j in colourChoices:
                self.colourStartSelect[i].insert(END, j)

            #create Button to begin Colour Cycle using Period and Initial Colour
            self.startCycle.append(Button(frame, text='Start Cycle',
                                          command=lambda arg=i+1: self.cycleLogic(arg)))
            self.startCycle[i].grid(row=3, column=4, columnspan=2)
            

    def centerWindow(self):

        w = 250
        h = 150

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw-w)/2
        y = (sh-h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
            
#####----- Widget commands -----#####

    #####----- Master tab -----#####    
    def onQuit(self):
        self.master.destroy()

    def onBriReset(self):
        bri_val = 150
        for i in range(num_lights):
            light = i+1
            huehub = "http://192.168.0.100/api/"+ myhash + "/lights/" + str(light)
##            reply = requests.get(huehub)
##            a=json.loads(reply.text)
##            if a['state']['on'] == True:
##                payload = json.dumps({"bri":bri_val})
##                sethuehub = huehub + "/state"
##                reply = requests.put(sethuehub, data=payload)
##                self.scale[i].set(150) #reset slider

    def pwr_toggle(self,light_id):
        #print light_id
        light = light_id
        global huehub
        huehub = "http://192.168.0.100/api/"+ myhash + "/lights/" + str(light)
##        reply= requests.get (huehub)
##        a=json.loads(reply.text)
##        
##        if a['state']['on'] == True :
##            print "%s was ON, now turning it off" % a['name']
##            onoff = False
##        else:
##            print "%s was OFF, now turning it on" % a['name']
##            onoff = True
##
##        # --- set new state of bulb
##        payload= json.dumps({"on":onoff})
##        sethuehub = huehub + "/state"
##        reply= requests.put(sethuehub, data=payload)

    def brightness_adj(self, arg, arg2):
        #print 'light_id = ' + str(arg2)
        #print 'light_value = ' + str(arg), '\n'
        light = int(arg2)
        bri_val = int(arg)
        huehub = "http://192.168.0.100/api/"+ myhash + "/lights/" + str(light)
##        reply = requests.get(huehub)
##        a=json.loads(reply.text)
##        payload = json.dumps({"bri":bri_val})
##        sethuehub = huehub + "/state"
##        reply = requests.put(sethuehub, data=payload)


    #####----- Widget commands for create_light_tabs -----#####
    def colour_select(self, light_id):

        try:
            (rgb, hx) = tkColorChooser.askcolor()
            if (rgb, hx) == (None, None):
                warnings.warn('ColorChooser Error: No RGB colour selected.')
    
            else:
                print '(rgb, hx):', rgb, hx
                red = rgb[0]
                green = rgb[1]
                blue = rgb[2]

                redScale = float(red) / 255.0 #rgb goes from 0-255, this changes it into the 0-1.0 that xy uses
                greenScale = float(green) / 255.0
                blueScale = float(blue) / 255.0
                # Initialization function for conversion between CIE XYZ and linear RGB spaces
                colormodels.init(
                    phosphor_red=colormodels.xyz_color(0.64843, 0.33086),
                    phosphor_green=colormodels.xyz_color(0.4091, 0.518),
                    phosphor_blue=colormodels.xyz_color(0.167, 0.04))
                xyz = colormodels.irgb_color(red, green, blue)
                xyz = colormodels.xyz_from_rgb(xyz)
                xyz = colormodels.xyz_normalize(xyz)
                print xyz, '\n'
                xy = [xyz[0], xyz[1]]
                

                #print 'rgb: ', red, green, blue
                #global huehub
                huehub = "http://192.168.0.100/api/"+ myhash + "/lights/" + str(light_id)
##                reply = requests.get(huehub)
##                a=json.loads(reply.text)
##                #print bri_val
##                payload = json.dumps({"xy":xy})
##                sethuehub = huehub + "/state"
##                reply = requests.put(sethuehub, data=payload)
        except TypeError, e:
            print 'Error closing ColorChooser: variable referenced before assignment\n', e, '\n'
            pass

    def lightDataRefresh(self, light_id):
        """
        Get state data from hub.
        """
        huehub = "http://192.168.0.100/api/"+ myhash + "/lights/" + str(light_id)
        print 'Fetching state data from hub'
##        reply = requests.get(huehub)
##        a=json.loads(reply.text)

    def onSelect(self, val):
        """
        Create global variable 'value' that represents the initial colour to be used in the loop.
        """
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)
        self.var.set(value)
        global value
        

    def cycleLogic(self, arg):
        print arg
        print value
        period =  self.periodText[arg-1].get('0.0', 'end-1c')
        print period

def main():
    root = Tk()
    root.resizable(width=False, height=False)
    app = hueApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
