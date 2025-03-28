
# Robber Vs Police: The Escape Plan

## Overview

Robber Vs Police: The Escape Plan is a 2D interactive game built with Python and Pygame, simulating a high-stakes heist where a robber must escape while evading AI-driven police patrols. The game features real-time movement, obstacle navigation, and dynamic enemy pursuit using the A* search algorithm.

This project explores AI-based pathfinding, comparing player strategies with algorithmic optimal routes. It demonstrates how artificial intelligence enhances chase dynamics, making gameplay unpredictable and engaging. 

## Features

- The robber can set checkpoints to navigate across the grid.
- Police officers use the A* pathfinding algorithm to chase the robber dynamically.
- The game includes a countdown timer; the player wins if the robber survives for 30 seconds.
- Game over occurs when the police catch the robber.
- Real-time movement with strategic decision-making.
- Procedurally generated obstacles for added challenge.

## Technologies Used

- Python
- Pygame
- Pathfinding (A* Algorithm)

## Installation

1. Install Python (>=3.7)
2. Install dependencies:
   ```sh
   pip install pygame pathfinding
   ```
3. Clone this repository:
   ```sh
   git clone <repository_url>
   ```
4. Navigate to the project folder:
   ```sh
   cd Robber-Vs-Police-The-Escape-Plan
   ```

## How to Play

1. Run the game:
   ```sh
   python main.py
   ```
2. Left-click to set checkpoints for the robber.
3. Avoid police while reaching checkpoints.
4. Survive for 30 seconds to win!

## Game Controls

- **Left Mouse Click**: Set a checkpoint for the robber.
- **Quit**: Close the game window.

## Game Mechanics

- **Pathfinding AI**: The police dynamically adjust their patrol routes based on the robber's position.
- **Escape Strategy**: Players must use the grid layout wisely to evade capture.
- **Obstacle Navigation**: Randomized obstacles make each playthrough unique.
- **Time-Based Challenge**: Survive the countdown to win the game.

## Screenshots

### Gameplay Demonstration
![Gameplay](../images/gameplay.png)

### Robber and Police Interaction
![Chase Scene](../images/chase.png)

### Game Over Screen
![Game Over](../images/game_over.png)

## Assets

Ensure the following assets are in the project folder:

- `robber.png`
- `police.png`
- `map.png`
- `selection.png`

## Future Improvements

- Implement different AI behaviors for police.
- Add multiple difficulty levels.
- Improve graphics and UI.
- Introduce power-ups and additional game modes.
- Multiplayer mode with cooperative and competitive gameplay.

## License

This project is open-source. Feel free to modify and improve!

## Author

Developed by Abhimanyu Kumar


