# A\* Pathfinder With Visulization

An A\* Pathfinding algorithm made completely in python.

## Features

-   Full GUI
-   Choose custom start and end points
-   Draw custom obsticles
-   Choose to visualize path finding process

## Requirements

This project requires pygame to be installed which can be done with one of the following commands depending your operating system and configuration:

```
pip install pygame
pip3 install pygame
python -m pip install pygame
python3 -m pip install pygame
```

## Usage

![Plot Points](/assets/Plot-points.png)

Choose the start and end coordinates for the pathfinding algorithm and choose if you wan visualization enabled.

Custom grid sizes are not yet supported so the coordinates have to be in between 0 and 29.

Once you have choosen the options you would like click "Submit" or push the `Enter` key on your keyboard.

![Draw Barriers](/assets/Draw-barriers.png)

Now you can define barriers you want the algorithm to avoid. To do so click and drag with your mouse on the grid.

![Find Path](/assets/Find-path.png)

Once you are ready to start pathfinding push `Space`.

To clear the grid push `c`.
