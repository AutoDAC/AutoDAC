import os
NO_DISPLAY = bool(os.environ['NO_DISPLAY']) if 'NO_DISPLAY' in os.environ else False
DEBUGGING = True
MOVEMENT_LENGTH = 2 if DEBUGGING else 0  # Moving mouse takes this many seconds
