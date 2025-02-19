# Snapple Snake Game

## Description
Snapple is a modern take on the classic Snake game, developed using Python and the Pygame library. In this game, players navigate a snake around the screen, consuming food to grow in size while avoiding collisions with itself and the screen boundaries.

## Features
- **Dynamic Gameplay**: The game progressively increases in speed as the player accumulates points.
- **User-Friendly Interface**: Engaging visuals with an interactive menu and pause functionality.
- **Sound Effects**: Added audio feedback for eating food and game over events.
- **Multiple Game Screens**: Includes intro, pause, and game-over screens with background images.
- **Customizable Elements**: Colors, speeds, and other gameplay elements can be modified.

## Game Components
1. **User Interface**
   - Visually appealing intro screen where players can start the game.
   - A pause screen allows users to temporarily stop gameplay.
   - The game-over screen displays the final score and gives players the option to restart or quit.

2. **Snake Mechanics**
   - The snake starts with a small body and grows each time it eats food.
   - It can move in four directions (up, down, left, and right).
   - Collision detection prevents movement in the opposite direction to avoid instant self-collision.

3. **Food System**
   - Food spawns randomly on the screen.
   - When the snake eats the food, the player's score increases, and the snake's length grows.
   - The game speed increases at specific score intervals to add difficulty.

4. **Collision Detection**
   - If the snake collides with the screen edges or itself, the game ends, triggering the game-over screen.
   - A game-over sound is played when a collision occurs.

## Controls
- **Arrow Keys**: Move the snake in the respective direction.
- **P Key**: Pause the game.
- **Y Key**: Resume the game after pausing.
- **Q Key**: Quit the game.
- **R Key**: Restart the game after a game-over.

## How to Run the Game
1. Install Pygame if not already installed:
   pip install pygame
2. Run the script:
   python snapple.py

