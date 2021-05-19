import json
import time
import threading

from songsLayout.songsLayout import *
from player.musicPlayer import *
from tabulate import *



class playerCLI():
    def __init__(self, settings):
        self.settings = settings
            
        with open(self.settings['layoutPath']) as l:
            self.sLayout = json.load(l)

        self.songInd = 0
        self.queue = []
        self.state = 'stop'
        self.songLayout = songsLayout(settings)
        self.player = musicPlayer()
        self.playerRun = False

        # key should be in lower case
        self.argsCheck = {
            'help' : {'command' : 'help', 'N' : 0, 'type' : [], 'args' : [''], 'confirm' : False},
            'pcreate' : {'command' : 'Pcreate', 'N' : 1, 'type' : [str], 'args' : ['playlistName'], 'confirm' : False},
            'pdelete' : {'command' : 'Pdelete', 'N' : 1, 'type' : [str], 'args' : ['playlistName'], 'confirm' : True},
            'sadd' : {'command' : 'Sadd', 'N' : 2, 'type' : [str, str], 'args' : ['playlistName', 'songName'], 'confirm' : False},
            'sremove' : {'command' : 'Sremove', 'N' : 2, 'type' : [str, str], 'args' : ['playlistName', 'songName'], 'confirm' : True},
            'sdelete' : {'command' : 'Sdelete', 'N' : 1, 'type' : [str], 'args' : ['songName'], 'confirm' : True},
            'pget' : {'command' : 'Pget', 'N' : 0, 'type' : [], 'args' : [], 'confirm' : False},
            'sget' : {'command' : 'Sget', 'N' : 1, 'type' : [str], 'args' : ['playlistName'], 'confirm' : False},
            'sgetall' : {'command' : 'Sgetall', 'N' : 0, 'type' : [], 'args' : [], 'confirm' : False},
            'lclear' : {'command' : 'Lclear', 'N' : 0, 'type' : [], 'args' : [], 'confirm' : True},
            'deleteall' : {'command' : 'deleteAll', 'N' : 0, 'type' : [], 'args' : [], 'confirm' : True},
            'pplay' : {'command' : 'Pplay', 'N' : 1, 'type' : [str], 'args' : ['playlistName'], 'confirm' : False},
            'play' : {'command' : 'play', 'N' : 1, 'type' : [str], 'args' : ['songName'], 'confirm' : False},
            'stop' : {'command' : 'stop', 'N' : 0, 'type' : [], 'args' : [], 'confirm' : False},
            'pause' : {'command' : 'pause', 'N' : 0, 'type' : [], 'args' : [], 'confirm' : False},
            'unpause' : {'command' : 'unpause', 'N' : 0, 'type' : [], 'args' : [], 'confirm' : False},
            'next' : {'command' : 'next', 'N' : 0, 'type' : [], 'args' : [], 'confirm' : False},
            'exit' : {'command' : 'exit', 'N' : 0, 'type' : [], 'args' : [], 'confirm' : True},
        }

    '''
        refresh Layout
    '''
    def refreshLayout(self):
        with open(self.settings['layoutPath']) as l:
            self.sLayout = json.load(l)


    '''
        player for the song using state and queue 
    '''
    def playerLoop(self):
        
        currentState = 'stop'
        while self.playerRun:

            try:
                if currentState != self.state:
                    if self.state == 'play':
                        self.player.play(self.queue[self.songInd]['name'], self.queue[self.songInd]['path'])
                        self.state = 'playing'  
                        currentState = self.state

                    elif self.state == 'stop':
                        self.songInd = 0
                        self.player.stop()
                        currentState = self.state
                    
                    elif self.state == 'pause':
                        self.player.pause()
                        currentState = self.state
                    
                    elif self.state == 'unpause':
                        self.player.unpause()
                        currentState = self.state

                    elif self.state == 'next':
                        self.player.stop()
                        self.songInd += 1
                        self.state = 'play'
                        if self.songInd >= len(self.queue):
                            self.state = "stop"

            except Exception as e:
                self.state = 'next'
                print(e)

            if not self.player.playCheck() and self.state == 'playing':
                self.state = 'next'
    '''
        CLI for the player
    '''
    def runCLI(self):

        self.playerRun = True
        self.playerThread = threading.Thread(target=self.playerLoop)
        self.playerThread.start()
        print("Player started")

        run = True
        while run:
            # get command entered by user, check if its valid
            time.sleep(1)
            print(">", end=" ")
            try:
                command_entered = input()

                if "\"" in command_entered:
                    command_entered = command_entered.split("\"")
                    command_entered = list(map(lambda x : x.strip(" "), command_entered))
                    if " " in command_entered[0]:
                        new_command_entered = command_entered[0].split(" ")
                        new_command_entered.extend(command_entered[1:]) 
                        command_entered = new_command_entered
                else:
                    command_entered = command_entered.split(" ")

                command_entered = list(filter(lambda x : x!='' and x!=" ", command_entered)) 

                # extract command, args, flags
                command, args = command_entered[0].lower(), command_entered[1:]
                flags = []

            except Exception as e:
                print(f'enter proper command, use help to get all commands')
                continue

            
            for arg in args:
                if arg[0] == '-':
                    args.pop(args.index(arg))
                    flags.append(arg)

            # check if command exists
            if  command not in self.argsCheck:
                print(f'no such command {command}, use help to get all commands')
                continue

            # args check
            if len(args) < self.argsCheck[command]['N']:
                Pcommand = self.argsCheck[command]['command']
                print(f'Too few args for {Pcommand}, use help to check args')
                continue
            elif len(args) > self.argsCheck[command]['N']:
                Pcommand = self.argsCheck[command]['command']
                print(f'Too many args for {Pcommand}, use help to check args')
                continue
            else:
                typeCheck = True
                Pcommand = self.argsCheck[command]['command']
                for i in range(self.argsCheck[command]['N']):
                    if type(args[i]) != self.argsCheck[command]['type'][i]:
                        print(f'wrongs arguments for {Pcommand}, use help to check args')
                        typeCheck = False
                        break
                
                if not typeCheck:
                    continue

            # ask for confirmation        
            if self.argsCheck[command]['confirm']:
                confirmFlag = 0
                while confirmFlag == 0:
                    print('are you sure you want to run the command? (Y/N)', end=" : ")
                    confirm = input()
                    if confirm.lower() == 'n':
                        confirmFlag = -1
                    elif confirm.lower() == 'y':
                        confirmFlag = 1
                    else:
                        print('invalid literal')
                if confirmFlag == -1:
                    continue

            # command handling
            if command == 'help':
                helpList = []
                for cmd in self.argsCheck:
                    helpList.append((self.argsCheck[cmd]['command'], ", ".join(self.argsCheck[cmd]['args'])))
                
                print(tabulate(helpList, headers=["command", "args"]))
                continue

            elif command == 'pcreate':
                try:
                    self.songLayout.createPlaylist(args[0])
                    self.refreshLayout()
                except Exception as e:
                    print(e)

                continue
            
            elif command == 'pdelete':
                try:
                    self.songLayout.deletePlaylist(args[0])
                    self.refreshLayout()
                except Exception as e:
                    print(e)

                continue
            
            elif command == 'sadd':
                try:
                    self.songLayout.addSong(args[0], args[1])
                    self.refreshLayout()
                except Exception as e:
                    print(e)

                continue

            elif command == 'sremove':
                try:
                    self.songLayout.removeSong(args[0], args[1])
                    self.refreshLayout()
                except Exception as e:
                    print(e)

                continue
            
            elif command == 'sdelete':
                try:
                    self.songLayout.deleteSong(args[0])
                    self.refreshLayout()
                except Exception as e:
                    print(e)

                continue

            elif command == 'pget':
                try:
                    Plist = self.songLayout.getPlaylist()
                    Plist = [(i+1, p) for i, p in enumerate(Plist)]
                    print(tabulate(Plist, headers=["No.", "Playlist"]))
                except Exception as e:
                    print(e)

                continue

            elif command == 'sget':
                try:
                    Slist = self.songLayout.getSongs(args[0])
                    Slist = [(i+1, p) for i, p in enumerate(Slist)]
                    print(tabulate(Slist, headers=["No.", "Song"]))
                except Exception as e:
                    print(e)

                continue

            elif command == 'sgetall':
                try:
                    Slist = self.songLayout.getAllSongs()
                    Slist = [(i+1, p) for i, p in enumerate(Slist)]
                    print(tabulate(Slist, headers=["No.", "Song"]))
                except Exception as e:
                    print(e)

                continue

            elif command == 'lclear':
                try:
                    self.songLayout.clearLayout()
                    self.refreshLayout()
                except Exception as e:
                    print(e)

                continue
            
            elif command == 'deleteall':
                try:
                    self.songLayout.deleteAll()
                    self.refreshLayout()
                except Exception as e:
                    print(e)

                continue

            elif command == 'pplay':
                self.songInd = 0
                self.queue = []
                if args[0] not in self.sLayout:
                    print(f'no playlist exists : {args[0]}')
                    continue
                for songName in self.sLayout[args[0]]['songs']:
                    self.queue.append({
                        'name' : self.sLayout[args[0]]['songs'][songName]['file'],
                        'path' : os.path.join(self.settings['downloadPath'], self.sLayout[args[0]]['songs'][songName]['file'])
                        })
                
                self.state = 'play'
                continue

            elif command == 'play':
                self.songInd = 0
                self.queue = []
                if args[0] not in self.sLayout[self.settings['allSongs']]['songs']:
                    print(f'no song exists : {args[0]}')
                    continue

                self.queue.append({
                    'name' : self.sLayout[self.settings['allSongs']]['songs'][args[0]]['file'],
                    'path' : os.path.join(self.settings['downloadPath'], self.sLayout[self.settings['allSongs']]['songs'][args[0]]['file'])
                    })
                
                self.state = 'play'
                continue
            
            elif command == 'stop':                
                self.state = 'stop'
                continue

            elif command == 'pause':                
                self.state = 'pause'
                continue

            elif command == 'unpause':                
                self.state = 'unpause'
                continue

            elif command == 'next':                
                self.state = 'next'
                continue

            elif command == 'exit':
                break

        self.playerRun = False
    

        


