from songsLayout.songsLayout import *
from player.musicPlayer import *
from settings import *
from loader.downloader import *
from playerCLI.playerCLI import *


c = playerCLI(settings)
c.runCLI()