from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, \
     ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

clock_int = 1.0 / 60.0
grav = 5 #m/s^2
global elapsed_time


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    ball = ObjectProperty(None)
    

    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(2, 2)

    def update(self, dt):

        if (self.ball.y <0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -0.95

        elif (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1

        else:
            self.ball.velocity_y += -grav*(Clock.get_boottime()**2)

        self.ball.move()

class PongApp(App):
        
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, clock_int)
        return game

if __name__ == '__main__':
    PongApp().run()
