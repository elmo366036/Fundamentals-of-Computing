# program template for Spaceship
# http://www.codeskulptor.org/#user45_Xlvigkso6N_1.py

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

SHIP_TILE_CENTER_OFFSET = 90 	#from ship image
SHIP_SIZE = [45, 45] 			#from ship image
ANGLE_VEL_CHANGE = .05
FRICTION_CONSTANT = .1
MISSILE_SPEED_MULTIPLIER = 3.5
MAX_ROCK_VEL = 2
FRAME_BORDER = 50 				#this keeps the asteroid from spawning
                                #too close to the edge. Also used for
                                #lives and score
MAX_ROCKS = 6
MIN_ASTEROID_SHIP_SPAWN_DISTANCE = 50	#this keeps the asteriods from spawining
                                        #to close to the ship

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated asteroid
animated_asteroid_info = ImageInfo([64, 64], [128, 128], 55, None, True)
animated_asteroid_dim = 64
animated_asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/asteroid1.opengameart.warspawn.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_dim = 24
explosion_framerate_factor = 1.0
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
#soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(canvas, group):
    for sprite in group:
        sprite.draw(canvas)
        if sprite.update():
            group.remove(sprite)

def group_collide(group, other_object):
    global explosion_group
    collision = False
    for sprite in set(group):
        if sprite.collide(other_object):
            group.discard(sprite)
            an_explosion = Sprite([sprite.get_position()[0],
                                   sprite.get_position()[1]],
                                  [0, 0], 0, 0, explosion_image,
                                  explosion_info, explosion_dim,
                                  explosion_framerate_factor, explosion_sound)
            #print an_explosion
            explosion_group.add(an_explosion)
            #print explosion_group
            collision = True
            explosion_sound.rewind()
            explosion_sound.play()
    return collision

def group_group_collide(group_a, group_b):
    group_a_remove = set([])
    for sprite_a in set(group_a):
        if group_collide(group_b, sprite_a):
            group_a_remove.add(sprite_a)
            group_a.discard(sprite_a)
    return len(group_a_remove)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.forward = [0,0]

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def thrust_on(self):
        self.thrust == True

    def thrust_off(self):
        self.thrust == False

    def shoot(self):
        global missile_group
        missile_velocity = [self.vel[0] + MISSILE_SPEED_MULTIPLIER * self.forward[0],
                            self.vel[1] + MISSILE_SPEED_MULTIPLIER * self.forward[1]]
        a_missile = Sprite([self.pos[0] + self.forward[0] * SHIP_SIZE[0],
                            self.pos[1] + self.forward[1] * SHIP_SIZE[1]],
                           missile_velocity, 0, 0,
                           missile_image, missile_info, 0,0, missile_sound)
        missile_group.add(a_missile)

    def draw(self,canvas):
        if not self.thrust:
            canvas.draw_image(self.image,
                              self.image_center,
                              self.image_size, self.pos,
                              self.image_size, self.angle)
            ship_thrust_sound.rewind()

        if self.thrust:
            canvas.draw_image(self.image,
                              (self.image_center[0] + SHIP_TILE_CENTER_OFFSET,
                              self.image_center[1]),
                              self.image_size, self.pos,
                              self.image_size, self.angle)
            ship_thrust_sound.play()

    def update(self):
        #Position & Orientation Update
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        #Friction Update
        self.vel[0] *= 1 - FRICTION_CONSTANT
        self.vel[1] *= 1 - FRICTION_CONSTANT

        #Determine Forward Vector
        self.forward = angle_to_vector(my_ship.angle)

        if self.thrust:
            self.vel[0] += self.forward[0]
            self.vel[1] += self.forward[1]

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, dim, framerate_factor, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated() #if false
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
        self.dim = dim
        self.framerate_factor = framerate_factor

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def collide(self, other_object):
        distance = dist(self.get_position(), other_object.get_position())
        if distance <= self.get_radius() + other_object.get_radius():
            return True
        return False

    def draw(self, canvas):
        if self.animated == False:
            canvas.draw_image(self.image,
                              self.image_center,
                              self.image_size, self.pos,
                              self.image_size, self.angle)
        else:
            current_image_index = (((time * self.framerate_factor) % self.dim) // 1)
            print current_image_index
            current_image_center = [self.image_center[0] +  current_image_index * self.image_size[0],
                                   self.image_center[1]]
            canvas.draw_image(self.image,
                          current_image_center,
                          self.image_size, self.pos,
                          self.image_size, self.angle)

    def update(self):
        #Position & Orientation Update
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1
        if self.age >= self.lifespan:
            return True
        return False

# event handlers
def draw(canvas):
    global time, started, lives, score, rock_group, missile_group, explosion_group, my_ship

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw score and lives
    canvas.draw_text("Lives "+str(lives), (FRAME_BORDER,
                                FRAME_BORDER), 20, "White")
    canvas.draw_text("Score "+str(score), (WIDTH - 4 * FRAME_BORDER,
                                FRAME_BORDER), 20, "White")

    if started:
        soundtrack.play()

        # draw and update ship
        my_ship.draw(canvas)
        my_ship.update()

        # draw and update sprite groups
        process_sprite_group(canvas, rock_group)
        process_sprite_group(canvas, missile_group)
        process_sprite_group(canvas, explosion_group)

        # check for collisions with ship
        if group_collide(rock_group, my_ship):
            lives -= 1

        # check for collisions with missiles
        score += group_group_collide(rock_group, missile_group)

            # check for lives = 0
        if lives <= 0:
            started = False
            rock_group = set([])
            missile_group = set([])
            ship_thrust_sound.rewind()
            soundtrack.rewind()

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())

#keydown handler
def keydown(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = -ANGLE_VEL_CHANGE
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = ANGLE_VEL_CHANGE
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = True
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()

#keyup handler
def keyup(key):
    #print "Key up "+str(key)
    if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = False

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, score, lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        score = 0
        lives = 3
        time = 0

# timer handler that spawns a rock
def rock_spawner():
    global rock_group
    if len(rock_group) >= MAX_ROCKS:
        return

    pos = [random.randrange(FRAME_BORDER, WIDTH - FRAME_BORDER),
           random.randrange(FRAME_BORDER, HEIGHT - FRAME_BORDER)]
    vel = [random.randrange(-MAX_ROCK_VEL, MAX_ROCK_VEL),
           random.randrange(-MAX_ROCK_VEL, MAX_ROCK_VEL)]
    #ang_vel = float(random.randrange(-10, 10) * .01)
        # this produces a range of -.1 to .1 for the angular velocity
    ang_vel = 0
    framerate_factor = random.randrange(250.0, 450.0) / 1000.0
    #print framerate_factor

    a_rock = Sprite([pos[0], pos[1]], vel, 0, ang_vel,
                    animated_asteroid_image,
                    animated_asteroid_info,
                    animated_asteroid_dim,
                    framerate_factor)

    distance = dist(my_ship.get_position(), a_rock.get_position())
    if distance > my_ship.get_radius() + a_rock.get_radius() + MIN_ASTEROID_SHIP_SPAWN_DISTANCE:
        rock_group.add(a_rock)


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
