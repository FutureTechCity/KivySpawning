from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.vector import Vector

class Shot(Image):
    velocity = Vector(0, 0)
    def update(self, dt):
        position = Vector(self.center) + self.velocity
        if (position.x < 0 or position.x > self.parent.width or position.y < 0 or position.y > self.parent.height):
            self.velocity = Vector(0, 0)
            position = Vector(self.parent.width / 2, 0)
        self.center = position

class SpawningScreen(Widget):
    shot = ObjectProperty(None)
    angle = NumericProperty(0)
    target = Vector(0, 0)
    def update(self, dt):
        angle = (self.target - Vector(self.width / 2, 0)).angle((0, 100))
        self.angle = angle
        self.shot.angle = angle
        self.shot.update(dt)
        
    def on_touch_down(self, touch):
        velocity = self.shot.velocity
        if (velocity.length2() == 0):
            self.target = Vector(touch.x, touch.y)
            v = self.target - Vector(self.width / 2, 0)
            if (v.length2() > 0):
                self.shot.velocity = v.normalize() * 10

class SpawningApp(App):
    def build(self):
        spawning = SpawningScreen()
        Clock.schedule_interval(spawning.update, 1.0/60.0)
        return spawning

if __name__ == '__main__':
    SpawningApp().run()
