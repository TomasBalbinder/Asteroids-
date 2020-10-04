import pyglet, math, random
from pyglet.window import key

HEIGHT = 1280
WIDTH = 1280
ROTATION_SPEED = 300
ACCELERATION = 300
BEGINING = 0

spaceship = pyglet.resource.image("spaceship.png")
laser_beam = pyglet.resource.image("laser_beam.png")
background = pyglet.resource.image("background.png")

window = pyglet.window.Window(height=HEIGHT, width=WIDTH)
key_handler = key.KeyStateHandler()

batch = pyglet.graphics.Batch()

background = pyglet.graphics.OrderedGroup(1)
foreground = pyglet.graphics.OrderedGroup(0)


class Spaceship:

    def __init__(self):

        spaceship.anchor_y = spaceship.width // 2
        spaceship.anchor_x = spaceship.height // 2

        self.ship = pyglet.sprite.Sprite(spaceship, batch=batch, group=foreground)

        self.ship.x = 640
        self.ship.y = 640
        self.rotation = -90
        self.speed_y = 0
        self.speed_x = 0

    def move(self, dt):

        if key_handler[key.A]:
            self.rotation = self.rotation - ROTATION_SPEED * dt

        if key_handler[key.D]:
            self.rotation = self.rotation + ROTATION_SPEED * dt

        if key_handler[key.W]:
            angle_radians = -math.radians(self.rotation)

            force_x = math.cos(angle_radians) * ACCELERATION * dt
            force_y = math.sin(angle_radians) * ACCELERATION * dt
            self.speed_x = self.speed_x + force_x
            self.speed_y = self.speed_y + force_y

        self.ship.rotation = self.rotation + 90
        self.ship.x += self.speed_x * dt
        self.ship.y += self.speed_y * dt

        if self.ship.y > HEIGHT or self.ship.x > HEIGHT:
            self.ship.x = HEIGHT - self.ship.x
            self.ship.y = HEIGHT - self.ship.y
            self.ship.rotation = self.rotation

        elif self.ship.y < BEGINING or self.ship.x < BEGINING:
            self.ship.x = HEIGHT - self.ship.x
            self.ship.y = HEIGHT - self.ship.y
            self.ship.rotation = self.rotation


ship_object = Spaceship()


class Asteroids:
    pass


class Missile:

    def __init__(self):
        laser_beam.anchor_y = laser_beam.width // 2
        laser_beam.anchor_x = laser_beam.height // 2

        self.beam = pyglet.sprite.Sprite(laser_beam, batch=batch, group=background)

        self.rotation = 0

        self.beam.x = 640
        self.beam.y = 640

    def press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.move()

    def shoot(self, dt):
        pass

    def move(self, dt):
        self.beam.x = ship_object.ship.x
        self.beam.y = ship_object.ship.y

        self.rotation = ship_object.ship.rotation
        self.beam.rotation = self.rotation + 90


beam_object = Missile()


def drawing():
    window.clear()
    batch.draw()


window.push_handlers(on_draw=drawing,
                     on_key_press=beam_object.press)
window.push_handlers(key_handler)

pyglet.clock.schedule_interval(ship_object.move, 1 / 60)

pyglet.clock.schedule_interval(beam_object.move, 1 / 60)

pyglet.clock.schedule_interval(beam_object.shoot, 1 / 60)

pyglet.app.run()
