import pyxel
import time
from enum import Enum
import random

presents = []
enemys = []
hearts = []

class Direction(Enum):
    NORTH = 1
    NORTH_EAST = 2
    EAST = 3
    SOUTH_EAST = 4
    SOUTH = 5
    SOUTH_WEST = 6
    WEST = 7
    NORTH_WEST = 8


class PhysicsObject:
    def __init__(self, x, y, width=8, height=8) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.move_speed_x = 1
        self.move_speed_y = 1
        self.velocity_x = 0
        self.velocity_y = 0

    def draw(self) -> None:
        pass

    def update(self) -> None:
        pass

    def collides_with_walls(self):
        if self.x >= pyxel.width - self.width:
            self.x -= 1
        elif self.x <= 0:
            self.x += 1
        elif self.y >= pyxel.height - self.height:
            self.y -= 1
        elif self.y <= 0:
            self.y += 1
        else:
            return False
        return True

class Arrow(PhysicsObject):
    def __init__(self, x, y, direction, width=8, height=8) -> None:
        super().__init__(x, y, width, height)
        self.direction = direction
        if direction == Direction.NORTH:
            self.image_x = 0
            self.image_y = 16
            self.y -= self.height
        elif direction == Direction.NORTH_EAST:
            self.image_x = 16
            self.image_y = 16
            self.x += self.width
            self.y -= self.height
        elif direction == Direction.EAST:
            self.image_x = 8
            self.image_y = 16
            self.x += self.width
        elif direction == Direction.SOUTH_EAST:
            self.image_x = 24
            self.image_y = 16
            self.x += self.width
            self.y += self.height
        elif direction == Direction.SOUTH:
            self.image_x = 0
            self.image_y = 24
            self.y += self.height
        elif direction == Direction.SOUTH_WEST:
            self.image_x = 16
            self.image_y = 24
            self.x -= self.width
            self.y += self.height
        elif direction == Direction.WEST:
            self.image_x = 8
            self.image_y = 24
            self.x -= self.width
        elif direction == Direction.NORTH_WEST:
            self.image_x = 24
            self.image_y = 24
            self.x -= self.width
            self.y -= self.height

    def draw(self) -> None:
        pyxel.blt(self.x, self.y, 0, self.image_x,
                  self.image_y, self.width, self.height)

class Heart(PhysicsObject):
    def __init__(self, x, y, width=8, height=8) -> None:
        super().__init__(x, y, width, height)
        self.image_x = 32
        self.image_y = 16

    def draw(self) -> None:
        pyxel.blt(self.x, self.y, 0, self.image_x,
                  self.image_y, self.width, self.height)

