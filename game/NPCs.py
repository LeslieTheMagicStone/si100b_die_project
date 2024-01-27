# -*- coding:utf-8 -*-

import pygame
from Effects import RenderIndex
from Projectiles import Causality, NPCSettings, NPCSettings, RenderIndex
from Settings import Causality, RenderIndex
from UI import Causality, NPCSettings, RenderIndex
import generator

from Settings import *
from Attributes import *
from Math import *
from EventSystem import *
from Projectiles import *
from UI import *
from globals import *
from Effects import *
from random import randint
from enum import Enum


class NPC(pygame.sprite.Sprite, Collidable, Renderable, MonoBehavior):
    def __init__(
        self, x, y, name, render_index=RenderIndex.npc, speed=NPCSettings.npcSpeed
    ):
        # Initialize father classes
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self, is_rigid=True)
        Renderable.__init__(self, render_index)
        MonoBehavior.__init__(self)

        # Image and rect related
        self.image = pygame.image.load(GamePath.npc)
        self.image = pygame.transform.scale(
            self.image, (NPCSettings.npcWidth, NPCSettings.npcHeight)
        )
        # NPCs are initialized with a random scale
        self.image = pygame.transform.scale_by(self.image, 0.8 + random() * 0.4)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = speed
        self.name = name

        # Used for flipping
        # given a random initial state
        self.face_right = randint(0, 1) == 0

    def update(self):
        raise NotImplementedError

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        # Handle flipping
        if self.velocity[0] > 0 and not self.face_right:
            self.face_right = True
        elif self.velocity[0] < 0 and self.face_right:
            self.face_right = False

        if not self.face_right:
            final_image = pygame.transform.flip(self.image, True, False)
        else:
            final_image = self.image.copy()

        if self.is_active:
            window.blit(final_image, self.rect.move(dx, dy))


class DialogNPC(NPC):
    def __init__(
        self,
        x,
        y,
        name,
        text,
        player_rect: pygame.Rect,
        render_index=RenderIndex.npc,
        speed=NPCSettings.npcSpeed,
    ):
        super().__init__(x, y, name, render_index, speed)

        # The npc's dialog
        self.text = text
        # Save player rect to detect distance
        self.player_rect = player_rect

        # Moving behavior
        self.is_walking = True
        self.behavior_timer = 1
        self.children = []

    def start(self):
        super().start()

        # Init trigger text
        self.trigger_text = generator.generate(DialogIcon(self.rect, "按Enter对话", dy=20))
        self.trigger_text.set_active(False)
        self.children.append(self.trigger_text)
        self.name_text = generator.generate(DialogIcon(self.rect, self.name, dy=0))
        self.name_text.set_active(False)
        self.children.append(self.name_text)

    def update(self):
        self.handle_dialog()
        self.handle_movement()

    def handle_movement(self):
        if CurrentState.state == GameState.DIALOG:
            return

        if self.behavior_timer < 0:
            # If is walking, then stop
            if self.is_walking:
                self.behavior_timer = random() * 1.5
                self.is_walking = False
                self.velocity = (0, 0)
            # If is stopping, then walk
            else:
                self.behavior_timer = randint(2, 3)
                self.is_walking = True
                self.velocity = Math.scale((randint(-1, 1), randint(-1, 1)), self.speed)
        self.behavior_timer -= Time.delta_time

    def handle_dialog(self):
        distance = Math.distance(self.rect.center, self.player_rect.center)
        if (
            distance < NPCSettings.npcTriggerRadius
            and CurrentState.state != GameState.DIALOG
        ):
            self.trigger_text.set_active(True)
            self.name_text.set_active(True)
            if Input.get_key_down(pygame.K_RETURN):
                self.trigger_text.set_active(False)
                self.name_text.set_active(False)
                EventSystem.fire_dialog_event(self.image, self.text)
        else:
            self.trigger_text.set_active(False)
            self.name_text.set_active(False)


class ShopNPC(DialogNPC):
    def __init__(
        self,
        x,
        y,
        name,
        items,
        player_rect: pygame.Rect,
        render_index=RenderIndex.npc,
        speed=NPCSettings.npcSpeed,
    ):
        super().__init__(x, y, name, items, player_rect, render_index, speed)
        self.items = items

    def handle_dialog(self):
        distance = Math.distance(self.rect.center, self.player_rect.center)
        if (
            distance < NPCSettings.npcTriggerRadius
            and CurrentState.state != GameState.DIALOG
        ):
            self.trigger_text.set_active(True)
            self.name_text.set_active(True)
            if Input.get_key_down(pygame.K_RETURN):
                self.trigger_text.set_active(False)
                self.name_text.set_active(False)
                EventSystem.fire_shop_event(self.image, self.text)
        else:
            self.trigger_text.set_active(False)
            self.name_text.set_active(False)


