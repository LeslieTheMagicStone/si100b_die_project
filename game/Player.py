# -*- coding:utf-8 -*-

import pygame

import generator


from Settings import *
from Attributes import *
from Portal import *
from EventSystem import *
from Math import *
from NPCs import *
from globals import *
from Projectiles import *
from UI import *


class Player(
    pygame.sprite.Sprite,
    Collidable,
    Damageable,
    MonoBehavior,
    Renderable,
    Buffable,
    Levelable,
    reinforcable,
):
    def __init__(self, x, y):
        # Must initialize everything one by one here
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self, need_collision_list=True, is_rigid=True)
        Damageable.__init__(self)
        MonoBehavior.__init__(self)
        Renderable.__init__(self, render_index=RenderIndex.player)
        Buffable.__init__(self)
        Levelable.__init__(self)
        reinforcable.__init__(self)

        # Collision layer
        self.layer = "Player"
        # Animation related
        self.images = [
            pygame.transform.scale(
                pygame.image.load(path), (PlayerSettings.width, PlayerSettings.height)
            )
            for path in GamePath.player
        ]
        self.anim_interval_second = PlayerSettings.animIntervalSecond
        self.anim_frame = 0
        self.image = self.images[0]
        self.anim_timer = 0
        self.rendered_image = self.image.copy()
        self.image_pos_x = 0
        self.image_pos_y = 0
        self.rotation = 0

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Scale the rect by 0.5x to make collision trigger more realistic
        resize_amount = [-self.rect.width // 2, -self.rect.height // 2]
        self.rect.inflate_ip(resize_amount[0], resize_amount[1])
        # Attribute related
        self.speed = PlayerSettings.speed
        self.coins = 0
        self.attack = PlayerSettings.attack
        self.defence = PlayerSettings.defence
        # Combat related
        self.max_hp = PlayerSettings.hp
        self.cur_hp = self.max_hp
        # Fire related
        self.fire_cd = 0.5
        self.fire_timer = 0
        self.bullet_type = 0
        self.bullet_causality = Causality.NORMAL
        # Flipping related
        self.face_right = True
        # Reinforce related
        self.reinforcing = 0
        # Init sound player
        self.sound_player = SoundPlayer()
        # Init hurt player to play hurt sound
        self.hurt_player = SoundPlayer()
        # Rolling related
        self.roll_cd = 2
        self.roll_cd_timer = 0
        self.is_rolling = False
        self.rolling_time = 0.5
        self.rolling_timer = 0

    def reset_pos(self, x=WindowSettings.width // 2, y=WindowSettings.height // 2):
        self.rect.center = (x, y)

    def update(self):
        self.update_buffs()
        self.handle_bullet_change()
        self.handle_tools()
        self.handle_fire()
        self.handle_movement()
        self.handle_roll()
        self.handle_collisions()
        self.handle_reinforce()

    def update_buffs(self):
        to_be_deleted = []
        for buff, buff_time in self.buffs.items():
            if buff_time > 0:
                self.buffs[buff] -= Time.delta_time
            elif buff_time <= 0 and buff_time != -1:
                to_be_deleted.append(buff)

        for buff in to_be_deleted:
            self.delete_Buff(buff)

    def add_buff(self, buff_name: str, buff_time: float):
        super().add_buff(buff_name, buff_time)

        if buff_name == "exp":
            self.add_exp(buff_time)

        if buff_name == "rein":
            self.add_accumulative(buff_time)

        self.delete_Buff("exp")
        self.delete_Buff("rein")

    def handle_running_animation(self):
        # Only need to play run animation when running
        if self.velocity == (0, 0):
            self.image = self.images[2]
            return

        if self.anim_timer < 0:
            self.anim_timer = self.anim_interval_second
            self.anim_frame += 1
            self.anim_frame = min(self.anim_frame, self.anim_frame % len(self.images))
            self.image = self.images[self.anim_frame]

        self.anim_timer -= Time.delta_time

    def handle_movement(self):
        if CurrentState.state == GameState.DIALOG:
            self.velocity = (0, 0)
            return

        keys = pygame.key.get_pressed()

        dx = dy = 0

        if Input.get_key(pygame.K_w):
            dy -= 1
        if Input.get_key(pygame.K_s):
            dy += 1
        if Input.get_key(pygame.K_a):
            dx -= 1
        if Input.get_key(pygame.K_d):
            dx += 1

        velocity = Math.scale(Math.normalize((dx, dy)), self.speed)

        self.velocity = velocity

    def handle_bullet_change(self):
        if Input.get_key_down(pygame.K_q):
            self.bullet_type = (self.bullet_type + 1) % 2

    def handle_reinforce(self):
        if Input.get_key_down(pygame.K_SPACE) and self.ready == 1:
            self.finished()
            self.add_buff("Reinforce", 5)
            self.sound_player.play("ws")

    def handle_tools(self):
        if Input.get_key_down(pygame.K_e) and "Causality" in self.buffs.keys():
            self.bullet_causality = Causality((self.bullet_causality.value + 1) % 3)

    def handle_fire(self):
        if CurrentState.state == GameState.DIALOG:
            return

        increase = 0
        if "Reinforce" in self.buffs.keys():
            increase = 2

        if self.fire_timer > 0:
            self.fire_timer -= Time.delta_time
            return

        dx = dy = 0

        if Input.get_key(pygame.K_UP):
            dy -= 1
        if Input.get_key(pygame.K_DOWN):
            dy += 1
        if Input.get_key(pygame.K_LEFT):
            dx -= 1
        if Input.get_key(pygame.K_RIGHT):
            dx += 1

        if ((dx, dy) != (0, 0)) and self.bullet_type == 0:
            bullet_velocity = Math.scale(
                Math.normalize((dx, dy)), ProjectileSettings.bulletSpeed
            )
            bullet = generator.generate(
                Bullet(
                    self.rect.centerx,
                    self.rect.centery,
                    bullet_velocity,
                    self.attack + increase,
                    causality=self.bullet_causality,
                )
            )

        elif ((dx, dy) != (0, 0)) and self.bullet_type == 1:
            bullet_velocity = Math.scale(
                Math.normalize((dx, dy)), ProjectileSettings.bulletSpeed / 2
            )
            bullet = generator.generate(
                Big_bullet(
                    self.rect.centerx,
                    self.rect.centery,
                    bullet_velocity,
                    (self.attack + increase * 2) * 6,
                    causality=self.bullet_causality,
                )
            )

            self.fire_timer = self.fire_cd

    def handle_roll(self):
        self.roll_cd_timer -= Time.delta_time

        if Input.get_key_down(pygame.K_LSHIFT):
            if self.roll_cd_timer <= 0:
                self.roll_cd_timer = self.roll_cd

                self.is_rolling = True
                self.rolling_timer = self.rolling_time
                self.original_rotation = self.rotation
                self.add_buff("Invulnerable", self.rolling_time)

        if self.is_rolling:
            if self.rolling_timer > 0:
                self.rotation += 1440 * Time.delta_time
                self.rolling_timer -= Time.delta_time
                # Player gets a speed boost when rolling
                self.velocity = Math.scale(self.velocity, 3)
            else:
                self.rolling_timer = 0
                self.rotation = self.original_rotation
                self.is_rolling = False

    def handle_damage(self, damage):
        if "Invulnerable" in self.buffs:
            return 0

        decrease = 0
        if "Reinforce" in self.buffs:
            decrease = 2

        damage = max(0, 1 - decrease, damage - self.defence - decrease)
        self.cur_hp = max(0, self.cur_hp - damage)

        if self.cur_hp == 0:
            EventSystem.fire_game_over_event()

        EventSystem.fire_hurt_event(damage)

        self.hurt_player.set_volume(0.2)
        self.hurt_player.play("hurt")

        self.add_buff("Invulnerable", 0.5)

        return damage

    def handle_collisions(self):
        for enter in self.collisions_enter:
            if isinstance(enter, Portal):
                if (
                    enter.GOTO != SceneManager.current_scene
                    and CurrentState.state != GameState.FLUSHING
                ):
                    CurrentState.state = GameState.FLUSHING
                    EventSystem.fire_switch_event(enter.GOTO)

        for stay in self.collisions_stay:
            if isinstance(stay, Monster):
                damage = self.handle_damage(stay.attack)
                EventSystem.fire_hurt_event(damage)

            if isinstance(stay, EnemyBullet):
                damage = self.handle_damage(stay.damage)
                EventSystem.fire_hurt_event(damage)

    def level_up(self):
        super().level_up()

        self.max_hp += 10
        self.cur_hp = self.max_hp
        self.attack += self.level % 2

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        self.image = self.images[0]
        if CurrentState.state != GameState.GAME_OVER:
            # Handle running animation
            self.handle_running_animation()
        # Handle invulnerable animation
        if "Invulnerable" in self.buffs:
            time = self.buffs["Invulnerable"]
            alpha = (2 - int(time * 100) % 2) * 127
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        # Handle flipping
        if self.face_right and self.velocity[0] < 0:
            self.face_right = False
        elif not self.face_right and self.velocity[0] > 0:
            self.face_right = True

        if not self.face_right:
            final_image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
        else:
            final_image = self.image.copy()

        # Handle reinforce animation
        if "Reinforce" in self.buffs:
            mask = pygame.mask.from_surface(final_image)
            mask_surface = mask.to_surface(
                setcolor=(200, 124, 124, 255), unsetcolor=(0, 0, 0, 0)
            )
            final_image.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            final_image = pygame.transform.scale_by(final_image, 1.2)

        # Handle rotation
        final_image = pygame.transform.rotate(final_image, self.rotation)

        # Calculate top-left corner of the picture separately
        # because that of the rect has been changed when scaling
        offset = -8 if self.face_right else 8
        self.image_pos_x = (
            self.rect.centerx - final_image.get_width() // 2 + offset
        )  # tiny offset to look more realistic
        self.image_pos_y = self.rect.centery - final_image.get_height() // 2
        window.blit(final_image, (self.image_pos_x + dx, self.image_pos_y + dy))
        self.rendered_image = final_image.copy()
