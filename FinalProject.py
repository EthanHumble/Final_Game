import arcade

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Move with Walls Example"
GAME_INTRO = 1
GAME_RUNNING = 2
GAME_OVER = 3
MOVEMENT_SPEED = 5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        # Sprite lists
        self.coin_list = None
        self.wall_list = None
        self.player_list = None

        # Set up the player
        self.player_sprite = None
        self.physics_engine = None

        #Sound
        self.standard = arcade.load_sound("arcade_resources_sounds_hit2.wav")

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                           SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 64
        self.player_sprite.angle = 0
        self.player_sprite.change_x = 1
        self.player_list.append(self.player_sprite)
        self.current_state = GAME_INTRO

        # -- Set up the walls
        # Create a row of boxes
        for x in range(0, 15000, 64):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 0
            self.wall_list.append(wall)

        # # Create a column of boxes
        # for y in range(273, 500, 64):
        #     wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
        #                          SPRITE_SCALING)
        #     wall.center_x = 465
        #     wall.center_y = y
        #     self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.wall_list)

        # Set the background color
        arcade.set_background_color(arcade.color.SKY_BLUE)


        if self.current_state == GAME_INTRO:
            arcade.draw_text("Welcome to Running Man", SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 30, arcade.color.BLACK,
                             25)
            arcade.draw_text("Use the Up Key and Down Key to jump and squat to avoid the obstacles", SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, arcade.color.BLACK,
                             25)
            arcade.draw_text("Press the space bar to continue.", SCREEN_WIDTH // 3, (SCREEN_HEIGHT // 2 - 30),
                             arcade.color.BLACK, 25)

        elif self.current_state == GAME_RUNNING:
             self.draw_game()

        else:
            ##End game
            self.draw_game_over()

    # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
        self.player_sprite, gravity_constant = GRAVITY)

    def draw_game(self):
        self.on_draw()

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.wall_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.angle = 270
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.angle = 0
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()


def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()