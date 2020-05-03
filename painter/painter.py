# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.config import Config
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Line
from kivy.clock import Clock
from datetime import datetime, timedelta
from kivy.properties import NumericProperty, ListProperty


Builder.load_file('ui/mainwindow.kv')
Builder.load_file('ui/toolbox.kv')
Builder.load_file('ui/geninfobar.kv')
Builder.load_file('ui/drawingspace.kv')
Builder.load_file('ui/generaloptions.kv')
Builder.load_file('ui/statusbar.kv')


class MainWindow(AnchorLayout):
    """Provide main window and organize widgets in window"""
    pass


class DraggableWidget(RelativeLayout):
    def __init__(self, **kwargs):
        self.selected = None
        super(DraggableWidget, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.select()
            return True
        return super(DraggableWidget, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        (x,y) = self.parent.to_parent(touch.x, touch.y)
        if self.selected and self.parent.collide_point(x - self.width/2, y - self.height/2):
            self.translate(touch.x-self.ix, touch.y-self.iy)
            return True
        return super(DraggableWidget, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.selected:
            self.unselect()
            return True
        return super(DraggableWidget, self).on_touch_up(touch)

    def select(self):
        if not self.selected:
            self.ix = self.center_x
            self.iy = self.center_y
            with self.canvas:
                self.selected = Line(rectangle=(0, 0, self.width,self.height), dash_offset=2)

    def unselect(self):
        if self.selected:
            self.canvas.remove(self.selected)
            self.selected = None

    def translate(self, x, y):
        self.center_x = self.ix = self.ix + x
        self.center_y = self.iy = self.iy + y


class StickMan(DraggableWidget):
    pass


class ToolButton(ToggleButton):
    def on_touch_down(self, touch):
        ds = self.parent.drawing_space
        if self.state == 'down' and ds.collide_point(touch.x, touch.y):
            (x, y) = ds.to_widget(touch.x, touch.y)
            self.draw(ds, x, y)
            return True
        return super(ToolButton, self).on_touch_down(touch)

    def draw(self, ds, x, y):
        pass


class ToolStickMan(ToolButton):
    def draw(self, ds, x, y):
        sm = StickMan(width=48, height=48)
        sm.center = (x, y)
        ds.add_widget(sm)


class GeneralOptions(BoxLayout):
    group_mode = False
    translation = ListProperty(None)

    def clear(self, instance):
        self.drawing_space.clear_widgets()


class Painter(App):
    """The entrance of App

    This class is a subclass of kivy App class, it has a built-in run()
    method to start the App.
    In this App, there are four core components:
        Data(): data object are shared and sync with all plugins
        WidgetManager(): Provide window and organize widgets in window
        DisplayManager(): Monitor data changes and update contents in widgets
        PluginManager(): Load and manage plugins
    Attributes:
        title: the title shown on the window
        data: object, the data object will be shared and sync with all plugins
        plugins: dict, the collection of loaded Plugins
    """
    def build(self):
        return MainWindow()


if __name__ == '__main__':
    Config.set('graphics', 'width', '960')
    Config.set('graphics', 'height', '540')  # 16:9

    from kivy.core.window import Window
    Window.clearcolor = get_color_from_hex('#000000')

    LabelBase.register(name='Font Awesome Solid',
                       fn_regular='fonts/fa-solid-900.ttf')

    Painter().run()
