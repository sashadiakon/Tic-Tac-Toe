from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import (Color, Rectangle, Line)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager , Screen
from kivy.uix.popup import Popup
from kivy.uix.image import Image
# from kivy.core.window import Window
from kivy.config import Config
import json
from time import localtime
# height = Window.height
# width = Window.width
height = 800
width = 630
Config.set("graphics", "width", width)
Config.set("graphics", "height", height)
Config.set("graphics", "resizble", 0)
print(height)
pad = 20
spac = 20
h_up = 0.1

h_down = 0.2
h_downp = h_down * height
h_upp = h_up * height
width_btn_field = int((width - 2 * (pad + spac)) / 3)
height_btn_field = int((height - 2 * (pad + spac) - h_downp - h_upp) / 3)
class BackgroundWidget(Widget):
    def __init__(self, **kwargs):
        super(BackgroundWidget, self).__init__(**kwargs)
        with self.canvas:
            Color(.8, .7, 1, 1)
            Rectangle(pos = (0, 0), size = (width, height))
            Color(0, 0, 0, 1)

            spaces_width = pad + int(spac / 2)
            spaces_height = pad + int(spac / 2) + h_downp
            y = spaces_height + height_btn_field
            x = spaces_width + width_btn_field
            Line(points = (x, h_downp + pad + 15, x, \
                         height - h_upp - pad), width = spac / 2)
            Line(points = (pad, y, width - pad, y), width = spac / 2)

            spaces_width = pad + spac * 1.5
            spaces_height = pad + spac * 1.5 + h_downp
            y = spaces_height + height_btn_field * 2
            x = spaces_width + width_btn_field * 2
            Line(points = (x, h_downp + pad + 15, x, \
                         height - h_upp - pad), width=spac / 2)
            Line(points = (pad, y, width - pad, y), width=spac / 2)
class Back(Widget):
    def __init__(self, **kwargs):
        super(Back, self).__init__(**kwargs)
        with self.canvas:
            Color(.8, .7, 1, 1)
            Rectangle(pos = (0,0), size = (width, height))
class DownPanelWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(DownPanelWidget, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.spacing = width/20
        self.padding = width/20
        btn_stat = Button(text = "Last Games",on_press = self.statistic,\
font_size = width/30, background_color = (.5, .75, 1, 1))
        btn_type = Button(text = "Multiple", on_press = self.choose_type,\
font_size = width/30, background_color = (.5, .75, 1, 1))
        self.add_widget(btn_stat)
        self.add_widget(btn_type)
    def go_sett(self, instance):
        global sm
        sm.current = "settings"
    def statistic(self, instance):
        global sm
        sm.current = "history"
    def choose_type(self, instance):
        pass

class HistoryScreen(Screen, BoxLayout):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)
        bll = BoxLayout(orientation = "vertical")
        bl = GridLayout(cols = 3)
        js = json.load(open("history.json"))
        print(js)

        tx = ""
        n = 9
        listt = []
        if len(js)>n:
            for i in range(0, n):
                listt.append(i)
        else:
            for i in range(0, len(js)):
                listt.append(i)
        bl1 = BoxLayout(size_hint = (1, 0.15), orientation = "horizontal")
        bl1.add_widget(Button(text = "Back", on_press = self.go_main, \
size_hint_x = 0.2, font_size = width*0.15/4))
        bl1.add_widget(Label(text = "Last Games:", font_size = width/12))
        bll.add_widget(bl1)
        for i in listt:

            match = js[i]
            field = match[1]

            fl = [field[0][0] + "|" + field[0][1] + "|" + field[0][2], \
field[1][0] + "|" + field[1][1] + "|" + field[1][2], \
field[2][0] + "|" + field[2][1] + "|" + field[2][2]]
            tx =  "\n" + match[2] + "\n" + match[0] + \
"\n     " + fl[0] + "\n     " + fl[1] + "\n     " + fl[2]

            bl.add_widget(Label(text = tx, color = (0,0,0,1), halign = "left", font_size = width/24))
        bll.add_widget(bl)
        self.add_widget(Back())
        self.add_widget(bll)
    def go_main(self, instance):
        global sm
        sm.current = "main"

