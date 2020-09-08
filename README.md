# Example-01d-RPG

Example for MSCH-C220, 3 September 2020. This is a *very* rough implementation of a Python game engine that understands some of the macro features in Harlowe 3.1.0. This is offered as a simple example of how *not* to accomplish something like this; the right way is to create a generic compiler rather than to try to replicate behavior in Python. 

## Implementation

Built using Visual Studio Code and Python 3.8.5. rpg.html and rpg.json were created in Twine 2 and exported with Twison 0.0.1 (https://github.com/lazerwalker/twison)

## References

[Harlowe 3.1.0 documentation](https://twine2.neocities.org)
rpg.html is an adaptation of [this tutorial](http://lambdamaphone.blogspot.com/2015/02/using-twine-for-games-research-part-ii.html)

## Future Development

if/else blocks are currently not implemented. The target is a small subset of the Harlowe macro language. There may be bugs that don't account for whitespace, etc.

## Created by

Jason Francis
