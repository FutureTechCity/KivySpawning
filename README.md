# KivySpawning

This Kivy project demonstrates how to spawn objects such as bullets.

## How it works

Kivy draws three elements: the shot, the barrel, and the turret, in that order. The shot is initially inside the centre of the turret. When the player touches the screen, the program calculates a vector from the turret to the touch point and sets a velocity on the shot matching that vector. (The code must also check that the shot is not already in the air or subsequent touches would change its direction.)

The shot updates its position each frame until it leaves the screen. The position of the shot is then reset to the centre of the turret, and the velocity returned to 0, ready for the next shot.

The barrel is rotated to point in the direction of the target touch. This is done using a rotation matrix.

## Create images

Download the `turret.png` image file or create your own. You will need 3 tiles: a turret, a barrel, and a shot.

## Create atlas file

Create an atlas file to describe the individual sprites on your image file. Create a file `turret.atlas` and paste in the following code in an editor. (If you use Spyder, remember to rename the file after Spyder has saved it because it adds a spurious `.py` to the end of the file name.)

~~~
{
    "turret.png": {
        "turret": [0, 0, 32, 32],
        "barrel": [32, 0, 32, 32],
        "shot":   [64, 0, 32, 32]
    }
}
~~~

If you created your own image file to a different scale you will have to replace the sprite positions and sizes listed in the file above,

## Create your code file

Create a file called `main.py` and copy the following code into it:

~~~
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
~~~

## Create your layout file

Create a file called `spawning.kv` and copy in the following code:

~~~
#:kivy 1.9.0

<SpawningScreen>:
    angle: 0
    shot: turret_shot

    Shot:
        id: turret_shot
        source: 'atlas://turret/shot'
        size: 32, 32
        center: root.width / 2, 0

    Image:
        source: 'atlas://turret/barrel'
        size: 32, 32
        center: root.width / 2, 13
        canvas.before:
            PushMatrix
            Rotate:
                angle: root.angle
                origin: root.width / 2, 0
        canvas.after:
            PopMatrix

    Image:
        source: 'atlas://turret/turret'
        size: 32, 32
        center: root.width / 2, 16
~~~

## Test your program

You should now be able to run your program by entering `python main.py` from the command line. (Don't forget to `activate kivy` first.)

## Challenges

* Add in a target sprite
* Detect collision between the target sprite and the projectile
* Animate your projectile and / or turret
* Rotate your projectile (you'll need a bigger sprite to see this effect)
* Allow more than one bullet in the air at a time
* Add code to guide the projectile towards your touch

## Appendix A: More than one bullet

Here's one way to add multiple simultaneous bullets. The trick is to create an array of duplicate bullet images as a pool and pick a free one to fire with each click. In this code a bullet is considered free if it has zero velocity. All of the bullets are updated on every frame.

The `SpawningScreen` object contains the list which is declared as an empty list `shots = []` which is filled in by the `start` function. Because the `start` function needs to be called after the loading of the `kv` file, it is called using the scheduler with the call `Clock.schedule_once().`

In the `start` function, a clone of template `shot` widget is created for each simultaneous shot. The `clone` function added to the `Shot` class creates a new Shot object and copies the properties one by one from the original. If additional properties are required they would need to be copied as well.

In the `on_touch_down` function we have to find a free shot. We do this by calculating the length of the velocity vector of each shot until we find one with velocity zero. (If there aren't any with velocity zero then they must all be in play and this function will ignore the touch.) When a shot is found and a direction can be determined, the `shoot` function is called on the shot to set its velocity.

In the `update` fucntion we now need to update every bullet. If a bullet is not in play, it will still get an update, but it will remain hidden behind the turret.

Here is the modified code:
~~~
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
~~~