class Santa(PhysicsObject):
    def __init__(self, x, y, width=6, height=8) -> None:
        global presents
        super().__init__(x, y, width, height)
        self.image_x = 8
        self.image_y = 8
        self.direction = Direction.EAST
        # presents setup
        self.presents = presents
        self.cooldown = 1
        self.present_speed = 2
        self.time = time.time()
        self.time_delta = 0
    
    def draw(self) -> None:
        Arrow(self.x, self.y, self.direction).draw()
        pyxel.blt(self.x, self.y, 0, self.image_x,
                  self.image_y, self.width, self.height)

    def move(self):
        if (
            (pyxel.btn(pyxel.KEY_UP) and pyxel.btn(pyxel.KEY_RIGHT))
            or (pyxel.btn(pyxel.GAMEPAD2_BUTTON_DPAD_UP) and pyxel.btn(pyxel.GAMEPAD2_BUTTON_DPAD_RIGHT))):
            self.y -= self.move_speed_y
            self.x += self.move_speed_x
            self.direction = Direction.NORTH_EAST
        elif (
            (pyxel.btn(pyxel.KEY_DOWN) and pyxel.btn(pyxel.KEY_RIGHT)
            or (pyxel.btn(pyxel.GAMEPAD2_BUTTON_DPAD_DOWN) and pyxel.btn(pyxel.GAMEPAD2_BUTTON_DPAD_RIGHT)))):
            self.y += self.move_speed_y
            self.x += self.move_speed_x
            self.direction = Direction.SOUTH_EAST
        elif (
            (pyxel.btn(pyxel.KEY_UP) and pyxel.btn(pyxel.KEY_LEFT))
            or (pyxel.btn(pyxel.GAMEPAD2_BUTTON_DPAD_UP) and pyxel.btn(pyxel.GAMEPAD2_BUTTON_DPAD_LEFT))):
            self.y -= self.move_speed_y
            self.x -= self.move_speed_x
            self.direction = Direction.NORTH_WEST
        elif (
            (pyxel.btn(pyxel.KEY_DOWN) and pyxel.btn(pyxel.KEY_LEFT))
            or (pyxel.btn(pyxel.GAMEPAD2_BUTTON_DPAD_DOWN) and pyxel.btn(pyxel.GAMEPAD2_BUTTON_DPAD_LEFT))):
            self.y += self.move_speed_y
            self.x -= self.move_speed_x
            self.direction = Direction.SOUTH_WEST
        elif pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD2_BUTTON_DPAD_UP):
            self.y -= self.move_speed_y
            self.direction = Direction.NORTH
        elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD2_BUTTON_DPAD_DOWN):
            self.y += self.move_speed_y
            self.direction = Direction.SOUTH
        elif pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD2_BUTTON_DPAD_LEFT):
            self.x -= self.move_speed_x
            self.width = -abs(self.width)
            self.direction = Direction.WEST
        elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD2_BUTTON_DPAD_RIGHT):
            self.x += self.move_speed_x
            self.width = abs(self.width)
            self.direction = Direction.EAST
        if self.direction == Direction.NORTH_EAST or self.direction == Direction.SOUTH_EAST:
            self.width = abs(self.width)
        elif self.direction == Direction.NORTH_WEST or self.direction == Direction.SOUTH_WEST:
            self.width = -abs(self.width)

    def spawn_present(self):
        present = Present(self.x, self.y)
        if self.direction == Direction.NORTH:
            present.velocity_y = -self.present_speed
        elif self.direction == Direction.NORTH_EAST:
            present.velocity_y = -self.present_speed
            present.velocity_x = self.present_speed
        elif self.direction == Direction.EAST:
            present.velocity_x = self.present_speed
        elif self.direction == Direction.SOUTH_EAST:
            present.velocity_y = self.present_speed
            present.velocity_x = self.present_speed
        elif self.direction == Direction.SOUTH:
            present.velocity_y = self.present_speed
        elif self.direction == Direction.SOUTH_WEST:
            present.velocity_y = self.present_speed
            present.velocity_x = -self.present_speed
        elif self.direction == Direction.WEST:
            present.velocity_x = -self.present_speed
        elif self.direction == Direction.NORTH_WEST:
            present.velocity_y = -self.present_speed
            present.velocity_x = -self.present_speed
        self.presents.append(present)

    def update(self) -> None:
        # update time
        old_time = self.time
        self.time = time.time()
        self.time_delta += self.time - old_time
        # check collisions
        if self.collides_with_walls():
            return
        self.move()
        if self.time_delta > self.cooldown-0.8:
            self.image_x = 8
            self.image_y = 8
        if pyxel.btn(pyxel.KEY_SPACE):
            if self.time_delta > self.cooldown:
                self.image_x = 0
                self.image_y = 8
                self.spawn_present()
                self.time_delta = 0


class Present(PhysicsObject):
    def __init__(self, x, y, width=8, height=8) -> None:
        global presents
        self.presents = presents
        self.image_x = 24
        self.image_y = 8
        super().__init__(x, y, width, height)

    def draw(self) -> None:
        # (x, y, image, x in image, y in image, height, width)
        pyxel.blt(self.x, self.y, 0, self.image_x,
                  self.image_y, self.width, self.height)

    def update(self) -> None:
        if self.collides_with_walls():
            self.presents.remove(self)
            return
        self.x += self.velocity_x
        self.y += self.velocity_y


