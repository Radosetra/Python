import kivy

# resolve the opengl version
from kivy import Config
Config.set('graphics', 'multisamples', '0')
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

# UI element
from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton

from kivy.graphics import Rectangle, Color, Line 

from kivy.properties import ObjectProperty

# main interface

# element of functionalities
class EditRGBA(GridLayout):
    def __init__(self,**kwargs):
        super(EditRGBA,self).__init__(**kwargs)
        self.cols = 2

        self.add_widget(Label(text="R:", size_hint=(0.8,0.20)))
        self.selectR = Slider(min=0,max=255,step=1)
        self.add_widget(self.selectR)

        self.add_widget(Label(text="G:", size_hint=(0.8,0.20)))
        self.selectG = Slider(min=0,max=255,step=1)
        self.add_widget(self.selectG)

        self.add_widget(Label(text="B:", size_hint=(0.8,0.20)))
        self.selectB = Slider(min=0,max=255,step=1)
        self.add_widget(self.selectB)

        self.add_widget(Label(text="A:", size_hint=(0.8,0.20)))
        self.selectA= Slider(min=0,max=255,step=1,value=125)
        self.add_widget(self.selectA)

class EditWidth(GridLayout):
    def __init__(self,**kwargs):
        super(EditWidth,self).__init__(**kwargs)

        self.cols = 2
        self.add_widget(Label(text="Width:", size_hint=(0.8,0.20)))
        self.selectW = Slider(min=0,max=10,step=1)
        self.add_widget(self.selectW)

class Erase(GridLayout):
    def __init__(self,**kwargs):
        super(Erase,self).__init__(**kwargs)

        self.cols = 1
        self.btn = ToggleButton(text="Erase")
        self.add_widget(self.btn)

class Clear(GridLayout):
    def __init__(self,**kwargs):
        super(Clear,self).__init__(**kwargs)

        self.cols = 1
        self.btn = Button(text="Clear")
        self.add_widget(self.btn)

    def canvasClear(editor):
        editor.canvas.clear()

class Setting(BoxLayout):
    def __init__(self,**kwargs):
        super(Setting,self).__init__(**kwargs)

        self.orientation = "vertical"

        self.EditRGBA = EditRGBA()
        self.add_widget(self.EditRGBA)

        self.EditWidth = EditWidth()
        self.add_widget(self.EditWidth)

        self.Erase = Erase()
        self.add_widget(self.Erase)

        self.Clear = Clear()
        self.add_widget(self.Clear)


# editor
class DrawerEditor(Widget):
    def __init__(self, **kwargs):
        super(DrawerEditor, self).__init__(**kwargs)

        self.r = 0
        self.g = 0
        self.b = 0
        self.a = 125

        self.lineW = 2

        self.eraserMode = False

        with self.canvas:
            self.color = Color(self.r,self.g,self.b,self.a)
            self.line = Line(points=[], width=2)
    
    def on_touch_down(self, touch):
        # touch may be the space you touch with your mouse

        super(DrawerEditor, self).on_touch_down(touch)

        if (not self.collide_point(*touch.pos)) and not self.eraserMode:
            return
        elif self.collide_point(*touch.pos) and self.eraserMode:
            with self.canvas:
                self.color = Color(0,0,0,1)
                self.line = Line(points=[touch.pos[0],touch.pos[1]], width=self.lineW)
        else :
            with self.canvas:
                self.color = Color(self.r,self.g,self.b,self.a)
                self.line = Line(points=[touch.pos[0],touch.pos[1]], width=self.lineW)
        

    def on_touch_move(self, touch):
        # self.rect.pos = touch.pos
        if not self.collide_point(*touch.pos):
            return

        self.line.points = self.line.points + [touch.pos[0], touch.pos[1]]
    
    def set_line_color(self, rgba):
        self.r = rgba[0]
        self.g = rgba[1]
        self.b = rgba[2]
        self.a = rgba[3]
        print(rgba)
    
    def set_new_width(self, userWidth):
        self.lineW = userWidth
    
    def set_eraserMode(self):
        self.eraserMode = not self.eraserMode
        if self.eraserMode:
            self.color = Color(0,0,0,1)

class MyInterface(BoxLayout):
    def __init__(self, **kwargs):
        super(MyInterface, self).__init__(**kwargs)
        self.orientation = "horizontal"

        self.DrawerEditor = DrawerEditor()
        self.add_widget(self.DrawerEditor)

        self.Setting = Setting()
        self.Setting.EditRGBA.selectR.bind(value=self.on_color_change)
        self.Setting.EditRGBA.selectG.bind(value=self.on_color_change)
        self.Setting.EditRGBA.selectB.bind(value=self.on_color_change)
        self.Setting.EditRGBA.selectA.bind(value=self.on_color_change)

        self.Setting.EditWidth.selectW.bind(value=self.on_width_change)
        self.add_widget(self.Setting)

        # add An Event to the btn
        self.Setting.Clear.btn.bind(on_press=self.canvasClear)

        # 
        self.Setting.Erase.btn.bind(on_press=self.erase)
        

    def on_color_change(self, instance, value):
        rgba = [self.Setting.EditRGBA.selectR.value, self.Setting.EditRGBA.selectG.value,self.Setting.EditRGBA.selectB.value,self.Setting.EditRGBA.selectA.value]
        self.DrawerEditor.set_line_color(rgba)

    def on_width_change(self, instance, value):
        w = self.Setting.EditWidth.selectW.value
        self.DrawerEditor.set_new_width(w)


    def canvasClear(self, instance):
        tmpColor = self.DrawerEditor.color.rgba

        self.DrawerEditor.canvas.clear()
        with self.DrawerEditor.canvas:
            self.DrawerEditor.color = Color(*tmpColor)
            self.DrawerEditor.line = Line(points=[], width=self.DrawerEditor.lineW)

    def erase(self,instance):
        self.DrawerEditor.set_eraserMode()


class MyApp(App):
    def build(self):
        return MyInterface()

if __name__ == "__main__":
    MyApp().run()