class Monster(NPC, Damageable, Levelable):  #
    def __init__(
        self,
        player_rect: pygame.Rect,
        x,
        y,
        speed=4,
        hp=10,
        attack=3,
        defence=1,
        money=15,
        causality=Causality.ICE,
        level=1,
    ):
        NPC.__init__(self, x, y, name="Monster", render_index=RenderIndex.monster)
        Damageable.__init__(self)
        Levelable.__init__(self)

        # Collision Layer is enemy
        self.layer = "Enemy"
        # Need collision list to detect hurt
        self.need_collision_list = True
        # Image and rect related
        if causality == Causality.ICE:
            self.image = pygame.image.load(GamePath.iceMonster)
        elif causality == Causality.FIRE:
            self.image = pygame.image.load(GamePath.fireMonster)
        self.image = pygame.transform.scale(
            self.image, (NPCSettings.npcWidth, NPCSettings.npcHeight)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Save player position
        self.player_rect = player_rect
        # Attribute related
        level = max(level, 1)
        self.level = level
        self.exp = self.level
        self.speed = speed
        self.max_hp = hp * level
        self.attack = int(attack * (1 + level / 10))
        self.defence = int(defence * (1 + level / 3))
        self.money = money
        self.causality = causality
        # Combat related
        self.is_dead = False
        self.cur_hp = self.max_hp

        self.children = []

    def start(self):
        # Init health bar
        self.health_bar = HealthBar(self, self.rect)
        generator.generate(self.health_bar)
        self.children.append(self.health_bar)
        # Init exp bar
        self.exp_bar = ExpBar(self, self.rect)
        generator.generate(self.exp_bar)
        self.children.append(self.exp_bar)
        # Play generate anim
        EffectManager.generate("teleport", self.rect.centerx, self.rect.centery)

    def update(self):
        if self.is_dead:
            return

        self.handle_movement()
        self.handle_collisions()

    def handle_movement(self):
        # Straightly moves towards the player
        dir = (self.player_rect.x - self.rect.x, self.player_rect.y - self.rect.y)
        movement = Math.round(Math.scale(Math.normalize(dir), self.speed))
        self.velocity = (movement[0], movement[1])

    def handle_damage(self, damage):
        damage = max(1, damage - self.defence)
        self.cur_hp = max(0, self.cur_hp - damage)

        if self.cur_hp == 0:
            self.handle_death()

        return damage

    def handle_death(self):
        EventSystem.fire_destroy_event(self)
        EventSystem.fire_buff_event("exp", self.exp)
        EventSystem.fire_buff_event("rein", 1)

    def handle_collisions(self):
        # if len(self.collisions_enter) != 0:
        #     print("enter", self.collisions_enter, self.velocity)
        # if len(self.collisions_stay) != 0:
        #     print("stay", self.collisions_stay, self.velocity)
        # if len(self.collisions_exit) != 0:
        #     print("exit", self.collisions_exit, self.velocity)
        for other in self.collisions_enter:
            if isinstance(other, Projectile):
                if isinstance(other, Bullet):
                    damage = other.damage
                    if self.causality == Causality.FIRE:
                        if other.causality == Causality.FIRE:
                            damage //= 2
                        elif other.causality == Causality.ICE:
                            damage *= 2
                    elif self.causality == Causality.ICE:
                        if other.causality == Causality.ICE:
                            damage //= 2
                        elif other.causality == Causality.FIRE:
                            damage *= 2
                    damage = self.handle_damage(damage)
                    # Generate random offset of the hit point to make the game juicier
                    ortho_normal = Math.ortho_normal(other.velocity)
                    random_offset = Math.scale(ortho_normal, randint(-20, 20))
                    EventSystem.fire_hit_event(
                        damage, Math.add(random_offset, other.rect.center)
                    )
                    EventSystem.fire_destroy_event(other)

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect.move(dx, dy))


