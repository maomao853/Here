# -*- coding: utf-8 -*-

# These must be specified to prevent wrapper import errors
AUTHOR = "maomao853"
VERSION = (1, 0, 0)  # DEFAULT (0, 1)
NAME = "Here"
SUMMARY = "Displays your coordinates to the entire server"
DESCRIPTION = """This plugin is activated by !here command.
It will display your coordinates to the entire Minecraft server.
For overworld and nether dimensions, it will also convert and display the corresponding coordinates in the opposite dimension.
Dimension display doesn't work without proxy.
"""

# Disables plugin
# TODO this plugin is Disabled to run it change this line:
DISABLED = False  # DEFAULT = False


# noinspection PyMethodMayBeStatic,PyUnusedLocal
# noinspection PyPep8Naming,PyClassicStyleClass,PyAttributeOutsideInit
class Main:
    def __init__(self, api, log):
        self.api = api
        self.log = log
        self.minecraft = api.minecraft

    def onEnable(self):
        # you can disable the plugin by returning False!

        # use wrapper-data/plugins folder
        self.data = self.api.getStorage("Here", False)

        self.api.registerCommand("here", self.here,)
        self.api.registerCommand("_display", self._display, )

        self.api.registerHelp(
            "Here", "description of plugin 'Here'",
            [  # help items
                ("!here", "!here to display your coordinates", "permission.node"),
            ]
        )

        # Everyone can use '/topic3'!
        self.api.registerPermission("permission.node", True)

        # Registered events
        self.api.registerEvent("player.message", self._np_commands)

    def onDisable(self):
        # save Storage to disk and close the Storage's periodicsave() thread.
        self.data.close()

    # Events section
    def _np_commands(self, payload):
        player = payload["player"]
        words = payload["message"].split(" ")
        if words[0][0] == "!":
            command = words[0][1:].lower()
            if len(words) > 1:
                subcomm = words[1].lower()
            else:
                subcomm = "nope"
            if command in ("here") and subcomm in ("?", "h", "help"):
                player.message("&eHome plugin Help:")
                player.message("&e!set - set your position.")
                player.message("&e!sethome - set your home (after !set).")
                player.message("&e!home - Go to your home.")
                player.message("&e!homes - advanced topic.")
            elif command == "here":
                self.here(player, words[1:])

    # Commands section
    def here(self, player, args):
        if len(args) > 0:
            player.message({"text": "!here does not take any arguments",
                            "color": "red"})
            return
        Dimensions = ["[Overworld]", "[End]", "[Nether]"]
        position = player.getPosition()
        dim = player.getDimension()
        #overworld
        if dim == 0:
            dispDim = Dimensions[dim]
            dispDimOpp = Dimensions[dim-1]
        #Nether
        elif dim == -1:
            dispDim = Dimensions[dim]
            dispDimOpp = Dimensions[dim+1]
        #End
        elif dim == 1:
            dispDim = Dimensions[dim]
        self._display(player, player.username, dispDim, position, dispDimOpp, dim)

    def _display(self, userobj, username, dispDim, xyzcoords, dispDimOpp, dim):
        self.minecraft.broadcast("dimension" + dispDim + str(dim))
        if dispDim == 0:
            self.minecraft.broadcast("§f%s §6@ §a%s %s %s %s §7-> §c%s %s %s %s" % (
                username, dispDim, xyzcoords[0], xyzcoords[1], xyzcoords[2], dispDimOpp, xyzcoords[0]*8, xyzcoords[1]*8, xyzcoords[2]*8
            ))
        elif dispDim == (-1):
            self.minecraft.broadcast("§f%s §6@ §c%s %s %s %s §7-> §a%s %s %s %s" % (
                username, dispDim, xyzcoords[0], xyzcoords[1], xyzcoords[2], dispDimOpp, xyzcoords[0]/8, xyzcoords[1]/8, xyzcoords[2]/8
            ))
        elif dispDim == 1:
            self.minecraft.broadcast("§f%s §6@ §e%s %s %s %s" % (
                username, dispDim, xyzcoords[0], xyzcoords[1], xyzcoords[2]
            ))

        return