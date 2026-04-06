# Bird Scaring Game

## Overview
This is a game in which you move your character up to crows to scare them away. Doing so earns you points which you can use on upgrades.
Use WASD to move around.

This project is built with the PyGame library

## Technical Implementations
### Bird Spawning
Bird spawning is run on a timer where the duration is randomly selected from within a range each time a bird a bird is spawned. A random position within the play bounds is chosen, called the `target_pos`, which is passed into a function to get the `start_pos`. The start position is found by detecting the side of the screen the `target_pos` is closest to, then randomly generating a distance outside of the screen, on the selected side.

### Sound Effects
The sound effects are implemented with `pygame.mixer`. Mostly nothing special is required, however the sound that plays while a bird is flying required some extra code. During initialisation, three audio channels are reserved for this sound, then during the update loop, the number of currently flying birds are counted. The game allows that many channels to play, though obviously capped by the amount of channels that were reserved (three). This is necessary because the flying sound effect plays so often that it blocks other sounds from playing, and too many playing at once gets much too loud and overpowering.

## Future Improvements
Biggest areas for improvements are the sound effects could do with some tweaking to make them more enjoyable to listen to, and the player movement could be made less simplistic to make it more satisfying.
