# %%
from songsLayout.songsLayout import *
from player.musicPlayer import *
from settings import *
from loader.downloader import *
from playerCLI.playerCLI import *

# s = songsLayout(settings)
# d = downloader(settings)
# x = d.download('lemon tree', 'https://www.youtube.com/watch?v=l2UiY2wivTs')
# print(x['format'])

c = playerCLI(settings)
c.runCLI()

# m = musicPlayer()
# %%
