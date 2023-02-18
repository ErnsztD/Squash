from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ( NumericProperty, ReferenceListProperty, ObjectProperty )
from kivy.vector import Vector
from kivy.clock import Clock
import random
from kivy.core.window import Window
from kivy.properties import ListProperty

class Ball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    color = ListProperty([1,0,0,])


    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class Player(Widget):
    score = NumericProperty(0)
    color = ListProperty([0,1,0])

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_x - self.center_x) / (self.width / 2)
            bounced = Vector(vx, -1 * vy)
            bounced_vel = bounced # * 1.1
            ball.velocity = bounced_vel.x + offset, bounced_vel.y
            ball.color = self.color



class SquashGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def start_ball(self, vel=(random.randint(4, 8), random.randint(4, 8))):
        self.ball.center = self.center
        self.ball.velocity = vel
        self.ball.color = [1,1,1]
        self.player1.color = [1,0,0]
        self.player2.color = [0,1,0]

    # def start_ball(self, vel=(0, -5)):
    #     self.ball.center = self.center
    #     self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce from sides
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1


        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1

        # bounce from middle wall
        if (self.ball.x > self.width /2 -15) and (self.ball.x < self.width /2 +5) and (self.ball.y <= self.height/3):
            self.ball.velocity_x *= -1
            self.ball.velocity_y *= -1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._keyboard = Window.request_keyboard(None, self)
        if not self._keyboard:
            return
        self._keyboard.bind(on_key_down = self.on_keyboard_down)

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):

        if keycode[1] == 'left':
            self.player2.x -= 10
        elif keycode[1] == 'right':
            self.player2.x += 10
        elif keycode[1] == 'up':
            self.player2.y += 10
        elif keycode[1] == 'down':
            self.player2.y -= 10
        elif keycode[1] == 'a':
            self.player1.x -= 10
        elif keycode[1] == 'd':
            self.player1.x += 10
        else:
            return False
        return True

class SquashApp(App):
    def build(self):
        game = SquashGame()
        game.start_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)

        return game


if __name__ == '__main__':
    SquashApp().run()