# Pyframe
A python project who simplify your usage of pygame

# Init
With pyframe.py in the same directory than the project :
```
import pyframe
```
That's it !

# Seting up the variables
(```example.py``` is a good example)

> Setting up the window
```pyframe.GLOBAL_WIN = pygame.display.set_mode((width,height))```
or
```
width = 500; height = 500
WIN = pygame.display.set_mode((width,height))
pyframe.GLOBAL_WIN = WIN
```

> Setting up the max framerate (0 for infinite)
```
fps = 60
pyframe.set_framerate(fps)
```

> Handle binds
For pyframe to handle binds, you need this instruction in your mainloop, who run every frame
```
pyframe.events_loop()
```

And that's it ! You can now use pyframe.
