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
## This mode keeps track of the awards and points for making the right ramp
## The intent is to have this be an always on mode, but to separate the code for readability
##

from procgame import *
import cc_modes
import ep

class RightRamp(ep.EP_Mode):
    """Cactus Canyon Right Ramp Mode"""
    def __init__(self, game, priority):
        super(RightRamp, self).__init__(game, priority)
        # Set up the sounds

    def mode_started(self):
        self.update_lamps()

    def mode_stopped(self):
        self.disable_lamps()

    def update_lamps(self):
        self.disable_lamps()
        ## if status is multiball check the jackpot and take actions
        lampStatus = self.game.show_tracking('lampStatus')
        # we bail here if the others don't match and it's not "ON"
        if lampStatus != "ON":
            return

        ## high noon check
        if self.game.show_tracking('highNoonStatus') == "RUNNING":
            self.game.lamps.rightRampSoundAlarm.schedule(0x00FF00FF)
            self.game.lamps.rightRampShootOut.schedule(0x00FF00FF)
            self.game.lamps.rightRampSavePolly.schedule(0x00FF00FF)
            self.game.lamps.rightRampJackpot.schedule(0x00FF00FF)
            return

        # goldmine multiball check
        if self.game.show_tracking('mineStatus') == "RUNNING":
            if self.game.show_tracking('jackpotStatus',4):
                self.game.lamps.rightRampJackpot.schedule(0x0F0FFE00)
                self.game.lamps.rightRampSavePolly.schedule(0x0F0F1F30)
                self.game.lamps.rightRampShootOut.schedule(0x0F0F03F1)
                self.game.lamps.rightRampSoundAlarm.schedule(0x0F0F007F)
            return

        # drunk multiball
        if self.game.show_tracking('drunkMultiballStatus') == "RUNNING":
        ## right ramp is #4 in the stampede jackpot list
            if 'rightRamp' in self.game.drunk_multiball.active:
                self.game.lamps.rightRampJackpot.schedule(0xF000F000)
                self.game.lamps.rightRampSavePolly.schedule(0xFF00FF00)
                self.game.lamps.rightRampShootOut.schedule(0xF0F0F0F0)
                self.game.lamps.rightRampSoundAlarm.schedule(0xF00FF00F)
            return

        # save polly
        if self.game.save_polly.running:
            self.game.lamps.rightRampSavePolly.schedule(0x0FF00FF0)
            self.game.lamps.rightRampShootOut.schedule(0x00FF00FF)
            self.game.lamps.rightRampSoundAlarm.schedule(0xF00FF00F)
            return
        # river chase
        if self.game.river_chase.running:
            self.game.lamps.rightRampSavePolly.schedule(0x0FF00FF0)
            self.game.lamps.rightRampShootOut.schedule(0x00FF00FF)
            self.game.lamps.rightRampSoundAlarm.schedule(0xF00FF00F)
            return
        # bank robbery
        if self.game.bank_robbery.running:
            if self.game.bank_robbery.isActive[2]:
                self.game.lamps.rightRampSavePolly.schedule(0x0FF00FF0)
                self.game.lamps.rightRampShootOut.schedule(0x00FF00FF)
                self.game.lamps.rightRampSoundAlarm.schedule(0xF00FF00F)
            return
        # bionic bart
        if self.game.show_tracking('bionicStatus') == "RUNNING":
            if 4 in self.game.bionic.activeShots:
                self.game.lamps.rightRampSoundAlarm.schedule(0x00FF00FF)
                self.game.lamps.rightRampShootOut.schedule(0x00FF00FF)
                self.game.lamps.rightRampSavePolly.schedule(0x00FF00FF)
                self.game.lamps.rightRampJackpot.schedule(0x00FF00FF)
            return

        # cva
        if self.game.show_tracking('cvaStatus') == "RUNNING":
            if self.game.cva.activeShot == 4:
                self.game.lamps.rightRampSoundAlarm.schedule(0x00FF00FF)
                self.game.lamps.rightRampShootOut.schedule(0x00FF00FF)
                self.game.lamps.rightRampSavePolly.schedule(0x00FF00FF)
                self.game.lamps.rightRampJackpot.schedule(0x00FF00FF)
            return

        stage = self.game.show_tracking('rightRampStage')

        if stage == 1:
            # blink the first light
            self.game.lamps.rightRampSoundAlarm.schedule(0x0F0F0F0F)
        elif stage == 2:
            # first light on
            self.game.lamps.rightRampSoundAlarm.enable()
            # blink the second
            self.game.lamps.rightRampShootOut.schedule(0x0F0F0F0F)
        elif stage == 3:
            # first two on
            self.game.lamps.rightRampSoundAlarm.enable()
            self.game.lamps.rightRampShootOut.enable()
            # blink the third
            self.game.lamps.rightRampSavePolly.schedule(0x0F0F0F0F)
        # this is completed - pulse the 3rd light
        elif stage == 5:
            # three on
            self.game.lamps.rightRampSoundAlarm.enable()
            self.game.lamps.rightRampShootOut.enable()
            self.game.lamps.rightRampSavePolly.enable()
        elif stage == 89:
        ## right ramp is #4 in the stampede jackpot list
            if self.game.stampede.active == 4:
                self.game.lamps.rightRampJackpot.schedule(0xF000F000)
                self.game.lamps.rightRampSavePolly.schedule(0xFF00FF00)
                self.game.lamps.rightRampShootOut.schedule(0xF0F0F0F0)
                self.game.lamps.rightRampSoundAlarm.schedule(0xF00FF00F)
            # if not active, just turn on the jackpot light only
            else:
                self.game.lamps.rightRampJackpot.schedule(0xFF00FF00)

        else:
            pass

    def disable_lamps(self):
        self.game.lamps.rightRampSoundAlarm.disable()
        self.game.lamps.rightRampShootOut.disable()
        self.game.lamps.rightRampSavePolly.disable()
        self.game.lamps.rightRampJackpot.disable()

    def sw_rightRampEnter_active(self,sw):
        # play the switch sound
        self.game.sound.play(self.game.assets.sfx_rightRampEnter)
        # score the arbitrary and wacky points
        self.game.score_with_bonus(2530)
        ## -- set the last switch hit --
        ep.last_switch = "rightRampEnter"

    def sw_rightRampMake_active(self,sw):
        # the actual game doesn't care if enter was just hit
        # so I don't either
        # tick one on to the total of player shots on the right ramp
        self.game.increase_tracking('rightRampShots')
        # check the chain status
        if ep.last_shot == "left":
            # if we're coming from the left ramp, increase the chain
            self.game.combos.increase_chain()
        else:
            # if not, set it back to one
            self.game.combos.chain = 1

        # score the points and mess with the combo
        if self.game.combos.myTimer > 0:
            # register the combo and reset the timer - returns true for use later
            combo = self.game.combos.hit()
        else:
            # and turn on the combo timer - returns false for use later
            combo = self.game.combos.start()

        # if a polly mode is running - let it go man
        if self.game.peril:
            pass
        else:
            self.award_ramp_score(combo)

        ## -- set the last switch hit --
        ep.last_switch = "rightRampMake"
        ep.last_shot = "right"


    def sw_rightRampBottom_active(self,sw):
        self.game.score_with_bonus(2530)
        ## -- set the last switch hit --
        ep.last_switch = "rightRampBottom"

    def award_ramp_score(self,combo):
        # cancel any other displays
        for mode in self.game.ep_modes:
            if getattr(mode, "abort_display", None):
                mode.abort_display()

        # TODO these all need fleshing out with sounds and final animations
        stage = self.game.show_tracking('rightRampStage')
        if stage == 1:
            ## set the text lines for the display later
            self.awardString = "SOUND ALARM"
            self.awardPoints = "125,000*"
            self.game.score_with_bonus(125000)
            # load the animation
            anim = self.game.assets.dmd_bankExplodes
            # calcuate the wait time to start the next part of the display
            myWait = len(anim.frames) / 8.57
            # play the first sound
            self.game.sound.play(self.game.assets.sfx_explosion1)
            self.game.base.play_quote(self.game.assets.quote_rightRamp1)
            # set the animation
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 7
            animLayer.opaque = True

            # added a frame listener for the second sound effect
            animLayer.add_frame_listener(5, self.game.sound.play,param=self.game.assets.sfx_fallAndCrash1)
            # play the animation
            self.layer = animLayer
            # add some score
            # apply the calculated delay to the next step
            self.delay(name="Display",delay=myWait,handler=self.blink_award_text)
        elif stage == 2:
            # set the text lines for the display
            self.awardString = "SHOOT OUT"
            self.awardPoints = "150,000*"
            self.game.score_with_bonus(150000)
            # load the animation
            anim = self.game.assets.dmd_bankSheriff
            # calculate the wait time
            myWait = len(anim.frames) / 8.57
            # set the animation
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold = True
            animLayer.frame_time = 7
            animLayer.opaque = True

            # add listener frames
            animLayer.add_frame_listener(15,self.game.sound.play,param=self.game.assets.sfx_explosion11)
            animLayer.add_frame_listener(17,self.game.sound.play,param=self.game.assets.sfx_explosion11)
            animLayer.add_frame_listener(19,self.game.sound.play,param=self.game.assets.sfx_explosion11)
            # play the start sound
            self.game.base.play_quote(self.game.assets.quote_rightRamp2)
            # play the animation
            self.layer = animLayer
            # apply the delay
            self.delay(name="Display",delay=myWait,handler=self.blink_award_text)

        elif stage == 3:
            self.game.increase_tracking('rightRampStage')
            self.game.modes.add(self.game.bank_robbery)
            self.game.bank_robbery.start_bank_robbery()


    ## for now, anything above 3 is 'complete'
        else:
            start_value = self.game.increase_tracking('adventureCompleteValue',5000)
            # vary the prize based on win/lose
            if self.game.bank_robbery.won:
                self.awardString = "ROBBERY FOILED"
                self.game.base.play_quote(self.game.assets.quote_victory)
                value = start_value
            else:
                self.awardString = "BANK ROBBED"
                value = start_value / 10
            self.awardPoints = str(ep.format_score(value)) + "*"
            self.game.score_with_bonus(value)
            # play sounds
            self.game.sound.play(self.game.assets.sfx_thrownCoins)
            # play animation
            if combo:
                self.layer = None
                self.game.combos.display()
            else:
                self.anim_bank_victory()

        # then tick the stage up for next time unless it's completed
        if self.game.show_tracking('rightRampStage') < 3:
            self.game.increase_tracking('rightRampStage')
            # do a little lamp flourish
            self.game.lamps.rightRampSoundAlarm.schedule(0x00FF00FF)
            self.game.lamps.rightRampShootOut.schedule(0x0FF00FF0)
            self.game.lamps.rightRampSavePolly.schedule(0xFF00FF00)
            # update the lamps
            self.delay(delay=1,handler=self.update_lamps)
            self.game.center_ramp.update_lamps()

    def anim_bank_victory(self):
        if self.game.bank_robbery.won:
            print "BANK VICTORY"
            anim = self.game.assets.dmd_pollyVictory
            myWait = len(anim.frames) / 8.57
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=True
            animLayer.frame_time = 7
            animLayer.opaque = True

            animLayer.add_frame_listener(7,self.game.sound.play,param=self.game.assets.sfx_blow)
            animLayer.add_frame_listener(14,self.game.sound.play,param=self.game.assets.sfx_grinDing)
            # play animation
            self.layer = animLayer
        else:
            backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_poutySheriff.frames[0])
            textLine1 = dmd.TextLayer(25,8,self.game.assets.font_12px_az,justify="center",opaque=False).set_text("TOO")
            textLine2 = dmd.TextLayer(98,8,self.game.assets.font_12px_az,justify="center",opaque=False).set_text("LATE!")
            combined = dmd.GroupedLayer(128,32,[backdrop,textLine1,textLine2])
            self.layer = combined
            myWait = 1.5

        self.delay(name="Display",delay=myWait,handler=self.blink_award_text)

    def blink_award_text(self):
        # stage one of showing the award text - this one blinks
        self.build_award_text(12)
        # switch to solid in 1 seconds
        self.delay(name="Display",delay=1,handler=self.show_award_text)

    def show_award_text(self):
        # stage 2 of showing the award text
        self.build_award_text()
        # turn it off in 1 seconds
        self.delay(name="Display",delay=1,handler=self.clear_layer)
        # show combo display if the chain is high enough
        if self.game.combos.chain > 1:
            self.delay(name="Display",delay=1,handler=self.game.combos.display)

    def build_award_text(self,blink=None):
        # create the two text lines
        awardTextTop = dmd.TextLayer(128/2,3,self.game.assets.font_5px_bold_AZ_outline,justify="center",opaque=False)
        awardTextBottom = dmd.TextLayer(128/2,11,self.game.assets.font_15px_az_outline,justify="center",opaque=False)
        awardTextBottom.composite_op = "blacksrc"
        awardTextTop.composite_op = "blacksrc"

        # if blink frames we have to set them
        if blink:
            awardTextTop.set_text(self.awardString,blink_frames=12)
            awardTextBottom.set_text(self.awardPoints,blink_frames=12)
        else:
            awardTextTop.set_text(self.awardString)
            awardTextBottom.set_text(self.awardPoints)
            #awardTextmask.set_text(self.awardPoints)
        # combine them
        completeFrame = dmd.GroupedLayer(128, 32, [self.layer,awardTextTop,awardTextBottom])
        # swap in the new layer
        self.layer = completeFrame

    def abort_display(self):
        self.clear_layer()
        self.cancel_delayed("Display")
