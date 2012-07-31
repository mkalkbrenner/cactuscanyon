##   ____           _                ____
##  / ___|__ _  ___| |_ _   _ ___   / ___|__ _ _ __  _   _  ___  _ __
## | |   / _` |/ __| __| | | / __| | |   / _` | '_ \| | | |/ _ \| '_ \
## | |__| (_| | (__| |_| |_| \__ \ | |__| (_| | | | | |_| | (_) | | | |
##  \____\__,_|\___|\__|\__,_|___/  \____\__,_|_| |_|\__, |\___/|_| |_|
##                                                   |___/
##           ___ ___  _  _ _____ ___ _  _ _   _ ___ ___
##          / __/ _ \| \| |_   _|_ _| \| | | | | __|   \
##         | (_| (_) | .` | | |  | || .` | |_| | _|| |) |
##          \___\___/|_|\_| |_| |___|_|\_|\___/|___|___/
##
## A P-ROC Project by Eric Priepke
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
## Original Cactus Canyon software by Matt Coriale
##
##
## The match animation routine
## Crutched on myPinball's IJ match routine heavily.
##

from procgame import *
from assets import *
import cc_modes
import random
import ep

class Match(ep.EP_Mode):
    """Cactus Canyon AttractMode"""
    def __init__(self, game, priority):
        super(Match, self).__init__(game, priority)
        self.digitLayer = dmd.TextLayer(76,13, self.game.assets.font_13px_thin_score, "center")
        self.zeroLayer = dmd.TextLayer(88,13, self.game.assets.font_13px_thin_score, "center").set_text("0")
        self.p1Layer = dmd.TextLayer(16, 1, self.game.assets.font_7px_az, "right", opaque=False)
        self.p2Layer = dmd.TextLayer(16, 9, self.game.assets.font_7px_az, "right", opaque=False)
        self.p3Layer = dmd.TextLayer(16, 17, self.game.assets.font_7px_az, "right", opaque=False)
        self.p4Layer = dmd.TextLayer(16, 25, self.game.assets.font_7px_az, "right", opaque=False)
        self.playerDigits = [0,0,0,0]
        self.playerLayers=[self.p1Layer,self.p2Layer,self.p3Layer,self.p4Layer]

    # TODO maybe set this up so it shows full scores, then they scroll off to the left for more pizazz

    def mode_started(self):
        self.winners = 0

    def run_match(self):
        self.game.sound.play(self.game.assets.sfx_ragtimePiano)
        possiblities = ["0","1","2","3","4","5","6","7","8","9"]
        # pick a random number
        self.selection = random.choice(possiblities)
        self.digitLayer.set_text(self.selection)
        # grab the last two digits of the scores  ... somehow?
        self.generate_digits()
        # put up the end of the scores
        # put up the bottles
        bottlesLayer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'match.dmd').frames[0])
        bottlesLayer.composite_op = "blacksrc"
        # put up the match number
        # text
        textLayer1 = dmd.TextLayer(20, 1, self.game.assets.font_7px_az, "center", opaque=False).set_text("MATCH",blink_frames=12)
        textLayer2 = dmd.TextLayer(20, 9, self.game.assets.font_7px_az, "center", opaque=False).set_text("TO",blink_frames=12)
        textLayer3 = dmd.TextLayer(20, 17, self.game.assets.font_7px_az, "center", opaque=False).set_text("WIN",blink_frames=12)

        combined = dmd.GroupedLayer(128,32,[self.p1Layer,self.p2Layer,self.p3Layer,self.p4Layer,bottlesLayer,textLayer1,textLayer2,textLayer3])

        # this is the first display with the bottles and score endings
        self.layer = combined
        # hold for 2 seconds, then animate
        self.delay(delay=2,handler=self.run_animation)

    def run_animation(self):
        # run the animation with sound
        # load up the animation
        anim = dmd.Animation().load(ep.DMD_PATH+'match.dmd')
        # start the full on animation
        myWait = len(anim.frames) / 7.5 + 0.5
        # setup the animated layer
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold=True
        animLayer.frame_time = 8
        animLayer.composite_op = "blacksrc"
        combined = dmd.GroupedLayer(128,32,[self.digitLayer,self.zeroLayer,self.p1Layer,self.p2Layer,self.p3Layer,self.p4Layer,animLayer])
        # fire it up
        self.layer = combined
        self.fire("LEFT")
        self.delay(delay=0.125,handler=self.game.sound.play,param=self.game.assets.sfx_breakingGlass1)
        self.delay(delay=0.5,handler=self.fire,param="RIGHT")
        self.delay(delay=0.625,handler=self.game.sound.play,param=self.game.assets.sfx_breakingGlass1)
        self.delay(delay=1,handler=self.fire,param="LEFT")
        self.delay(delay=1.125,handler=self.game.sound.play,param=self.game.assets.sfx_breakingGlass1)
        self.delay(delay=1.125,handler=self.fire,param="RIGHT")
        self.delay(delay=1.250,handler=self.game.sound.play,param=self.game.assets.sfx_breakingGlass1)
        self.delay(delay=1.625,handler=self.fire,param="LEFT")
        self.delay(delay=1.75,handler=self.game.sound.play,param=self.game.assets.sfx_breakingGlass1)
        self.delay(delay=1.75,handler=self.fire,param="RIGHT")
        self.delay(delay=1.875,handler=self.game.sound.play,param=self.game.assets.sfx_breakingGlass1)


        # after the animation ends, see if anybody won and run that action
        self.delay(delay = myWait,handler=self.award_match)

    def award_match(self):
        # check the scores to see if anybody won
        for i in range(len(self.game.players)):
            if str(self.playerDigits[i]) == self.selection:
                # set the text on that layer to blink
                self.playerLayers[i].set_text(str(self.playerDigits[i]) + "0",blink_frames=8)
                # and tick the winner count to true
                self.winners += 1

        # if we had any winners there's stuff to do
        if self.winners > 0:
            self.digitLayer.set_text(self.selection,blink_frames=8)
            self.zeroLayer.set_text("0",blink_frames=8)
            bottlesLayer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'match.dmd').frames[20])
            bottlesLayer.composite_op = "blacksrc"
            combined = dmd.GroupedLayer(128,32,[self.digitLayer,self.zeroLayer,self.p1Layer,self.p2Layer,self.p3Layer,self.p4Layer,bottlesLayer])
            self.layer = combined
            # TODO play the knocker once for each winner
            #self.game.knock(self.winners)

        # Then delay for 2 seconds and shut 'er down
        self.delay(delay=2,handler=self.finish_up)

    def fire(self,side):
        self.game.sound.play(self.game.assets.sfx_explosion11)
        if side == "LEFT":
            self.game.coils.leftGunFlasher.pulse(30)
        if side == "RIGHT":
            self.game.coils.rightGunFlasher.pulse(30)

    def generate_digits(self):
        #extract and display the last 2 score digits for each player

        for i in range(len(self.game.players)):
            score = self.game.players[i].score
            print "PLAYER SCORE - " + str(score)
            digit = str(score)[-2:-1]
            print "MATCH DIGITS - " + str(digit)
            digitString = str(digit) + "0"
            self.playerLayers[i].set_text(digitString)
            #set var for comparison
            self.playerDigits[i]=digit

    def finish_up(self):
        # run the high score routine after the match
        self.game.run_highscore()
        # and remove thyself.
        self.unload()