from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.vector import Vector

class Shot(Image):
    velocity = Vector(0, 0)
    shot_speed = 600
    def clone(self):
        clone = Shot()
        clone.id = self.id
        clone.source = self.source
        clone.allow_stretch = self.allow_stretch
        clone.size = self.size
        clone.center = self.center
        return clone
    
    def update(self, dt):
        position = Vector(self.center) + self.velocity * dt
        if (position.x < 0 or position.x > self.parent.width or position.y < 0 or position.y > self.parent.height):
            self.velocity = Vector(0, 0)
            position = Vector(self.parent.width / 2, 0)
        self.center = position
        
    def shoot(self, direction):
        self.velocity = direction * self.shot_speed

class SpawningScreen(Widget):
    shot = ObjectProperty(None)
    shots = []
    total_shots = 3
    angle = NumericProperty(0)
    target = Vector(0, 0)
    def start(self, time):
        self.shot.center = Vector(self.width / 2, 0)
        for index in range(0, self.total_shots):
            shot = self.shot.clone()
            self.shots.append(shot)
            self.add_widget(shot, len(self.children))
    
    def update(self, dt):
        angle = (self.target - Vector(self.width / 2, 0)).angle((0, 100))
        self.angle = angle
        for shot in self.shots:
            shot.update(dt)
        
    def on_touch_down(self, touch):
        for shot in self.shots:
            velocity = shot.velocity
            if (velocity.length2() == 0):
                self.target = Vector(touch.x, touch.y)
                v = self.target - Vector(self.width / 2, 0)
                if (v.length2() > 0):
                    direction = v.normalize()
                    shot.shoot(direction)
                break

class SpawningApp(App):
    def build(self):
        spawning = SpawningScreen()
        Clock.schedule_once(spawning.start, 0)
        Clock.schedule_interval(spawning.update, 1.0/60.0)
        return spawning

if __name__ == '__main__':
    SpawningApp().run()