class MainScreen(Screen, Widget):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        bl = BoxLayout(orientation = "vertical")
        self.grid = GridLayout(cols = 3, rows = 3, spacing = spac, padding = pad, size_hint = (1, 1-h_up-h_down))
        self.btn = Button(text = "", background_color = (.4, .5, 1, 1), on_press = self.end, font_size = 0.4*width/16)
        self.step = "X"
        self.popup = Popup(title = "The end of game", content = self.btn , size_hint = (.4, .2))
        self.lbl_stat = Label(text = "Turn: X!", font_size = int(width/14), size_hint = (1, h_up), color = (0,0,0,1))
        self.field = [["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"]]
        self.win = False
        self.winner = ""
        self.listt = []
        self.free_fields = 9
        self.free_fields = 9
        if width_btn_field >= height_btn_field:
            font = height_btn_field / 1.5
        else:
            font = width_btn_field / 1.5
        for i in range(9):
            btnn = Button( on_press = self.presss, color = (0,0,0,1),\
 font_size = font, background_color = (1,1,1,0))
            self.listt.append(btnn)
            self.grid.add_widget(btnn)
        bl.add_widget(self.lbl_stat)
        bl.add_widget(self.grid)
        bl.add_widget(DownPanelWidget(size_hint = (1, h_down)))
        self.add_widget(BackgroundWidget())
        self.add_widget(bl)
    def presss(self, instance):
        if instance.text == "":#Validation of clear
            # Next figure
            # instance.text = self.step
            n = self.listt.index(instance)
            if instance.text == "":  # Validation of clear
                self.free_fields -= 1
                # Next figure
                instance.text = self.step
                if self.step == "X":
                    instance.color = (.25, .6, 1, 1)
                else:
                    instance.color = (0, 0, 0, 1)

                n = self.listt.index(instance)




            '''This will insert into list.'''
            if n <= 2:
                self.field[0][n] = self.step
            elif 2 < n <= 5:
                self.field[1][n-3] = self.step
            else:
                self.field[2][n-6] = self.step
            print(self.field)
            if self.step == "X":

                self.step = "O"
                self.lbl_stat.text = "Turn: " + self.step
            else:
                self.step = "X"
                self.lbl_stat.text = "Turn: " + self.step

            #Has somebody already won?
            for i in range(3):
                print(i)
                if self.field[0][i] == self.field[1][i] == self.field[2][i] != "*":#Check horizontal
                    self.win = True
                    winner = self.field[0][i]

                elif self.field[i][0] == self.field[i][1] == self.field[i][2] != "*":#Check vertical
                    self.win = True
                    winner = self.field[i][0]

            if self.field[0][0] == self.field[1][1] == self.field[2][2] != "*"\
            or self.field[0][2] == self.field[1][1] == self.field[2][0] != "*":
                self.win = True
                winner = self.field[1][1]
            #If someone won
            if self.win:
                self.btn.text = "The winner is " + winner
                history = json.load(open("history.json"))
                tm = list(map(str, localtime()))
                while len(history)>= 12:
                    history.pop(len(history)-1)
                for i in range(1, 5):
                    if int(tm[i]) < 10:
                        tm[i] = "0" + tm[i]
                history.insert(0, ["Winner: " + winner, self.field, tm[1]+"."+tm[2]+", "+tm[3]+":"+tm[4]])
                with open("history.json", "w") as file:
                    file.write(json.dumps(history))
                self.popup.open()
                self.field = [["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"]]
                self.step = "X"
                self.win = False
                for i in self.listt:
                    i.text = ""
                self.free_fields = 9

            elif self.free_fields == 0:#Draw
                tm = list(map(str, localtime()))
                self.btn.text = "Draw"
                history = json.load(open("history.json"))
                while len(history)>= 12:
                    history.pop(len(history)-1)
                for i in range(1,5):
                    if int(tm[i]) < 10:
                        tm[i] = "0"+tm[i]
                history.insert(0, ["Draw", self.field, tm[1]+"."+tm[2]+", "+tm[3]+":"+tm[4]])
                with open("history.json", "w") as file:
                    file.write(json.dumps(history))
                self.popup.open()
                self.field = [["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"]]
                self.step = "X"
                self.win = False
                for i in self.listt:
                    i.text = ""
                self.free_fields = 9

        else:
            pass
    def end(self, instance):
        self.popup.dismiss()
        for i in self.listt:
            i.text = ""
        self.free_fields = 9

sm = ScreenManager()
sm.add_widget(MainScreen(name = "main"))
sm.add_widget(HistoryScreen(name = "history"))
sm.current = "main"
class My_App(App):
    def build(self):
        global sm
        return sm
My_App().run()