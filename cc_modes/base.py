##
## This Class is the mode that runs at all times during active play as a catch all
## Any general events that don't apply to any particular mode will end up handled here
## Like awarding points for hitting the slingshots - or the outlanes - or the start
## button is pressed - etc,
##
## Where to put combos? quickdraws? More modes? or stick them here?
## HMMMM


from procgame import *
from assets import *
import ep
import random


class BaseGameMode(ep.EP_Mode):
    """docstring for AttractMode"""
    def __init__(self, game,priority):
        super(BaseGameMode, self).__init__(game, priority)
        self.ball_starting = True
        # rank - set up the bulb list
        self.rankLamps = [self.game.lamps.rankStranger,
                          self.game.lamps.rankPartner,
                          self.game.lamps.rankDeputy,
                          self.game.lamps.rankSheriff,
                          self.game.lamps.rankMarshall]
        self.current_music = self.game.assets.music_mainTheme
        self.mug_shots = self.game.user_settings['Gameplay (Feature)']['Beer Mug Hits For Multiball']
        self.unbusy()

    def mode_started(self):
        print "INTERRUPTER IS DISPATCHING DELAYS"

        ## cancel the closing song delay, just in case
        self.game.interrupter.dispatch_delayed()
        # and update the lamps
        self.game.update_lamps()

    def mode_stopped(self):
        # Ensure flippers are disabled
        self.game.enable_flippers(enable=False)
        # Deactivate the ball search logic so it won't search due to no
        # switches being hit.
        self.game.ball_search.disable()
        # shut down all the modes
        self.remove_modes()

    def load_modes(self):
        self.game.modes.add(self.game.bonus_lanes)
        self.game.modes.add(self.game.combos)
        self.game.modes.add(self.game.right_ramp)
        self.game.modes.add(self.game.left_ramp)
        self.game.modes.add(self.game.center_ramp)
        self.game.modes.add(self.game.left_loop)
        self.game.modes.add(self.game.right_loop)
        self.game.modes.add(self.game.mine)
        self.game.modes.add(self.game.saloon)
        self.game.modes.add(self.game.bart)
        self.game.modes.add(self.game.bad_guys)

    def remove_modes(self):
        self.game.modes.remove(self.game.bonus_lanes)
        self.game.modes.remove(self.game.combos)
        self.game.modes.remove(self.game.right_ramp)
        self.game.modes.remove(self.game.left_ramp)
        self.game.modes.remove(self.game.center_ramp)
        self.game.modes.remove(self.game.left_loop)
        self.game.modes.remove(self.game.right_loop)
        self.game.modes.remove(self.game.mine)
        self.game.modes.remove(self.game.bart)
        self.game.modes.remove(self.game.saloon)
        self.game.modes.remove(self.game.bad_guys)

    def ball_drained(self):
        print "CHECKING TRACKING ball drained LR: " + str(self.game.show_tracking('leftRampStage'))
        # if that was the last ball in play need to finish up - unless high noon is finishing up
        if self.game.trough.num_balls_in_play == 0 and self.game.show_tracking('highNoonStatus') != "FINISH":
            # turn off all the lights
            for lamp in self.game.lamps:
                lamp.disable()
            # stop the music
            print "game.ball_drained IS KILLING THE MUSIC"
            self.game.sound.stop_music()
            # turn off ball save
            self.game.ball_search.disable()
            # turn off the flippers
            self.game.enable_flippers(False)
            # unload the modes
            self.remove_modes()
            if self.game.show_tracking('tiltStatus') != 3:
                # go check the bonus - after that we'll finish the ball
                # delay 1 second to give other modes time too set the busy if needed
                self.delay(delay=1,handler=self.check_bonus)
            else:
                self.layer = None
                self.game.ball_ended()

    def update_lamps(self):
        # reset first
        self.disable_lamps()
        status = self.game.show_tracking('lampStatus')
        ## if status is off, we bail here
        if status != "ON" or self.game.show_tracking('bionicStatus') == "RUNNING":
            return
        # left side - either the playfield light is on or blinking, or the inlane light is on
        left = self.game.show_tracking('quickdrawStatus',0)
        if left == 'OPEN':
            self.game.lamps.leftQuickdraw.enable()
        elif left == 'TOP' or left == 'BOT':
            self.game.lamps.leftQuickdraw.schedule(0x00FF00FF)
        elif left == 'READY':
            self.game.lamps.leftReturnQuickdraw.schedule(0x00FF00FF)
        else:
            pass
        # right has 2 lights so if unhit the light appropriate is on, or the inlane if ready
        right = self.game.show_tracking('quickdrawStatus',1)
        if right == 'OPEN':
            self.game.lamps.topRightQuickdraw.enable()
            self.game.lamps.bottomRightQuickdraw.enable()
        elif right == 'TOP':
            self.game.lamps.bottomRightQuickdraw.enable()
        elif right == 'BOT':
            self.game.lamps.topRightQuickdraw.enable()
        elif right == 'READY':
            self.game.lamps.rightReturnQuickdraw.schedule(0x00FF00FF)
        else:
            pass
        ## on a second pass thorugh the returns - if showdown is ready, flash 'em
        if self.game.show_tracking('showdownStatus') == "READY" or self.game.show_tracking('ambushStatus') == "READY":
            self.game.lamps.rightReturnQuickdraw.schedule(0x0F0F0F0F)
            self.game.lamps.leftReturnQuickdraw.schedule(0xF0F0F0F0)
        # extra ball
        if self.game.current_player().extra_balls > 0:
            self.game.lamps.shootAgain.enable()
        # the rank lights
        rank = self.game.show_tracking('rank')
        # loop through 0 through current rank and turn the lamps on
        for lamp in range(0,(rank +1),1):
            self.rankLamps[lamp].enable()

    def disable_lamps(self):
        for lamp in self.rankLamps:
            lamp.disable()
        self.game.lamps.leftQuickdraw.disable()
        self.game.lamps.bottomRightQuickdraw.disable()
        self.game.lamps.topRightQuickdraw.disable()
        self.game.lamps.leftReturnQuickdraw.disable()
        self.game.lamps.rightReturnQuickdraw.disable()
        self.game.lamps.shootAgain.disable()

    def sw_startButton_active(self, sw):
        # if start button is pressed during the game
        # if we're on the first ball and there are less than four players, add one.
        if self.game.ball == 1 and len(self.game.players) < 4:
            self.game.add_player()
            # and play a soundbyte
            if len(self.game.players) == 2:
                self.game.sound.play(self.game.assets.quote_playerTwo)
            elif len(self.game.players) == 3:
                self.game.sound.play(self.game.assets.quote_playerThree)
            elif len(self.game.players) == 4:
                self.game.sound.play(self.game.assets.quote_playerFour)
        ## -- set the last switch hit --
        ep.last_switch = "startButton"

    def sw_shooterLane_open_for_1s(self,sw):
        if not self.game.autoPlunge:
            if self.game.ballStarting:
                self.game.ballStarting = False
                ball_save_time = 10
                self.game.ball_save.start(num_balls_to_save=1, time=ball_save_time, now=True, allow_multiple_saves=False)
            else:
                self.game.ball_save.disable()

    def sw_beerMug_active(self,sw):
        # track it, because why not
        hits = self.game.increase_tracking('beerMugHits')
        self.game.increase_tracking('beerMugHitsTotal')
        # score points
        self.game.score(2130)
        # play a sound
        self.game.sound.play(self.game.assets.sfx_ricochetSet)
        # a little display action
        textLine1 = dmd.TextLayer(51, 1, self.game.assets.font_9px_az, "center", opaque=False).set_text("BEER MUG")
        # TODO right now it takes 15 shots to light drunk multiball - change this to a config param
        left = self.mug_shots - hits
        ## if we're at zero, it's lit and the display shows it
        if left == 0:
            self.light_drunk_multiball()
        ## if we're past zero then it shows a message
        elif left < 0:
            textString = "SHOOT THE SALOON"
            textString2 = "FOR MULTIBALL"
            textLine2 = dmd.TextLayer(51, 12, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString,blink_frames=8)
            textLine3 = dmd.TextLayer(51, 21, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString2)
            self.mug_display(textLine1,textLine2,textLine3)

        ## if we're still not there yet, show how much is left
        else:
            if left == 1:
                textString = "1 MORE HIT FOR"
            else:
                textString = str(left) + " MORE HITS FOR"
            textString2 = "DRUNKEN MULTIBALL"
            textLine2 = dmd.TextLayer(51, 12, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString)
            textLine3 = dmd.TextLayer(51, 21, self.game.assets.font_7px_az, "center", opaque=False).set_text(textString2)
            self.mug_display(textLine1,textLine2,textLine3)

        if left != 0:
            # play a quote on a random 1/3 choice
            weDo = random.choice([False,True,False])
            if weDo:
                self.game.sound.play(self.game.assets.quote_beerMug)
        ## -- set the last switch -- ##
        ep.last_switch = 'beerMug'
        ## kill the combo shot chain
        ep.last_shot = None


    def mug_display(self,textLine1,textLine2,textLine3):
        backdrop = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'beer-mug-1.dmd').frames[0])
        combined = dmd.GroupedLayer(128,32,[backdrop,textLine1,textLine2,textLine3])
        # kill any previous display
        self.cancel_delayed("Display")
        # turn on the layer
        self.layer = combined
        # set a delay to clear
        self.delay(name="Display", delay = 1.6, handler=self.clear_layer)

    def light_drunk_multiball(self,callback = None):
        # set the hits to the same number it takes to light - this is a catch for the super skillshot award
        self.game.set_tracking('beerMugHits',self.mug_shots)
        # enable the multiball
        self.game.set_tracking('drunkMultiballStatus', "READY")
        self.game.saloon.update_lamps()
        textLine1 = ep.pulse_text(self,51,1,"DRUNK")
        textLine2 = ep.pulse_text(self,51,12,"MULTIBALL")
        textLine3 = dmd.TextLayer(51, 23, self.game.assets.font_6px_az, "center", opaque=False).set_text("IS LIT")
        self.repeat_ding(4)
        self.game.sound.play(self.game.assets.quote_drunkMultiballLit)
        self.mug_display(textLine1,textLine2,textLine3)
        # so super can start gameplay
        if callback:
            self.delay(delay=1.7,handler=callback)
        self.delay(delay=1.7,handler=self.clear_layer)

    # Allow service mode to be entered during a game.
    def sw_enter_active(self, sw):
        self.game.modes.add(self.game.service_mode)
        return True

    def music_on(self,song=None):
            # if a song is passed, set that to the active song
            # if not, just re-activate the current
            if song:
                self.current_music = song
            self.game.sound.play_music(self.current_music, loops=-1)

    def delayed_music_on(self,wait,song=None):
        self.delay(delay=wait, handler=self.music_on,param=song)

    def repeat_ding(self,times):
        self.game.sound.play(self.game.assets.sfx_bountyBell)
        self.game.coils.saloonFlasher.pulse(ep.FLASHER_PULSE)
        times -= 1
        if times > 0:
            self.delay(delay=0.4,handler=self.repeat_ding,param=times)

    ###
    ###  _____ _ _ _
    ### |_   _(_) | |_
    ###   | | | | | __|
    ###   | | | | | |_
    ###   |_| |_|_|\__|
    ###

    def sw_plumbBobTilt_active(self, sw):
        # first, register the hit
        status = self.game.increase_tracking('tiltStatus')
        # if that puts us at three, time to tilt
        if status == 3:
            self.tilt()
        # for 2 or 1 hand off to interrupter jones
        else:
            self.game.interrupter.tilt_danger(status)

    def tilt(self):
        # Process tilt.
        # First check to make sure tilt hasn't already been processed once.
        # No need to do this stuff again if for some reason tilt already occurred.
        if self.game.show_tracking('tiltStatus') == 3:

            self.game.interrupter.tilt_display()
            # Disable flippers so the ball will drain.
            self.game.enable_flippers(enable=False)

            # Make sure ball won't be saved when it drains.
            self.game.ball_save.disable()

            # Make sure the ball search won't run while ball is draining.
            self.game.ball_search.disable()

            # Ensure all lamps are off.
            for lamp in self.game.lamps:
                lamp.disable()

            # Kick balls out of places it could be stuck.
            if self.game.switches.minePopper.is_active():
                self.game.coils.minePopper.pulse(30)
            if self.game.switches.saloonPopper.is_active():
                self.game.coils.saloonPopper.pulse(30)
        #play sound
        #play video

    ###
    ###  ___       _
    ### |_ _|_ __ | | __ _ _ __   ___  ___
    ###  | || '_ \| |/ _` | '_ \ / _ \/ __|
    ###  | || | | | | (_| | | | |  __/\__\
    ### |___|_| |_|_|\__,_|_| |_|\___||___/
    ###
    ###

    def sw_leftReturnLane_active(self, sw):
        # register a left return lane hit
        self.return_lane_hit(0)
        ## -- set the last switch hit --
        ep.last_switch = "leftReturnLane"


    def sw_rightReturnLane_active(self,sw):
        # register a right return lane hit
        self.return_lane_hit(1)
        ## -- set the last switch hit --
        ep.last_switch = "rightReturnLane"

    def return_lane_hit(self,side):
        # play the sound
        self.game.sound.play(self.game.assets.sfx_rattlesnake)
        # score the points
        self.game.score_with_bonus(2530)
        # if there's a running quickdraw or showdown - pass
        if not self.guns_allowed():
            print "PASSING - Guns disabled"
            print self.game.show_tracking('stackLevel')
        # move your train
        elif self.game.show_tracking('mytStatus') == "READY":
            # if MYT is ready, start it and raise the post to catch the ball
            self.game.move_your_train.start(True,side)
        # if guns are allowed, and showdown is ready do that
        elif self.game.show_tracking('showdownStatus') == "READY":
            self.game.modes.add(self.game.showdown)
            self.game.showdown.start_showdown(side)
        # if guns are allowed and ambush is ready, do that
        elif self.game.show_tracking('ambushStatus') == "READY":
            self.game.modes.add(self.game.ambush)
            self.game.ambush.start_ambush(side)
        # if there's no showdown ready, gunfight is possible
        elif self.game.show_tracking('gunfightStatus') == "READY":
            self.game.modes.add(self.game.gunfight)
            self.game.gunfight.start_gunfight(side)
        # else if quickdraw is lit - run that passing which side started it
        elif self.game.show_tracking('quickdrawStatus',side) == "READY":
            # fire the startup
            self.game.modes.add(self.game.quickdraw)
            self.game.quickdraw.start_quickdraw(side)
        else:
            pass

    def guns_allowed(self):
        # this is for turning the guns back on if the conditions are good
        if True in self.game.show_tracking('stackLevel'):
        # if any stack level is active, new gunfight action is not allowed
            return False
        else:
            return True


    ###
    ###   ___        _   _
    ###  / _ \ _   _| |_| | __ _ _ __   ___  ___
    ### | | | | | | | __| |/ _` | '_ \ / _ \/ __|
    ### | |_| | |_| | |_| | (_| | | | |  __/\__\
    ###  \___/ \__,_|\__|_|\__,_|_| |_|\___||___/
    ###

    def sw_leftOutlane_active(self,sw):
        self.outlane_hit(0)
        ## -- set the last switch hit --
        ep.last_switch = "leftOutlane"


    def sw_rightOutlane_active(self,sw):
        self.outlane_hit(1)
        ## -- set the last switch hit --
        ep.last_switch = "rightOutlane"


    def outlane_hit(self, side):
        self.game.score_with_bonus(2530)
        self.game.sound.play(self.game.assets.sfx_outlane)

    ###
    ###  ____  _ _                 _           _
    ### / ___|| (_)_ __   __ _ ___| |__   ___ | |_ ___
    ### \___ \| | | '_ \ / _` / __| '_ \ / _ \| __/ __|
    ###  ___) | | | | | | (_| \__ \ | | | (_) | |_\__\
    ### |____/|_|_|_| |_|\__, |___/_| |_|\___/ \__|___/
    ###                  |___/
    ###

    def sw_leftSlingshot_active(self,sw):
        self.slingshot_hit(0)
        ## -- set the last switch hit --
        ep.last_switch = "leftSlingshot"


    def sw_rightSlingshot_active(self,sw):
        self.slingshot_hit(1)
        ## -- set the last switch hit --
        ep.last_switch = "rightSlingshot"


    def slingshot_hit(self,side):
        # play a sound
        self.game.sound.play(self.game.assets.sfx_ricochetSet)
        # blink a flasher
        if side == 0:
            self.delay(delay=0.03,handler=self.game.coils.leftGunFlasher.pulse)
        else:
            self.delay(delay=0.03,handler=self.game.coils.rightGunFlasher.pulse)
        # score points
        self.game.score(3770)

    ###  ____
    ### | __ ) _   _ _ __ ___  _ __   ___ _ __ ___
    ### |  _ \| | | | '_ ` _ \| '_ \ / _ \ '__/ __|
    ### | |_) | |_| | | | | | | |_) |  __/ |  \__\
    ### |____/ \__,_|_| |_| |_| .__/ \___|_|  |___/
    ###                       |_|

    def sw_leftJetBumper_active(self,sw):
        self.bumper_hit('left')

    def sw_rightJetBumper_active(self,sw):
        self.bumper_hit('right')

    def sw_bottomJetBumper_active(self,sw):
        self.bumper_hit('bottom')

    def bumper_hit(self,bumper):
        # if combos are on, award grace
        if self.game.combos.myTimer > 0:
            self.game.combos.myTimer = self.game.combos.default
        hits = self.game.increase_tracking('bumperHits')
        # flash the back left flasher per hit
        self.game.coils.backLeftFlasher.pulse(30)
        if hits == 75:
            # display the super jets display
            pass
        elif hits == 150:
            # display the mega jets display
            pass
        if hits < 75:
            # if we're under 75 points are low
            self.game.score(5250)
            # and the sound is a punch
            self.game.sound.play(self.game.assets.sfx_punch)
            self.display_bumper(hits,"SUPER")
        elif hits >= 75 and hits < 150:
            # if we're in super jets the score is more
            self.game.score(50000)
            # and the sound is an explosion
            self.game.sound.play(self.game.assets.sfx_smallExplosion)
            self.display_bumper(hits,"MEGA")
        elif hits >= 150:
            # mega jets
            self.game.score(500000)
            # and the sound is the futuristic ricochet
            self.game.sound.play(self.game.assets.sfx_futuristicRicochet)

    ## TODO add the displays for shots to increase level and the various active levels
    def display_bumper(self,hits,nextup):
        if nextup == "SUPER":
            textString1 = "< " + str(75 - hits) + " MORE HITS >"
            textString2 = "< FOR SUPER JETS >"
        elif nextup == "MEGA":
            textString1 = "<" + str(150 - hits) + " MORE HITS >"
            textString2 = "< FOR  MEGA  JETS >"
        textLayer1 = dmd.TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString1)
        textLayer2 = dmd.TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString2)
        textLayer1.composite_op = "blacksrc"
        textLayer2.compoaite_op = "blacksrc"
        self.cancel_delayed("Display")
        self.layer = textLayer1
        self.delay(name="Display",delay=.5,handler=self.change_layer,param=textLayer2)
        self.delay(name="Display",delay=1,handler=self.clear_layer)

    def change_layer(self,myLayer):
        self.layer = myLayer

    ###
    ###  _____ _ _
    ### |  ___| (_)_ __  _ __   ___ _ __ ___
    ### | |_  | | | '_ \| '_ \ / _ \ '__/ __|
    ### |  _| | | | |_) | |_) |  __/ |  \__\
    ### |_|   |_|_| .__/| .__/ \___|_|  |___/
    ###           |_|   |_|
    ###

    ## Flipper switch detection for flipping the bonus lanes
    def sw_flipperLwL_active(self,sw):
        # toggle the bonus lane
        self.game.bonus_lanes.flip()

    def sw_flipperLwR_active(self,sw):
        # toggle the bonus lane
        self.game.bonus_lanes.flip()

    ### shooter lane stuff

    def sw_shooterLane_active_for_300ms(self,sw):
        # if we're dealing with a saved ball, plunge like the wind
        print "checking ball saved"
        if self.game.autoPlunge == True:
            print "AUTOPLUNGE, MF"
            self.game.coils.autoPlunger.pulse(40)


    def sw_shooterLane_inactive_for_100ms(self,sw):
        # play the ball lanuch noise
        self.game.sound.play(self.game.assets.sfx_shooterLaunch)
        # kill the player number display if active
        self.game.interrupter.abort_player_number()

    def sw_shooterLane_active_for_5s(self,sw):
        # if the ball sits in the shooter lane, flash the player number
        self.game.interrupter.display_player_number(idle=True)

    def sw_skillBowl_active(self,sw):
        if self.game.autoPlunge:
            self.cancel_delayed("Stop Autoplunge")
            # delay cancelling auto punge for 3 seconds in case more balls are coming
            self.delay(name="Stop Autoplunge",delay=3,handler=self.disable_auto_plunge)

    def disable_auto_plunge(self):
        print "TURNING OFF AUTOPLUNGE"
        self.game.autoPlunge = False

    ### stampede
    def check_stampede(self):
        # if both loops are done and the save polly is finished, then it's time to stampede
        if self.game.show_tracking('leftLoopStage') == 4 and \
            self.game.show_tracking('rightLoopStage') == 4 and \
            self.game.show_tracking('centerRampStage') == 5 and \
            self.game.show_tracking('leftRampStage') == 4 and \
            self.game.show_tracking('rightRampStage') == 4:

            self.game.modes.add(self.game.stampede)
            self.game.stampede.start_stampede()
        else:
            pass

    ###
    ###   ___        _      _       _
    ###  / _ \ _   _(_) ___| | ____| |_ __ __ ___      _____
    ### | | | | | | | |/ __| |/ / _` | '__/ _` \ \ /\ / / __|
    ### | |_| | |_| | | (__|   < (_| | | | (_| |\ V  V /\__\
    ###  \__\_\\__,_|_|\___|_|\_\__,_|_|  \__,_| \_/\_/ |___/
    ###
    ### The handling of the Quickdraw targets and lights is here
    ### the actual game mode loads and unloads as needed to set it
    ### at a higher priority so it can take over the DMD -- maybe

    def sw_topLeftStandUp_active(self, sw):
        self.quickdraw_hit('TOP',0)
        ## -- set the last switch hit --
        ep.last_switch = "topLeftStandup"
        ## kill the combo shot chain
        ep.last_shot = None

    def sw_bottomLeftStandUp_active(self,sw):
        self.quickdraw_hit('BOT',0)
        ## -- set the last switch hit --
        ep.last_switch = "bottomLeftStandup"
        ## kill the combo shot chain
        ep.last_shot = None

    def sw_topRightStandUp_active(self, sw):
        self.quickdraw_hit('TOP',1)
        ## -- set the last switch hit --
        ep.last_switch = "topRightStandup"
        ## kill the combo shot chain
        ep.last_shot = None

    def sw_bottomRightStandUp_active(self,sw):
        self.quickdraw_hit('BOT',1)
        ## -- set the last switch hit --
        ep.last_switch = "bottomRightStandup"
        ## kill the combo shot chain
        ep.last_shot = None


    def quickdraw_hit(self, position,side):
        # lookup the status of the side, and difficulty
        stat = self.game.show_tracking('quickdrawStatus',side)
        difficulty = self.game.user_settings['Gameplay (Feature)']['Multiball Locks Difficulty']
        # if quickdraw is running or lit on the side hit, or position matches stat, or bionic bart is running
        if "RUNNING" in self.game.show_tracking('quickdrawStatus') or \
          stat == "READY" or  \
          stat == position or \
          self.game.show_tracking('bionicStatus') == "RUNNING":
            print "QUICKDRAW IS RUNNING OR LIT"
            # register a lit hit
            self.quickdraw_lit_hit()
        # otherwise quickdraw is NOT running or LIT
        else:
            # register an unlit hit
            self.quickdraw_unlit_hit(position,side,stat,difficulty)

    def quickdraw_lit_hit(self):
        #play the alt sound
        self.game.sound.play(self.game.assets.sfx_quickdrawOn)
        # award some points
        self.game.score(10000)

    def quickdraw_unlit_hit(self,position,side,stat,difficulty):
        # play the sound
        self.game.sound.play(self.game.assets.sfx_quickdrawOff)
        # award the points -- dividing the normal 22500 for lighting quickdraw into 2 parts to acccount for "Hard" difficulty
        self.game.score(10000)
        # if the status is already BOT/TOP or the difficulty is easy
        if stat == "BOT" or stat == "TOP" or  difficulty == "Easy":
            # light quickdraw
            self.light_quickdraw(side)
        # else set the status to the hit target sending the position for the amount and side for the key
        else:
            # will also need to do something with lights here
            self.game.set_tracking('quickdrawStatus',position,side)
            self.update_lamps()

    def light_quickdraw(self,side=9):
        # this is for handling a call to light quickdraw with no side favor the right
        if side == 9:
            target = self.game.show_tracking('quickdrawStatus')
            if target[1] == "READY":
                side = 0
            else:
                side = 1
        # add the rest of the points for lighting the quickdraw
        self.game.score(12500)
        # turn on the quickdraw light
        # play a quote from the stack
        self.game.sound.play_voice(self.game.assets.quote_quickdrawLit)
        # set the status for the hit side to READY
        self.game.set_tracking('quickdrawStatus',"READY",side)
        self.update_lamps()

    ###
    ###  ____
    ### | __ )  ___  _ __  _   _ ___
    ### |  _ \ / _ \| '_ \| | | / __|
    ### | |_) | (_) | | | | |_| \__\
    ### |____/ \___/|_| |_|\__,_|___/
    ###

    def check_bonus(self):
        # we have to wait until other things finish
        self.wait_until_unbusy(self.do_bonus)

    def do_bonus(self):
        # get the bonus multiplier
        times = self.game.show_tracking('bonusX')
        print "BONUS TIMES: " + str(times)
        # then reset it for next time
        self.game.set_tracking('bonusX',1)
        # then loop through the display
        # get the bonus points
        self.bonus = self.game.show_tracking('bonus')
        # and reset it
        self.game.set_tracking('bonus',0)
        # and clear the running total
        self.runningTotal = 0
        # throw up a  layer that says bonus as an interstitial
        textLine = dmd.TextLayer(64, 5, self.game.assets.font_20px_az, "center", opaque=False).set_text("BONUS")
        self.layer = textLine
        # then 1.5 seconds later, move on
        self.delay(delay=1.5,handler=self.display_bonus,param=times)

    def display_bonus(self,times):
        background = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(ep.DMD_PATH+'cactus-border.dmd').frames[0])
        titleString = "BONUS " + str(times) + "X"
        titleLine = dmd.TextLayer(128/2, 2, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text(titleString)
        # add the bonus amount to the running total
        self.runningTotal += self.bonus
        pointsLine = dmd.TextLayer(128/2, 16, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text(ep.format_score(self.runningTotal))
        # turn the layer on
        self.layer = dmd.GroupedLayer(128,32,[background,titleLine,pointsLine])
        # play a sound
        self.game.sound.play(self.game.assets.sfx_bonusX)
        # tick down the counter of times
        times -= 1
        if times <= 0:
            # if we're at the last one, it's time to finish up
            self.delay(delay=1.5,handler=self.reveal_bonus,param=self.runningTotal)
        else:
            # if not, loop back around after a delay
            self.delay(delay=0.5,handler=self.display_bonus,param=times)

    def reveal_bonus(self,points):
        # load up the animation
        anim = dmd.Animation().load(ep.DMD_PATH+'burst-wipe.dmd')
        myWait = len(anim.frames) / 15.0
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold = True
        animLayer.frame_time = 4
        self.layer = animLayer
        self.delay(delay=myWait,handler=self.finish_bonus,param=points)

    def finish_bonus(self,points):
        # set up the text display
        anim = dmd.Animation().load(ep.DMD_PATH+'burst-wipe-2.dmd')
        myWait = len(anim.frames) / 15.0 + 1.5
        animLayer = ep.EP_AnimatedLayer(anim)
        animLayer.hold = True
        animLayer.frame_time = 4
        animLayer.composite_op = "blacksrc"

        titleString = "TOTAL BONUS:"
        titleLine = dmd.TextLayer(128/2, 2, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text(titleString)
        pointsLine = dmd.TextLayer(128/2, 16, self.game.assets.font_12px_az_outline, "center", opaque=False).set_text(ep.format_score(points))
        self.layer = dmd.GroupedLayer(128,32,[titleLine,pointsLine,animLayer])
        # add the points to the score
        self.game.score(points)
        # play a final sound
        self.game.sound.play(self.game.assets.sfx_flourish6)
        # then loop back to end ball
        self.delay(delay=2,handler=self.game.ball_ended)
        self.delay(delay=2,handler=self.clear_layer)


    # red flasher flourish thing
    ## a flasher flourish
    def red_flasher_flourish(self,foo='bar'):
        self.flash(self.game.coils.middleRightFlasher)
        self.delay(delay=0.03,handler=self.flash,param=self.game.coils.backRightFlasher)
        self.delay(delay=0.06,handler=self.flash,param=self.game.coils.backLeftFlasher)
        self.delay(delay=0.09,handler=self.flash,param=self.game.coils.middleRightFlasher)
        self.delay(delay=0.12,handler=self.flash,param=self.game.coils.backRightFlasher)
        self.delay(delay=0.15,handler=self.flash,param=self.game.coils.backLeftFlasher)

    def flash(self,bulb):
        bulb.pulse(30)