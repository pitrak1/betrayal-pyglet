# Betrayal at House on the Hill

This is a version of the board game Betrayal at House on the Hill, written using the following packages:

- python
- pip
- pyglet
- pytest
- pytest-mock

All of the following can be installed using pip.

## Running

To run test, run `<python3> -m pytest`.  This is important to do instead of running just `pytest` directly because importing relies on the root directory.  Running `pytest` directly makes the root directory for each test file the directory that file is in, whereas `<python3> -m pytest` makes the root directory the root directory of the repo, allowing us to import modules relative to the root directory of the repo.

To run the app itself, run `<python3> main.py` in the root directory.

## Notes

This project is obviously in its infancy with only a few proofs of concept currently.

How I envision this project working is this:

The draw and update handlers will operate on the same tree (ignoring pyglet's batch drawing options).  Input handlers will add commands to a command queue, and on update, those commands will be popped off and sent down the tree.  Nodes within the tree will either be sent the command queue itself or a callback to add commands to the queue, so either way, nodes handling commands may also add commands of their own to be handled.