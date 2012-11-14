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
## A P-ROC Project by Eric Priepke, Copyright 2012
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
## Original Cactus Canyon software by Matt Coriale
##
###
###
### Save Poor Polly from getting run over by the train!
###

from procgame import dmd
import random
import ep

class BankRobbery(ep.EP_Mode):
    """Polly Peril - Hostage at the bank"""
    def __init__(self,game,priority):
        super(BankRobbery, self).__init__(game,priority)
        self.running = False
        self.halted = False
        self.position = [-49,-4,43]
        self.y_pos = 7
        self.isActive = [True,True,True]
        self.shots = [self.game.left_ramp,self.game.center_ramp,self.game.right_ramp]
        self.won = False
        self.flashers = [self.game.coils.backLeftFlasher,self.game.coils.backRightFlasher,self.game.coils.middleRightFlasher]

        script = []
        # set up the text layer
        textString = "< SAVE POLLY PAUSED >"
        textLayer = dmd.TextLayer(128/2, 24, self.game.assets.font_6px_az_inverse, "center", opaque=False).set_text(textString)
        script.append({'seconds':0.3,'layer':textLayer})
        # set up the alternating blank layer
        blank = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_blank.frames[0])
        blank.composite_op = "blacksrc"
        script.append({'seconds':0.3,'layer':blank})
        # make a script layer with the two
        self.pauseView = dmd.ScriptedLayer(128,32,script)
        self.pauseView.composite_op = "blacksrc"


    def mode_started(self):
        # fire up the switch block if it's not already loaded
        self.game.switch_blocker('add')

        self.game.peril = True
        # point value for shots
        self.shotValue = 250000
        self.isActive = [True,True,True]
        self.won = False
        self.have_won = False
        self.banner = False
        # stuff for the random shootering
        self.shotTimer = 0
        self.shotTarget = 0
        self.shooting = False
        self.shooter = 0
        self.shotWait = 0

        # set up the dude standing layers
        self.dude0 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_bankDude.frames[0])
        self.dude0.set_target_position(self.position[0],self.y_pos)
        self.dude0.composite_op = "blacksrc"
        self.dude1 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_bankDude.frames[0])
        self.dude1.set_target_position(self.position[1],self.y_pos)
        self.dude1.composite_op = "blacksrc"
        self.dude2 = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_bankDude.frames[0])
        self.dude2.set_target_position(self.position[2],self.y_pos)
        self.dude2.composite_op = "blacksrc"

        # set the dude layers to the starting layer
        self.dude0Layer = self.dude0
        self.dude1Layer = self.dude1
        self.dude2Layer = self.dude2
        self.layers = [self.dude0Layer,self.dude1Layer,self.dude2Layer]

        # load the shot animation
        self.shotAnim = self.game.assets.dmd_dudeShotFullBody
        # create the layer
        self.deathWait = len(self.shotAnim.frames) / 10.0
        # set the timer
        self.modeTimer = self.game.user_settings['Gameplay (Feature)']['Save Polly Timer - Bank']
        self.modeTimer += 1

        # foreground
        self.foreground = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_bankInterior.frames[0])
        self.foreground.composite_op = "blacksrc"



    def ball_drained(self):
        print "Bank robbery thinks the ball drained"
        if self.game.trough.num_balls_in_play == 0:
            if self.running:
                self.game.base.busy = True
                self.game.base.queued += 1
                self.polly_died()

    # bonus lanes pause save polly
    def sw_leftBonusLane_active(self,sw):
        if not self.halted:
            self.halt()

    def sw_rightBonusLane_active(self,sw):
        if not self.halted:
            self.halt()

    # bumpers pause quickdraw
    def sw_leftJetBumper_active(self,sw):
        if not self.halted:
            self.halt()

    def sw_rightJetBumper_active(self,sw):
        if not self.halted:
            self.halt()

    def sw_bottomJetBumper_active(self,sw):
        if not self.halted:
            self.halt()

    # so does the mine and both pass the 'advanced' flag to avoid moo sounds
    def sw_minePopper_active_for_390ms(self,sw):
        if not self.halted:
            self.halt()

    def sw_saloonPopper_active_for_290ms(self,sw):
        if not self.halted:
            self.halt()

    def sw_saloonPopper_inactive(self,sw):
        if self.running and self.halted:
            self.halted = False
            self.in_progress()

    # resume when exit
    def sw_jetBumpersExit_active(self,sw):
        if self.running and self.halted:
            # kill the halt flag
            self.halted = False
            self.in_progress()

    def sw_centerRampMake_active(self,sw):
        if self.running:
            self.process_shot(1)

    def sw_leftRampEnter_active(self,sw):
        if self.running:
            self.process_shot(0)

    def sw_rightRampMake_active(self,sw):
        if self.running:
            self.process_shot(2)

    def process_shot(self,shot):
        # kill the mode timer for good measure
        self.cancel_delayed("Mode Timer")
        # combos
        if self.game.combos.myTimer > 0:
        # register the combo and reset the timer - returns true for use later
            combo = self.game.combos.hit()
        else:
            # and turn on the combo timer - returns false for use later
            combo = self.game.combos.start()

        if self.isActive[shot]:
            # if we hit an active shot, it's a hit
            # set that shot to inactive
            self.isActive[shot] = False
            # update the lamps
            self.lamp_update()
            # score points
            self.game.score(self.shotValue)
            # kill the guy
            self.kill_dude(shot)
        else:
            self.game.score(2370)
            self.game.sound.play(self.game.assets.sfx_thrownCoins)
            # if we did't hit a shot, restart the mode timer
            self.in_progress()

    def start_bank_robbery(self,step=1):
        if step == 1:
            # set the level 1 stack flag
            self.game.stack_level(2,True)

            # set the running flag
            self.running = True
            # clear any running music
            print "start_bank_robbery IS KILLING THE MUSIC"
            self.game.sound.stop_music()
            self.lamp_update()

            # start the music
            self.game.base.music_on(self.game.assets.music_pollyPeril)
            # run the animation
            anim = self.game.assets.dmd_pollyIntro
            myWait = len(anim.frames) / 30
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=True,repeat=False,frame_time=2)
            self.layer = animLayer

            # loop back for the title card
            self.delay(delay=myWait,handler=self.start_bank_robbery,param=2)
        if step == 2:
            # pick a shoot delay
            self.set_shot_target()
            # set up the title card
            titleCard = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_hatbTitle.frames[0])
            # transition to the title card
            self.transition = ep.EP_Transition(self,self.layer,titleCard,ep.EP_Transition.TYPE_WIPE,ep.EP_Transition.PARAM_EAST)
            # delay the start process
            self.delay("Get Going",delay=2,handler=self.in_progress)
            self.delay(delay=2,handler=self.game.base.play_quote,param=self.game.assets.quote_hatbIntro)

    ## this is the main mode loop - not passing the time to the loop because it's global
    ## due to going in and out of pause
    def in_progress(self):
        if self.running:
            #print "IN PROGRESS " + str(self.modeTimer)
            #print "Shooter info: Target - " + str(self.shotTarget) + " Timer - " + str(self.shotTimer)
            # and all the text
            p = self.game.current_player()
            scoreString = ep.format_score(p.score)
            scoreLine = dmd.TextLayer(34, 6, self.game.assets.font_5px_bold_AZ, "center", opaque=False).set_text(scoreString,blink_frames=8)
            timeString = str(int(self.modeTimer))
            self.timeLine = dmd.TextLayer(128,26, self.game.assets.font_5px_AZ, "right", opaque=False).set_text(timeString)

            # stick together the animation and static text with the dynamic text
            composite = dmd.GroupedLayer(128,32,[self.dude0Layer,self.dude1Layer,self.dude2Layer,self.foreground,self.timeLine])
            self.layer = composite

            # increment the shot timer
            self.shotTimer += 1
            # check if time to shoot
            if self.shotTimer == self.shotTarget:
                # if it is that time, generate a firing guy
                self.dude_shoots()

            # did we just kill the last guy?
            if self.have_won:
                self.have_won = False
                # delay for the dude getting shot animation to finish
                self.delay(delay=self.deathWait,handler=self.polly_saved)
            # how about any guy?
            if self.banner:
                self.banner = False
                # if we need to show a dude killed banner, do that
                self.delay(delay=self.deathWait,handler=self.banner_display)
            # is a guy shooting?
            if self.shooting:
                self.shooting = False
                # set a delay to put the plain guy back after
                self.delay(delay=self.shotWait,handler=self.end_shot_sequence)
            # both of those bail before ticking down the timer and looping back

            ## tick down the timer
            self.modeTimer -= 0.1
            ## hurry quote at 5 seconds, plead at 15
            if abs(self.modeTimer - 15) < 0.00000001:
                self.game.base.play_quote(self.game.assets.quote_pollyPlead)
            if abs(self.modeTimer - 5) < 0.00000001:
                self.game.base.play_quote(self.game.assets.quote_pollyHurry)
            if self.modeTimer <= 0:
                # go to a grace period
                self.polly_died()
            # otherwise ...
            else:
                # set up a delay to come back in 1 second with the lowered time
                self.delay(name="Mode Timer",delay=0.1,handler=self.in_progress)

    def kill_dude(self,shot):
        # if the guy died was about to shot, that should be stopped
        if shot == self.shooter and self.shooting:
            # turn the flag off
            self.shooting = False
            # and get a new time/guy
            self.set_shot_target()

        # killing the get going delay just in case a guy is shot before we're started
        if self.modeTimer > 29:
            self.cancel_delayed("Get Going")
        print "KILLING DUDE " + str(shot)
        animLayer = dmd.AnimatedLayer(frames=self.shotAnim.frames,hold=True,opaque=False,repeat=False,frame_time=6)
        animLayer.composite_op = "blacksrc"
        # set the target position based on the shot
        animLayer.set_target_position(self.position[shot],self.y_pos)
        # set the layer
        if shot == 0:
            self.dude0Layer = animLayer
        elif shot == 1:
            self.dude1Layer = animLayer
        elif shot == 2:
            self.dude2Layer = animLayer
        else:
            # WAT?
            pass
        # play a shot sound
        self.game.sound.play(self.game.assets.sfx_gunfightShot)
        # set a won flag if they're all dead
        if True not in self.isActive:
            self.have_won = True
            self.won = True
        else:
            self.banner = True
        # then go to in_progress to restart the timer
        self.in_progress()

    def halt(self):
        # if guys are still alive, halt
        if True in self.isActive:
            print "HALTING -- BUMPERS/MINE/SALOON"
            # cancel delays
            self.cancel_delayed("Mode Timer")
            # this is the initial delay - have to include it in case of a straight shot to the mine off the ramp
            self.cancel_delayed("Get Going")
            # set the flag
            self.halted = True
            self.layer = self.pauseView


    # success
    def polly_saved(self):
        self.game.score(750000)
        self.cancel_delayed("Mode Timer")
        stackLevel = self.game.show_tracking('stackLevel')
        if True not in stackLevel[3:] and self.game.trough.num_balls_in_play != 0:
            self.game.sound.stop_music()
        # kill the lights on the three ramps
        self.game.lamp_control.left_ramp('Base')
        self.game.lamp_control.center_ramp('Base')
        self.game.lamp_control.right_ramp('Base')
        self.win_display()

    # fail
    def polly_died(self):
        self.cancel_delayed("Mode Timer")
        backdrop = dmd.FrameLayer(opaque=True, frame=self.game.assets.dmd_poutySheriff.frames[0])
        textLine1 = dmd.TextLayer(25,8,self.game.assets.font_12px_az,justify="center",opaque=False).set_text("TOO")
        textLine2 = dmd.TextLayer(98,8,self.game.assets.font_12px_az,justify="center",opaque=False).set_text("LATE!")
        combined = dmd.GroupedLayer(128,32,[backdrop,textLine1,textLine2])
        self.layer = combined
        self.game.sound.play(self.game.assets.sfx_glumRiff)

        self.delay("Operational",delay=1.5,handler=self.end_bank_robbery)

    def win_display(self,step=1):
        if step == 1:
            self.game.base.play_quote(self.game.assets.quote_victory)
            # frame layer of the dead guy
            self.layer = dmd.FrameLayer(opaque=False, frame=self.game.assets.dmd_ourHero.frames[0])
            self.delay("Display",delay=0.5,handler=self.win_display,param=2)
        if step == 2:
            # the pan up
            anim = self.game.assets.dmd_ourHero
            # math out the wait
            myWait = len(anim.frames) / 60.0
            # set the animation
            animLayer = dmd.AnimatedLayer(frames=anim.frames,hold=True,opaque=False,repeat=False,frame_time=1)
            # turn it on
            self.layer = animLayer
            # loop back for the finish animation
            self.delay("Display",delay=myWait,handler=self.win_display,param=3)
        if step == 3:
            anim = self.game.assets.dmd_pollyVictory
            myWait = len(anim.frames) / 8.57
            animLayer = ep.EP_AnimatedLayer(anim)
            animLayer.hold=True
            animLayer.frame_time = 7

            animLayer.add_frame_listener(7,self.game.sound.play,param=self.game.assets.sfx_blow)
            animLayer.add_frame_listener(14,self.game.sound.play,param=self.game.assets.sfx_grinDing)
            # play animation
            self.layer = animLayer
            self.delay("Display",delay=myWait,handler=self.win_display,param=4)
        if step == 4:
            # saved banner goes here
            awardTextString = "POLLY SAVED"
            awardScoreString = "750,000"
            # combine them
            completeFrame = self.build_display(awardTextString,awardScoreString)
            stackLevel = self.game.show_tracking('stackLevel')
            # if something higher is running, throw the win display in a cut in
            if True in stackLevel[3:]:
                self.game.interrupter.cut_in(completeFrame,1)
            else:
                self.layer = completeFrame
            self.delay(name="Operational",delay=2,handler=self.end_bank_robbery)
            # show combo display if the chain is high enough
            if self.game.combos.chain > 1:
                self.delay(name="Display",delay=2,handler=self.game.combos.display)

    def banner_display(self):
        # halt the mode timer for a second
        self.cancel_delayed("Mode Timer")
        # turn the banner off
        self.banner = False
        total = 0
        # count up the remaining shots
        for shot in self.isActive:
            if shot:
                total += 1
        # build a text line with that
        awardTextString = str(total) + " MORE TO GO"
        # build the display layer
        banner = self.build_display(awardTextString,"250,000")
        # activate it
        self.layer = banner
        # delay a return to in progress
        self.delay(delay=1.5,handler=self.in_progress)

    def build_display(self,awardTextString,awardScoreString):
        # create the two text lines
        awardTextTop = dmd.TextLayer(128/2,3,self.game.assets.font_5px_bold_AZ_outline,justify="center",opaque=False)
        awardTextBottom = dmd.TextLayer(128/2,11,self.game.assets.font_15px_az_outline,justify="center",opaque=False)
        awardTextBottom.composite_op = "blacksrc"
        awardTextTop.composite_op = "blacksrc"
        awardTextTop.set_text(awardTextString)
        awardTextBottom.set_text(awardScoreString)
        # combine them
        if self.layer == None:
            self.layer = self.no_layer()
        completeFrame = dmd.GroupedLayer(128, 32, [self.layer,awardTextTop,awardTextBottom])
        # swap in the new layer
        return completeFrame

    def end_bank_robbery(self):
        self.running = False
        # stop the polly music
        print "end_bank_robbery IS KILLING THE MUSIC"
        # only kill the music if there's not a higher level running
        stackLevel = self.game.show_tracking('stackLevel')
        if True not in stackLevel[3:] and self.game.trough.num_balls_in_play != 0:
            self.game.sound.stop_music()
        self.layer = None
        # set the tracking on the ramps
        self.game.set_tracking('rightRampStage',5)
        self.lamp_update()
        self.end_save_polly()

    # clean up and exit
    def end_save_polly(self):
        print "ENDING SAVE POLLY"
        # turn the level 1 stack flag back off
        self.game.stack_level(2,False)
        # check to see if stampede is ready - if we're not ending due to ball fail
        if self.game.trough.num_balls_in_play != 0:
            self.game.base.check_stampede()
            # unset the busy flag
        self.game.base.busy = False
        self.game.base.queued -= 1
        # turn the music back on
        stackLevel = self.game.show_tracking('stackLevel')
        if True not in stackLevel[3:] and self.game.trough.num_balls_in_play != 0:
            self.game.base.music_on(self.game.assets.music_mainTheme)
        self.game.peril = False
        # remove the switch blocker
        self.game.switch_blocker('remove')
        # unload the mode
        self.unload()

    def set_shot_target(self):
        # pick a random target time
        self.shotTarget = random.randrange(35, 50, 1)
        # reset the counter
        self.shotTimer = 0

    def dude_shoots(self):
        # bail if no bad guys remain
        if True not in self.isActive:
            return
            # get the available bad guys into a list
        dudes = []
        if self.isActive[0]: dudes.append(0)
        if self.isActive[1]: dudes.append(1)
        if self.isActive[2]: dudes.append(2)
        print "DUDES:"
        print dudes
        # pick a random guy to shoot
        self.shooter = random.choice(dudes)
        print "THE SHOOTER IS: " + str(self.shooter)
        # load the animation
        anim = self.game.assets.dmd_bankDude
        # math out the wait
        self.shotWait = len(anim.frames) / 10.0
        # the shoots back animation
        eGuy0 = ep.EP_AnimatedLayer(anim)
        eGuy0.hold=True
        eGuy0.frame_time=6
        eGuy0.composite_op = "blacksrc"
        eGuy0.add_frame_listener(2,self.game.sound.play,param=self.game.assets.sfx_explosion11)
        eGuy0.add_frame_listener(2,self.game.base.flash,param=self.flashers[self.shooter])
        eGuy0.add_frame_listener(4,self.game.sound.play,param=self.game.assets.sfx_explosion11)
        eGuy0.add_frame_listener(4,self.game.base.flash,param=self.flashers[self.shooter])

        # set the position of the layer based on choice
        eGuy0.set_target_position(self.position[self.shooter],self.y_pos)
        # assign the layer to the positon of the shooter
        if self.shooter == 0:
            self.dude0Layer = eGuy0
        elif self.shooter == 1:
            self.dude1Layer = eGuy0
        elif self.shooter == 2:
            self.dude2Layer = eGuy0
            # set a flag
        self.shooting = True

    def end_shot_sequence(self):
        # if the guy who was shooting is still alive, reset their layer
        if self.shooter == 0 and self.isActive[0]:
            self.dude0Layer = self.dude0
        elif self.shooter == 1 and self.isActive[1]:
            self.dude1Layer = self.dude1
        elif self.shooter == 2 and self.isActive[2]:
            self.dude2Layer = self.dude2
        # assign a new dude
        self.set_shot_target()

    def abort_display(self):
        # if we're done, we should quit
        if True not in self.isActive and self.running:
           self.end_bank_robbery()
        self.cancel_delayed("Display")
        self.layer = None



