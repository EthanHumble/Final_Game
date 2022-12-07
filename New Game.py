"""
Platformer Game
"""
import random

import arcade

# Constants
WIDTH = 1000
HEIGHT = 650
SCREEN_TITLE = "Platformer"
SCREEN_TITLE2 = "Sprite Move with Walls Example"
MOVEMENT_SPEED = 5

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Welcome to Running Man!", WIDTH / 2, HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", WIDTH / 2, HEIGHT / 2 - 75,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.LIGHT_YELLOW)

    def on_draw(self):
        self.clear()
        arcade.draw_text("The controls are simple", WIDTH / 2, HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Use the Up Key to jump and Down Key to squat to avoid the obstacles", WIDTH / 2, HEIGHT / 2 - 75,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        # Keep track of the score
        self.score = 0

    def on_show_view(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Instructions Screen", WIDTH / 2, HEIGHT / 2,
                        arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", WIDTH / 2, HEIGHT / 2 - 75,
                        arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Set up the Camera
        self.camera = arcade.Camera(WIDTH, HEIGHT)

        # Set up the GUI Camera
        self.gui_camera = arcade.Camera(WIDTH, HEIGHT)

        # Keep track of the score
        self.score = 0

        self.crate_list = arcade.SpriteList()

        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 96
        self.player_sprite.change_x = 5
        self.scene.add_sprite("Player", self.player_sprite)

        #Sprite list
        self.brick_spritelist = arcade.SpriteList()

        #Timer variable
        self.timer = 100

        #Score timer
        self.score_timer = 0

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1000000, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        import random

        x_coord = random.randrange(0, WIDTH)
        coordinate_list = [[x_coord, 96]]
        coordinate_list_2 = [[x_coord, 192]]

        for coordinate in coordinate_list:
            # Add a cactus on the ground
            wall = arcade.Sprite(":resources:images/tiles/cactus.png", TILE_SCALING)
            wall.position = coordinate
            self.crate_list.append(wall)

        for coordinate in coordinate_list_2:
            # Add a crate to the air
            crate = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            crate.position = coordinate
            self.crate_list.append(crate)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
        )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate our Camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 18,)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        if key == arcade.key.DOWN:
            self.player_sprite.angle = 90

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.angle = 0
            self.player_sprite.change_y = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Position the camera
        self.center_camera_to_player()

        #Timer update
        if self.timer <= 0:
            wall = arcade.Sprite(":resources:images/tiles/cactus.png", TILE_SCALING)
            x_coord = random.randrange(self.player_sprite.center_x + 400, self.player_sprite.center_x + 900)
            coordinate = [x_coord, 96]
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)
            self.brick_spritelist.append(wall)
            self.timer = 100
        else:
            self.timer -= 1

        if self.timer <= 0:
            crate = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            x_coord = random.randrange(self.player_sprite.center_x + 400, self.player_sprite.center_x + 900)
            coordinate = [x_coord, 192]
            crate.position = coordinate
            self.scene.add_sprite("Crates", crate)
            self.brick_spritelist.append(crate)
            self.timer = 100
        else:
            self.timer -= 1

        self.score_timer += 1
        if self.score_timer % 50 == 0:
            self.score += 1

        if self.timer == 100:
            print(self.player_sprite.change_x)
            self.player_sprite.change_x += 1
        elif self.timer == 400:
            print(self.player_sprite.change_x)
            self.player_sprite.change_x += 1
        elif self.timer == 1600:
            print(self.player_sprite.change_x)
            self.player_sprite.change_x += 1
        elif self.timer == 4800:
            print(self.player_sprite.change_x)
            self.player_sprite.change_x += 1

        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.crate_list)
        for crate in hit_list:
            arcade.exit()



def main():
    window = arcade.Window(WIDTH, HEIGHT, "Running Man")
    window.total_score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()