class Boss(Monster):
    def __init__(
        self,
        player_rect: pygame.Rect,
        x,
        y,
        speed=4,
        hp=1000,
        attack=30,
        defence=10,
        money=15,
        causality=Causality.NORMAL,
        level=1,
    ):
        super().__init__(
            player_rect, x, y, speed, hp, attack, defence, money, causality, level
        )
        self.image = pygame.image.load(GamePath.boss)
        self.image = pygame.transform.scale(
            self.image, (BossSettings.width, BossSettings.height)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Scale the rect to make collision trigger more realistic
        resize_amount = [-self.rect.width // 4, -self.rect.height // 4]
        self.rect.inflate_ip(resize_amount[0], resize_amount[1])

        # It has three phases
        self.remaining_lives = 2

        # Combat related
        self.behavior_timer = 0
        self.states = {"ATTACK": 2, "STOP": 1, "SUMMON": 3}
        self.cur_state = "STOP"

        # This gives player rein during combat when boss gets enough damage
        self.rein_progress = 0
        self.rein_damage = 50

    def start(self):
        EffectManager.generate("boss", self.rect.centerx, self.rect.centery)

        # Init boss health bar
        self.health_bar = generator.generate(BossHealthBar(self))
        self.children.append(self.health_bar)

    def update(self):
        super().update()

        self.behavior_timer -= Time.delta_time

        # If behavior timer to time, change state randomly
        if self.behavior_timer <= 0:
            index = randint(0, len(self.states.keys()) - 1)
            self.cur_state = list(self.states.keys())[index]
            self.behavior_timer = self.states[self.cur_state]

        if self.cur_state == "STOP":
            pass
        elif self.cur_state == "ATTACK":
            # Calculate basic data

            x = self.rect.centerx
            y = self.rect.centery
            direction = Math.normalize(
                Math.minus(self.player_rect.center, self.rect.center)
            )
            velocity = Math.scale(direction, ProjectileSettings.bulletSpeed)

            generator.generate(EnemyBullet(x, y, velocity, 5, Causality.ICE))

            if randint(0, 5) == 0:
                generator.generate(
                    EnemyBigBullet(x, y, Math.scale(velocity, 0.5), 5, Causality.ICE)
                )

            if self.remaining_lives == 2:
                return

            # Phase 2 gets upgrades
            noise = (randint(-2, 2), randint(-2, 2))
            if randint(0, 4) == 0:
                generator.generate(
                    EnemyBigBullet(
                        x,
                        y,
                        Math.add(Math.scale(velocity, 0.5), noise),
                        5,
                        Causality.FIRE,
                    )
                )

            if self.remaining_lives == 1:
                return

            # Phase 1 gets more upgrades
            self.states["ATTACK"] = 3
            self.states["STOP"] = 0.5
            if randint(0, 10) == 0:
                generator.generate(
                    EnemyLaserGenerator(x, y, 10, 5, Causality(randint(0, 2)))
                )
        elif self.cur_state == "SUMMON":
            self.velocity = (random() * randint(-5, 5), random() * randint(-5, 5))
            distance_coords = Math.minus(self.player_rect.center, self.rect.center)
            distance = Math.norm(distance_coords)

            if randint(0, 20) == 0 and distance >= 200:
                x = random() * distance_coords[0] + self.rect.centerx
                y = random() * distance_coords[1] + self.rect.centery
                # Avoid spawning monster inside rigid collidables
                for i in range(5):
                    rand_level = randint(5, 10) + (2 - self.remaining_lives) * 5
                    monster = Monster(
                        self.player_rect,
                        x,
                        y,
                        causality=Causality(randint(1, 2)),
                        level=rand_level,
                    )
                    if not CollisionChecker.check_rigids(monster.rect):
                        generator.generate(monster)
                        break

    def handle_damage(self, damage):
        damage = max(1, damage - self.defence)
        self.cur_hp = max(0, self.cur_hp - damage)

        self.rein_progress += damage
        if self.rein_progress >= self.rein_damage:
            self.rein_progress = 0
            EventSystem.fire_buff_event("rein", 1)

        if self.cur_hp == 0:
            self.handle_death()

        return damage

    def handle_death(self):
        # If it has remaining life, just revive
        if self.remaining_lives > 0:
            self.remaining_lives -= 1
            self.cur_hp = self.max_hp

            # Last life play transition anim
            if self.remaining_lives == 0:
                CurrentState.in_transition_animation = True

            return

        super().handle_death()

        EventSystem.fire_buff_event("BossSlayer", -1)

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        # Calculate top-left corner of the picture separately
        # because that of the rect has been changed when scaling
        image_pos_x = self.rect.centerx - self.image.get_width() // 2
        image_pos_y = self.rect.centery - self.image.get_height() // 2
        window.blit(self.image, (image_pos_x + dx, image_pos_y + dy))