class Enemy(PhysicsObject):
    def __init__(self, x, y, velocity_x, width=8, height=8) -> None:
        global presents, enemys, hearts
        self.presents = presents
        self.enemys = enemys
        self.hearts = hearts
        self.image_x = 32
        self.image_y = 8
        self.dying = False
        super().__init__(x, y, width, height)
        self.velocity_x = velocity_x
        self.time = None
        self.time_delta = 0

    def draw(self) -> None:
        if self.dying:
            if self.time is None:
                self.velocity_x = 0
                self.time = time.time()
                self.image_x += 8
            old_time = self.time
            self.time = time.time()
            self.time_delta += self.time - old_time
            if self.time_delta > 0.2:
                self.image_x -= 8
                self.image_y -= 8
            if self.time_delta > 0.5:
                self.image_x += 8
            if self.time_delta > 0.8:
                print("remove")
                self.enemys.remove(self)
                return

        pyxel.blt(self.x, self.y, 0, self.image_x,
                  self.image_y, self.width, self.height)

    def collides_with_present(self):
        for present in self.presents:
            if (self.x < present.x + present.width 
            and self.x + self.width > present.x 
            and self.y < present.y + present.height 
            and self.y + self.height > present.y):
                return True
        return False
    
    def reached_end(self):
        if self.x <= 0:
            return True
        return False

    def update(self) -> None:
        if self.reached_end():
            del self.hearts[-1]
            self.enemys.remove(self)
        if self.collides_with_present():
            self.dying = True
            pyxel.play(0, 1)
            return
        self.x += self.velocity_x
        self.y += self.velocity_y


class App:
    def __init__(self) -> None:
        global presents, enemys, hearts
        pyxel.init(128, 128, fps=60)  # , display_scale=8)
        pyxel.load("assets/my_resource.pyxres")
        pyxel.pal(0, 9)
        self.santa = Santa(32, 32)
        self.presents = presents
        self.enemys = enemys
        self.hearts = hearts
        # game speed
        self.game_speed = 1 / 1000
        self.time = time.time()
        self.time_delta = 0
        
        self.level = 0
        self.create_hearts()
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        old_time = self.time
        self.time = time.time()
        self.time_delta += self.time - old_time
        if len(self.enemys) == 0:
            self.level += 1
            self.presents.clear()
            self.create_enemys()
        if len(self.hearts) == 0:
            pyxel.play(0, 0)
            pyxel.cls(0)
            pyxel.text(pyxel.width//2.75, pyxel.height//2.5, "GAME OVER", 7)
            pyxel.text(pyxel.width//2.5, pyxel.height//2, f"LEVEL {self.level}", 7)
            pyxel.show()
        if self.time_delta > self.game_speed:
            self.santa.update()
            present: Present
            for present in self.presents:
                present.update()
            enemy: Enemy
            for enemy in self.enemys:
                enemy.update()
            self.time_delta = 0
    
    def create_enemys(self):
        for _ in range(0, self.level):
            random_x = random.randrange(int(pyxel.width*0.6), pyxel.width, 8)
            random_y = random.randrange(0, pyxel.height, 8)
            self.enemys.append(Enemy(random_x, random_y, -0.3))
    
    def create_hearts(self):
        position_y = pyxel.height - 9
        position_x = 1
        for _ in range(0, 3):
            self.hearts.append(Heart(position_x, position_y))
            position_x += 9
            
    def draw(self) -> None:
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, pyxel.height)
        self.santa.draw()
        pyxel.text(1, 1, f"Level {self.level}", 7)

        present: Present
        for present in self.presents:
            present.draw()
        enemy: Enemy
        for enemy in self.enemys:
            enemy.draw()
        heart: Heart
        for heart in self.hearts:
            heart.draw()


app = App()
