from procgame import *


class Assets():

    def __init__(self, game):

        self.game = game

        # Paths
        self.lampshows_path = "lampshows/"
        self.sounds_path = "sounds/"
        self.sfx_path = "sounds/sfx/"
        self.music_path = "sounds/music/"
        self.quotes_path = "sounds/quotes/"
        self.dmd_path = "dmd/"

        # CC Fonts
        # _az = All numerals, letters, and lower case
        # _AZ = All numerals and upper case letters
        # _score = Numerals only
        self.font_5px_AZ = dmd.Font(self.dmd_path + "Font_3_CactusCanyon.dmd")
        self.font_5px_bold_AZ = dmd.Font(self.dmd_path + "Font_21_CactusCanyon.dmd")

        self.font_5px_bold_AZ_outline = dmd.Font(self.dmd_path + "Font_21_mask_CactusCanyon.dmd")
        self.font_5px_bold_AZ_outline.tracking = -1
        self.font_5px_bold_AZ_outline.composite_op = "blacksrc"

        self.font_6px_az = dmd.Font(self.dmd_path + "Font_19_CactusCanyon.dmd")

        self.font_7px_alt_az = dmd.Font(self.dmd_path + "Font_1_CactusCanyon.dmd")
        self.font_7px_az = dmd.Font(self.dmd_path + "Font_2_CactusCanyon.dmd")
        self.font_7px_score = dmd.Font(self.dmd_path + "Font_5_CactusCanyon.dmd")
        self.font_7px_extra_thin_score = dmd.Font(self.dmd_path + "Font_10_CactusCanyon.dmd")
        self.font_7px_thin_score = dmd.Font(self.dmd_path + "Font_4_CactusCanyon.dmd")
        self.font_7px_wide_score = dmd.Font(self.dmd_path + "Font_6_CactusCanyon.dmd")
        self.font_7px_bold_az = dmd.Font(self.dmd_path + "Font_14_CactusCanyon.dmd")

        self.font_9px_az = dmd.Font(self.dmd_path + "Font_15_CactusCanyon.dmd")
        self.font_9px_az_mid = dmd.Font(self.dmd_path + "Font_15_CactusCanyon_2.dmd")
        self.font_9px_az_dim = dmd.Font(self.dmd_path + "Font_15_CactusCanyon_1.dmd")

        self.font_12px_az = dmd.Font(self.dmd_path + "Font_16_CactusCanyon.dmd")
        self.font_12px_az_dim = dmd.Font(self.dmd_path + "Font_16_CactusCanyon_dim.dmd")

        self.font_12px_az_outline = dmd.Font(self.dmd_path + "Font_16_mask_CactusCanyon.dmd")
        self.font_12px_az_outline.tracking = -1
        self.font_12px_az_outline.composite_op = "blacksrc"

        self.font_13px_score = dmd.Font(self.dmd_path + "Font_8_CactusCanyon.dmd")
        self.font_13px_extra_thin_score = dmd.Font(self.dmd_path + "Font_11_CactusCanyon.dmd")
        self.font_13px_thin_score = dmd.Font(self.dmd_path + "Font_7_CactusCanyon.dmd")
        self.font_13px_wide_score = dmd.Font(self.dmd_path + "Font_9_CactusCanyon.dmd")

        self.font_15px_az = dmd.Font(self.dmd_path + "Font_17_CactusCanyon.dmd")

        self.font_15px_az_outline = dmd.Font(self.dmd_path + "Font_17_mask_CactusCanyon.dmd")
        self.font_15px_az_outline.tracking = -1
        self.font_15px_az_outline.composite_op = "blacksrc"

        self.font_17px_score = dmd.Font(self.dmd_path + "Font_12_CactusCanyon.dmd")

        #self.font_score_x12 = dmd.Font(self.dmd_path + "Font_Score_12_CactusCanyon.dmd")
        self.font_score_x12 = dmd.Font(self.dmd_path + "Font_12b_CactusCanyon.dmd")
        self.font_score_x11 = dmd.Font(self.dmd_path + "Font_12c_CactusCanyon.dmd")
        self.font_score_x10 = dmd.Font(self.dmd_path + "Font_12d_CactusCanyon.dmd")

        self.font_20px_az = dmd.Font(self.dmd_path + "Font_18_CactusCanyon.dmd")

        self.font_skillshot = dmd.Font(self.dmd_path + "Font_20_CactusCanyon.dmd")


        # CC Sounds
        # Sound Effects
        self.sfx_ballOneLock = 'sfx_ballOneLock'
        self.game.sound.register_sound(self.sfx_ballOneLock, self.sfx_path + "241-sfx-ball-one-lock.wav")
        self.sfx_banjoTrillUp = 'sfx_banjoTrillUp'
        self.game.sound.register_sound(self.sfx_banjoTrillUp, self.sfx_path + "622-banjo-trill-up.wav")
        self.sfx_banjoTrillDown = 'sfx_banjoTrillDown'
        self.game.sound.register_sound(self.sfx_banjoTrillDown, self.sfx_path + "623-banjo-trill-down.wav")
        self.sfx_banjoTaDa = 'sfx_banjoTaDa'
        self.game.sound.register_sound(self.sfx_banjoTaDa, self.sfx_path + "624-banjo-ta-da.wav")
        self.sfx_blow = 'sfx_blow'
        self.game.sound.register_sound(self.sfx_blow, self.sfx_path + "169-sfx-blow-on-gun.wav")
        self.sfx_breakingGlass1 = 'sfx_breakingGlass1'
        self.game.sound.register_sound(self.sfx_breakingGlass1, self.sfx_path + "119-sfx-breaking-glass-1.wav")
        self.sfx_breakingGlass2 = 'sfx_breakingGlass2'
        self.game.sound.register_sound(self.sfx_breakingGlass2, self.sfx_path + "135-sfx-breaking-glass-2.wav")
        self.sfx_cactusMash = 'sfx_cactusMash'
        self.game.sound.register_sound(self.sfx_cactusMash, self.sfx_path + "235-bonus-cactus-mash.wav")
        self.sfx_explosion1 = 'sfx_explosion1'
        self.game.sound.register_sound(self.sfx_explosion1, self.sfx_path + "105-sfx-explosion-1.wav")
        self.sfx_explosion11 = 'sfx_explosion2'
        self.game.sound.register_sound(self.sfx_explosion11, self.sfx_path + "257-sfx-explosion-11.wav")
        self.sfx_explosion17 = 'sfx_explosion17'
        self.game.sound.register_sound(self.sfx_explosion17, self.sfx_path + "341-sfx-explosion-17.wav")
        self.sfx_fallAndCrash1 = 'sfx_fallAndCrash1'
        self.game.sound.register_sound(self.sfx_fallAndCrash1, self.sfx_path + "101-sfx-fall-and-crash-1.wav")
        self.sfx_flourish6 = 'sfx_flourish6'
        self.game.sound.register_sound(self.sfx_flourish6, self.sfx_path + "032-flourish-6.wav")
        self.sfx_flourish7 = 'sfx_flourish7'
        self.game.sound.register_sound(self.sfx_flourish7, self.sfx_path + "034-flourish-7-Horns.wav")
        self.sfx_grinDing = 'sfx_grinDing'
        self.game.sound.register_sound(self.sfx_grinDing, self.sfx_path + "117-sfx-grin-ding.wav")
        self.sfx_rightRampEnter = 'sfx_rightRampEnter'
        self.game.sound.register_sound(self.sfx_rightRampEnter, self.sfx_path + "129-sfx-right-ramp-enter.wav")
        self.sfx_leftRampEnter = 'sfx_leftRampEnter'
        self.game.sound.register_sound(self.sfx_leftRampEnter, self.sfx_path + "407-sfx-river-ramp-splash.wav")
        self.sfx_leftLoopEnter = 'sfx_leftLoopEnter'
        self.game.sound.register_sound(self.sfx_leftLoopEnter, self.sfx_path + "179-woosh-with-horse-running.wav")
        self.sfx_orchestraRiff = 'sfx_orchestraRiff'
        self.game.sound.register_sound(self.sfx_orchestraRiff, self.sfx_path + "041-orchestra-riff.wav")
        self.sfx_quickdrawOff = 'sfx_quickdrawOff'
        self.game.sound.register_sound(self.sfx_quickdrawOff, self.sfx_path + "287-quickdraw-hit-light.wav")
        self.sfx_quickdrawOn = 'sfx_quickdrawOn'
        self.game.sound.register_sound(self.sfx_quickdrawOn, self.sfx_path + "289-quickdraw-hit-already-lit.wav")
        self.sfx_rattlesnake = 'sfx_rattlesnake'
        self.game.sound.register_sound(self.sfx_rattlesnake, self.sfx_path + "221-rattlesnake.wav")
        self.sfx_rightLoopEnter = 'sfx_rightLoopEnter'
        self.game.sound.register_sound(self.sfx_rightLoopEnter, self.sfx_path + "155-sfx-ricochet-triple.wav")
        self.sfx_skillShotWoosh = 'sfx_skillShotWoosh'
        self.game.sound.register_sound(self.sfx_skillShotWoosh, self.sfx_path + "393-skillshot-woosh.wav")
        self.sfx_thrownCoins = 'sfx_thrownCoins'
        self.game.sound.register_sound(self.sfx_thrownCoins, self.sfx_path + "137-sfx-thrown-coins.wav")
        self.sfx_yeeHoo = 'sfx_yeeHoo'
        self.game.sound.register_sound(self.sfx_yeeHoo, self.sfx_path + "1963-yee-hoo.wav")
        self.sfx_gunfightHit1 = 'sfx_gunfightHit1'
        self.game.sound.register_sound(self.sfx_gunfightHit1, self.sfx_path + "011-gunfight-hit-1.wav")
        self.sfx_gunfightHit2 = 'sfx_gunfightHit2'
        self.game.sound.register_sound(self.sfx_gunfightHit2, self.sfx_path + "013-gunfight-hit-2.wav")
        self.sfx_gunfightHit3 = 'sfx_gunfightHit3'
        self.game.sound.register_sound(self.sfx_gunfightHit3, self.sfx_path + "015-gunfight-hit-3.wav")
        self.sfx_gunfightBell = 'sfx_gunfightBell'
        self.game.sound.register_sound(self.sfx_gunfightBell, self.sfx_path + "123-gunfight-four-bells.wav")
        self.sfx_centerRampEnter = 'sfx_cetnerRampEnter'
        self.game.sound.register_sound(self.sfx_centerRampEnter, self.sfx_path + "201-train-center-ramp-enter-chugging.wav")
        self.sfx_quickdrawHit = 'sfx_quickdrawHit'
        self.game.sound.register_sound(self.sfx_quickdrawHit, self.sfx_path + "309-sfx-quickdraw-hit.wav")
        self.sfx_quickdrawCheer = 'sfx_quickdrawCheer'
        self.game.sound.register_sound(self.sfx_quickdrawCheer, self.sfx_path + "165-sfx-crowd-cheer-3.wav")
        self.sfx_bountyBell = 'sfx_bountyBell'
        self.game.sound.register_sound(self.sfx_bountyBell, self.sfx_path + "113-sfx-other-bell.wav")
        self.sfx_bountyCollected = 'sfx_bountyCollected'
        self.game.sound.register_sound(self.sfx_bountyCollected, self.sfx_path + "045-sfx-bounty-collected.wav")
        self.sfx_gunCock = 'sfx_gunCock'
        self.game.sound.register_sound(self.sfx_gunCock, self.sfx_path + "391-sfx-gun-cock.wav")
        self.sfx_gunfightShot = 'sfx_gunfightShot'
        self.game.sound.register_sound(self.sfx_gunfightShot, self.sfx_path + "339-sfx-gunfight-hit.wav")
        self.sfx_gunfightFlourish = 'sfx_gunfightFlourish'
        self.game.sound.register_sound(self.sfx_gunfightFlourish, self.sfx_path + "068-sfx-gunfight-flourish.wav")
        self.sfx_shooterLaunch = 'sfx_shooterLaunch'
        self.game.sound.register_sound(self.sfx_shooterLaunch, self.sfx_path + "273-sfx-shooter-lane-launch.wav")
        self.sfx_outlane = 'sfx_outlane'
        self.game.sound.register_sound(self.sfx_outlane, self.sfx_path + "283-sfx-outlane.wav")

        # Quotes
        # this bunches the welcome strings together for play_voice()
        self.quote_welcomes = 'quote_welcomes'
        self.game.sound.register_sound(self.quote_welcomes, self.quotes_path + "1202-prospector-welcome-to-cactus-canyon.wav")
        self.game.sound.register_sound(self.quote_welcomes, self.quotes_path + "1101-mayor-dewey-cheetum-at-your-service.wav")
        self.game.sound.register_sound(self.quote_welcomes, self.quotes_path + "1324-undertaker-welcome-to-cactus-canyon.wav")
        self.game.sound.register_sound(self.quote_welcomes, self.quotes_path + "2002-waitress-come-in-and-take-a-load-off-stranger.wav")
        self.game.sound.register_sound(self.quote_welcomes, self.quotes_path + "1100-mayor-welcome-to-cactus-canyon-stranger.wav")
        self.game.sound.register_sound(self.quote_welcomes, self.quotes_path + "803-polly-welcome-to-town-stranger.wav")
        self.quote_bountyLit = 'quote_bountyLit'
        self.game.sound.register_sound(self.quote_bountyLit, self.quotes_path + "1012-mayor-theres-a-bounty-just-waitin-for-ya.wav")
        self.game.sound.register_sound(self.quote_bountyLit, self.quotes_path + "1013-mayor-bounty-is-lit.wav")
        self.game.sound.register_sound(self.quote_bountyLit, self.quotes_path + "1043-mayor-collect-your-bounty-son.wav")
        self.quote_bountyCollected = 'quote_bountyCollected'
        self.game.sound.register_sound(self.quote_bountyCollected, self.quotes_path + "1014-mayor-your-bounty-friend.wav")
        self.game.sound.register_sound(self.quote_bountyCollected, self.quotes_path + "1042-mayor-bounty-collected.wav")
        self.quote_quickDrawLit = 'quote_quickDrawLit'
        self.game.sound.register_sound(self.quote_quickDrawLit, self.quotes_path + "509-townie-quickdraw-is-lit.wav")
        self.game.sound.register_sound(self.quote_quickDrawLit, self.quotes_path + "1304-undertaker-oh-goodie-quickdraw-is-lit.wav")
        self.game.sound.register_sound(self.quote_quickDrawLit, self.quotes_path + "1305-undertaker-quickdraws-are-good-for-business.wav")
        self.game.sound.register_sound(self.quote_quickDrawLit, self.quotes_path + "2040-waitress-quickdraw-is-lit.wav")
        self.game.sound.register_sound(self.quote_quickDrawLit, self.quotes_path + "1037-mayor-quickdraw-is-lit.wav")
        self.quote_quickDrawStart = 'quote_quickDrawStart'
        self.game.sound.register_sound(self.quote_quickDrawStart, self.quotes_path + "1241-prospector-get-that-bad-guy.wav")
        self.game.sound.register_sound(self.quote_quickDrawStart, self.quotes_path + "1274-prospector-nail-that-bad-guy-lawman.wav")
        self.game.sound.register_sound(self.quote_quickDrawStart, self.quotes_path + "1150-mayor-theres-a-bad-guy-out-there.wav")
        self.quote_quickDrawTaunt = 'quote_quickDrawTaunt'
        self.game.sound.register_sound(self.quote_quickDrawTaunt, self.quotes_path + "1151-mayor-shoot-the-bad-guy.wav")
        self.game.sound.register_sound(self.quote_quickDrawTaunt, self.quotes_path + "1554-leader-bart-go-on-take-your-best-shot.wav")
        self.game.sound.register_sound(self.quote_quickDrawTaunt, self.quotes_path + "1550-leader-bart-you-cant-shoot.wav")
        self.game.sound.register_sound(self.quote_quickDrawTaunt, self.quotes_path + "1552-leader-bart-come-on-tough-guy.wav")
        self.game.sound.register_sound(self.quote_quickDrawTaunt, self.quotes_path + "1156-mayor-mertilate-that-villan.wav")
        self.game.sound.register_sound(self.quote_quickDrawTaunt, self.quotes_path + "1155-mayor-shoot-that-scurvy-scoundrel.wav")
        self.game.sound.register_sound(self.quote_quickDrawTaunt, self.quotes_path + "1277-prospector-the-bad-guy-shoot-the-bad-guy.wav")
        self.game.sound.register_sound(self.quote_quickDrawTaunt, self.quotes_path + "2042-waitress-hit-that-bad-guy.wav")
        self.game.sound.register_sound(self.quote_quickDrawTaunt, self.quotes_path + "1520-leader-bart-go-get-im.wav")
        self.game.sound.register_sound(self.quote_quickDrawTaunt, self.quotes_path + "1416-drunk-shoot-that-bad-guy.wav")
        self.game.sound.register_sound(self.quote_quickDrawTaunt, self.quotes_path + "511-prospector-you-cant-shoot-nothin.wav")
        self.quote_quickDrawWin = 'quote_quickDrawWin'
        self.game.sound.register_sound(self.quote_quickDrawWin, self.quotes_path + "852-polly-nice-shootin.wav")
        self.game.sound.register_sound(self.quote_quickDrawWin, self.quotes_path + "1315-undertaker-my-theyre-dropping-like-flies.wav")
        self.game.sound.register_sound(self.quote_quickDrawWin, self.quotes_path + "2003-waitress-i-didnt-like-that-deadbeat-anyway.wav")
        self.game.sound.register_sound(self.quote_quickDrawWin, self.quotes_path + "1318-undertaker-a-dead-ringer.wav")
        self.game.sound.register_sound(self.quote_quickDrawWin, self.quotes_path + "1111-mayor-that-was-a-bit-too-close-for-comfort.wav")
        self.game.sound.register_sound(self.quote_quickDrawWin, self.quotes_path + "839-polly-youre-quite-a-man.wav")
        self.game.sound.register_sound(self.quote_quickDrawWin, self.quotes_path + "840-polly-congratulations.wav")
        self.game.sound.register_sound(self.quote_quickDrawWin, self.quotes_path + "2008-waitress-amazing.wav")
        self.game.sound.register_sound(self.quote_quickDrawWin, self.quotes_path + "2005-waitress-ooh-what-are-you-packin.wav")
        self.game.sound.register_sound(self.quote_quickDrawWin, self.quotes_path + "1116-mayor-this-calls-for-a-drink.wav")
        self.quote_lockLit = 'quote_lockLit'
        self.game.sound.register_sound(self.quote_lockLit, self.quotes_path + "1186-mayor-lock-is-lit.wav")
        self.game.sound.register_sound(self.quote_lockLit, self.quotes_path + "859-polly-lock-is-lit.wav")
        self.game.sound.register_sound(self.quote_lockLit, self.quotes_path + "1431-drunk-lock-is-lit.wav")
        self.game.sound.register_sound(self.quote_lockLit, self.quotes_path + "1432-drunk-lock-is-lit-and-so-am-i.wav")
        self.quote_leftRamp1 = 'quote_leftRamp1'
        self.game.sound.register_sound(self.quote_leftRamp1, self.quotes_path + "831-polly-im-gettin-all-wet.wav")
        self.game.sound.register_sound(self.quote_leftRamp1, self.quotes_path + "829-polly-were-headed-for-the-falls.wav")
        self.game.sound.register_sound(self.quote_leftRamp1, self.quotes_path + "1579-leader-bart-laugh-2.wav")
        self.quote_leftRamp2 = 'quote_leftRamp2'
        self.game.sound.register_sound(self.quote_leftRamp2, self.quotes_path + "830-polly-were-going-over-the-falls.wav")
        self.game.sound.register_sound(self.quote_leftRamp2, self.quotes_path + "1580-leader-bart-laugh-1.wav")
        self.quote_rightRamp1 = 'quote_rightRamp1'
        self.game.sound.register_sound(self.quote_rightRamp1, self.quotes_path + "1307-undertaker-oh-good-mayhem-at-the-bank.wav")
        self.game.sound.register_sound(self.quote_rightRamp1, self.quotes_path + "1134-mayor-well-do-somethin-my-moneys-in-there.wav")
        self.game.sound.register_sound(self.quote_rightRamp1, self.quotes_path + "1189-mayor-those-bart-boys-are-robbin-the-bank.wav")
        self.quote_rightRamp2 = 'quote_rightRamp2'
        self.game.sound.register_sound(self.quote_rightRamp2, self.quotes_path + "1580-leader-bart-laugh-1.wav")
        self.game.sound.register_sound(self.quote_rightRamp2, self.quotes_path + "850-polly-ooh-how-brave.wav")
        self.quote_centerRamp1 = 'quote_centerRamp1'
        self.game.sound.register_sound(self.quote_centerRamp1, self.quotes_path + "1576-leader-bart-you-cant-stop-this-train.wav")
        self.quote_centerRamp2 = 'quote_centerRamp2'
        self.game.sound.register_sound(self.quote_centerRamp2, self.quotes_path + "1577-leader-bart-youll-never-catch-us.wav")
        self.quote_leftLoop1 = 'quote_leftLoop1'
        self.game.sound.register_sound(self.quote_leftLoop1, self.quotes_path + "1255-prospector-guess-that-horse-is-breaking-you-in.wav")
        self.game.sound.register_sound(self.quote_leftLoop1, self.quotes_path + "1200-prospector-woo-cough.wav")
        self.game.sound.register_sound(self.quote_leftLoop1, self.sfx_path + "115-sfx-horse-running-with-yell.wav")
        self.game.sound.register_sound(self.quote_leftLoop1, self.quotes_path + "1254-prospector-oh-boy-thats-gotta-hurt.wav")
        self.quote_leftLoop2 = 'quote_leftLoop2'
        self.game.sound.register_sound(self.quote_leftLoop2, self.quotes_path + "2007-waitress-i-like-how-you-ride-that-horse.wav")
        self.game.sound.register_sound(self.quote_leftLoop2, self.quotes_path + "1187-mayor-a-fine-ride-sir.wav")
        self.game.sound.register_sound(self.quote_leftLoop2, self.quotes_path + "1256-prospector-ride-em-cowboy-hey-hey.wav")
        self.quote_victory = 'quote_victory'
        self.game.sound.register_sound(self.quote_victory, self.quotes_path + "836-polly-youre-the-greatest.wav")
        self.game.sound.register_sound(self.quote_victory, self.quotes_path + "837-polly-youre-my-hero.wav")
        self.game.sound.register_sound(self.quote_victory, self.quotes_path + "838-polly-my-hero.wav")
        self.quote_gunfightLit = 'quote_gunfightLit'
        self.game.sound.register_sound(self.quote_gunfightLit, self.quotes_path + "1038-mayor-gunfight-is-lit.wav")
        self.game.sound.register_sound(self.quote_gunfightLit, self.quotes_path + "1237-prospector-gunfight-is-lit.wav")
        self.game.sound.register_sound(self.quote_gunfightLit, self.quotes_path + "1306-undertaker-theres-going-to-be-a-gunfight.wav")
        self.quote_gunfightStart = 'quote_gunfightStart'
        self.game.sound.register_sound(self.quote_gunfightStart, self.quotes_path + "1004-mayor-ok-son-lets-gunfight.wav")
        self.game.sound.register_sound(self.quote_gunfightStart, self.quotes_path + "1029-mayor-dont-move-its-a-gunfight.wav")
        self.game.sound.register_sound(self.quote_gunfightStart, self.quotes_path + "2041-waitress-looks-like-a-gunfight.wav")
        self.game.sound.register_sound(self.quote_gunfightStart, self.quotes_path + "1233-prospector-ooh-i-smell-a-gunfight-brewin.wav")
        self.quote_gunWin = 'quote_gunWin'
        self.game.sound.register_sound(self.quote_gunWin, self.quotes_path + "1117-mayor-say-thats-a-pretty-good-eye-there.wav")
        self.game.sound.register_sound(self.quote_gunWin, self.quotes_path + "1170-mayor-quite-a-knack-with-those-six-shooters-friend.wav")
        self.quote_gunFail = 'quote_gunFail'
        self.game.sound.register_sound(self.quote_gunFail, self.quotes_path + "1198-mayor-maybe-you-better-check-the-sights-on-that-weapon.wav")
        self.game.sound.register_sound(self.quote_gunFail, self.quotes_path + "1199-mayor-are-you-sure-that-thing-is-loaded.wav")
        self.quote_beerMug = 'quote_beerMug'
        self.game.sound.register_sound(self.quote_beerMug, self.quotes_path + "1408-drunk-hey-buddy-you-shot-my-drink.wav")
        self.game.sound.register_sound(self.quote_beerMug, self.quotes_path + "1409-drunk-stop-shootin-at-my-drink.wav")
        self.game.sound.register_sound(self.quote_beerMug, self.quotes_path + "1414-drunk-i-was-drinking-that-thank-you.wav")
        self.quote_extraBallLit = 'quote_extraBallLit'
        self.game.sound.register_sound(self.quote_extraBallLit, self.quotes_path + "2013-waitress-that-extra-ball-is-lit-honey.wav")
        self.game.sound.register_sound(self.quote_extraBallLit, self.quotes_path + "1258-prospector-extra-ball-is-lit.wav")
        self.game.sound.register_sound(self.quote_extraBallLit, self.quotes_path + "1020-mayor-the-extra-ball-is-lit.wav")

        self.quote_hitBigBart = 'quote_hitBigBart'
        self.game.sound.register_sound(self.quote_hitBigBart, self.quotes_path + "1451-big-hit-that-hurt-a-little.wav")
        self.game.sound.register_sound(self.quote_hitBigBart, self.quotes_path + "1452-big-hit-nothin-but-a-little-hole.wav")
        self.game.sound.register_sound(self.quote_hitBigBart, self.quotes_path + "1456-big-hit-ow-i-said.wav")
        self.game.sound.register_sound(self.quote_hitBigBart, self.quotes_path + "1460-big-hit-ow.wav")
        self.game.sound.register_sound(self.quote_hitBigBart, self.quotes_path + "1462-big-hit-well-that-hurt.wav")
        self.game.sound.register_sound(self.quote_hitBigBart, self.quotes_path + "1464-big-hit-ow-dangit.wav")
        self.game.sound.register_sound(self.quote_hitBigBart, self.quotes_path + "1465-big-hit-well-i-can-tell-ya-that-hurt.wav")
        self.quote_tauntBigBart = 'quote_tauntBigBart'
        self.game.sound.register_sound(self.quote_tauntBigBart, self.quotes_path + "1450-big-taunt-mess-with-me-will-ya.wav")
        self.game.sound.register_sound(self.quote_tauntBigBart, self.quotes_path + "1454-big-taunt-youre-messin-with-the-wrong-hombre-hombre.wav")
        self.game.sound.register_sound(self.quote_tauntBigBart, self.quotes_path + "1457-big-taunt-im-gonna-shoot-my-initials-in-ya-lawman.wav")
        self.game.sound.register_sound(self.quote_tauntBigBart, self.quotes_path + "1467-big-taunt-what-do-you-think-youre-doin-pilgrim.wav")
        self.quote_defeatBigBart = 'quote_defeatBigBart'
        self.game.sound.register_sound(self.quote_defeatBigBart, self.quotes_path + "1468-big-defeat-well-im-done-for.wav")
        self.game.sound.register_sound(self.quote_defeatBigBart, self.quotes_path + "1469-big-defeat-well-thats-all-folks.wav")
        self.game.sound.register_sound(self.quote_defeatBigBart, self.quotes_path + "1470-big-defeat-i-guess-ill-just-fall-down-now.wav")

        self.quote_hitBandeleroBart = 'quote_hitBandeleroBart'
        self.game.sound.register_sound(self.quote_hitBandeleroBart, self.quotes_path + "1803-bandelero-hit-oh-i-think-ive-been-hit.wav")
        self.game.sound.register_sound(self.quote_hitBandeleroBart, self.quotes_path + "1804-bandelero-hit-that-one-hurt.wav")
        self.game.sound.register_sound(self.quote_hitBandeleroBart, self.quotes_path + "1806-bandelero-hit-ooh-ive-been-air-conditioned.wav")
        self.game.sound.register_sound(self.quote_hitBandeleroBart, self.quotes_path + "1809-bandelero-hit-look-at-all-this-blood-my-wife-is-going-to-kill-me.wav")
        self.game.sound.register_sound(self.quote_hitBandeleroBart, self.quotes_path + "1810-bandelero-hit-holy-camochie-ive-been-shot.wav")
        self.game.sound.register_sound(self.quote_hitBandeleroBart, self.quotes_path + "1823-bandelero-hit-ooh.wav")
        self.quote_tauntBandeleroBart = 'quote_tauntBandeleroBart'
        self.game.sound.register_sound(self.quote_tauntBandeleroBart, self.quotes_path + "1801-bandelero-taunt-you-dont-think-i-see-you-but-i-do.wav")
        self.game.sound.register_sound(self.quote_tauntBandeleroBart, self.quotes_path + "1807-bandelero-taunt-you-couldnt-hit-the-broad-side-of-a-burrito.wav")
        self.game.sound.register_sound(self.quote_tauntBandeleroBart, self.quotes_path + "1808-bandelero-taunt-my-burro-can-shoot-better-than-that.wav")
        self.game.sound.register_sound(self.quote_tauntBandeleroBart, self.quotes_path + "1821-bandelero-taunt-come-on-lone-ranger.wav")
        self.quote_defeatBandeleroBart = 'quote_defeatBandeleroBart'
        self.game.sound.register_sound(self.quote_defeatBandeleroBart, self.quotes_path + "1813-bandelero-defeat-adios-amigo-time-for-a-siesta.wav")
        self.game.sound.register_sound(self.quote_defeatBandeleroBart, self.quotes_path + "1814-bandelero-defeat-say-youre-pretty-good.wav")
        self.game.sound.register_sound(self.quote_defeatBandeleroBart, self.quotes_path + "1824-bandelero-defeat-you-got-me.wav")

        self.quote_hitBubbaBart = 'quote_hitBubbaBart'
        self.game.sound.register_sound(self.quote_hitBubbaBart, self.quotes_path + "1900-bubba-hit-bubba-hit.wav")
        self.game.sound.register_sound(self.quote_hitBubbaBart, self.quotes_path + "1901-bubba-hit-bubba-mad-now.wav")
        self.game.sound.register_sound(self.quote_hitBubbaBart, self.quotes_path + "1906-bubba-hit-shiny-ball-hurt.wav")
        self.game.sound.register_sound(self.quote_hitBubbaBart, self.quotes_path + "1909-bubba-hit-uh.wav")
        self.game.sound.register_sound(self.quote_hitBubbaBart, self.quotes_path + "1910-bubba-hit-groan.wav")
        self.game.sound.register_sound(self.quote_hitBubbaBart, self.quotes_path + "1912-bubba-hit-oh.wav")
        self.game.sound.register_sound(self.quote_hitBubbaBart, self.quotes_path + "1914-bubba-hit-groan2.wav")
        self.game.sound.register_sound(self.quote_hitBubbaBart, self.quotes_path + "1918-bubba-hit-groan3.wav")
        self.quote_tauntBubbaBart = 'quote_tauntBubbaBart'
        self.game.sound.register_sound(self.quote_tauntBubbaBart, self.quotes_path + "1902-bubba-taunt-you-mess-wif-bubba-bubba-mess-wif-you.wav")
        self.game.sound.register_sound(self.quote_tauntBubbaBart, self.quotes_path + "1903-bubba-taunt-bubba-mess-pants.wav")
        self.game.sound.register_sound(self.quote_tauntBubbaBart, self.quotes_path + "1905-bubba-taunt-bubba-like-shiny-silver-ball.wav")
        self.game.sound.register_sound(self.quote_tauntBubbaBart, self.quotes_path + "1915-bubba-taunt-me-bubba-you-dead.wav")
        self.game.sound.register_sound(self.quote_tauntBubbaBart, self.quotes_path + "1917-bubba-taunt-bubba-gonna-mess-you-up.wav")
        self.game.sound.register_sound(self.quote_tauntBubbaBart, self.quotes_path + "1919-bubba-taunt-youre-dead.wav")
        self.quote_defeatBubbaBart = 'quote_defeatBubbaBart'
        self.game.sound.register_sound(self.quote_defeatBubbaBart, self.quotes_path + "1904-bubba-defeat-bubba-take-dirt-nap.wav")
        self.game.sound.register_sound(self.quote_defeatBubbaBart, self.quotes_path + "1916-bubba-defeat-nite-nite-bubba-go-to-sleep-now.wav")

        self.quote_pollyHelp = 'quote_pollyHelp'
        self.game.sound.register_sound(self.quote_pollyHelp, self.quotes_path + "802-polly-help.wav")
        self.quote_pollyThankYou = 'quote_pollyThankYou'
        self.game.sound.register_sound(self.quote_pollyThankYou,self.quotes_path + "835-polly-thank-you.wav")
        self.quote_playerTwo = 'quote_playerTwo'
        self.game.sound.register_sound(self.quote_playerTwo, self.quotes_path + "856-polly-player-two.wav")
        self.quote_playerThree = 'quote_playerThree'
        self.game.sound.register_sound(self.quote_playerThree, self.quotes_path + "857-polly-player-three.wav")
        self.quote_playerFour = 'quote_playerFour'
        self.game.sound.register_sound(self.quote_playerFour, self.quotes_path + "858-polly-player-four.wav")
        self.quote_mayorMyMoneysInThere = 'quote_mayorMyMoneysInThere'
        self.game.sound.register_sound(self.quote_mayorMyMoneysInThere, self.quotes_path + "1134-mayor-well-do-somethin-my-moneys-in-there.wav")
        self.quote_gunfightReady = 'quote_gunfightReady'
        self.game.sound.register_sound(self.quote_gunfightReady, self.quotes_path + "1546-leader-bart-ready.wav")
        self.quote_gunfightSet = 'quote_gunfight_Set'
        self.game.sound.register_sound(self.quote_gunfightSet, self.quotes_path + "1547-leader-bart-set.wav")
        self.quote_gunfightDraw = 'quote_gunfightDraw'
        self.game.sound.register_sound(self.quote_gunfightDraw, self.quotes_path + "1507-leader-bart-draw.wav")


        # Music
        self.music_drumRiff = 'music_drumRiff'
        self.game.sound.register_sound(self.music_drumRiff, self.music_path + "001-drum-lead-in.wav")
        self.music_shooterLaneGroove = 'music_shooterLaneGroove'
        self.game.sound.register_music(self.music_shooterLaneGroove, self.music_path + "001-shooter-lane-groove.wav")
        self.music_mainTheme = 'music_mainTheme'
        self.game.sound.register_music(self.music_mainTheme, self.music_path + "002-song-starting-gameplay.wav")
        self.music_quickDrawBumper = 'music_quickDrawBumper'
        self.game.sound.register_sound(self.music_quickDrawBumper, self.music_path + "017-quickdraw-bumper.wav")
        self.music_quickDraw = 'music_quickDraw'
        self.game.sound.register_music(self.music_quickDraw, self.music_path + "025-quickdraw.wav")
        self.music_gunfightIntro = 'music_gunfightIntro'
        self.game.sound.register_sound(self.music_gunfightIntro, self.music_path + "009-gunfight-intro.wav")
        self.music_drumRoll = 'music_drumRoll'
        self.game.sound.register_music(self.music_drumRoll, self.music_path + "009-gunfight-drumroll.wav")

        # Shared Paths
        self.shared_sound_path = "shared/sound/"
        self.shared_dmd_path = "shared/dmd/"

        # Shared Fonts
        self.font_tiny7 = dmd.Font(self.shared_dmd_path + "04B-03-7px.dmd")
        self.font_jazz18 = dmd.Font(self.shared_dmd_path + "Jazz18-18px.dmd")
        self.font_18x12 = dmd.Font(self.shared_dmd_path + "Font18x12.dmd")
        self.font_18x11 = dmd.Font(self.shared_dmd_path + "Font18x11.dmd")
        self.font_14x10 = dmd.Font(self.shared_dmd_path + "Font14x10.dmd")
        self.font_14x9 = dmd.Font(self.shared_dmd_path + "Font14x9.dmd")
        self.font_14x8 = dmd.Font(self.shared_dmd_path + "Font14x8.dmd")
        self.font_09Bx7 = dmd.Font(self.shared_dmd_path + "Font09Bx7.dmd")
        self.font_09x7 = dmd.Font(self.shared_dmd_path + "Font09x7.dmd")
        self.font_09x6 = dmd.Font(self.shared_dmd_path + "Font09x6.dmd")
        self.font_09x5 = dmd.Font(self.shared_dmd_path + "Font09x5.dmd")
        self.font_07x4 = dmd.Font(self.shared_dmd_path + "Font07x4.dmd")
        self.font_07x5 = dmd.Font(self.shared_dmd_path + "Font07x5.dmd")

        # Shared Sounds
        self.game.sound.register_sound('service_enter', self.shared_sound_path + "menu_in.wav")
        self.game.sound.register_sound('service_exit', self.shared_sound_path + "menu_out.wav")
        self.game.sound.register_sound('service_next', self.shared_sound_path + "next_item.wav")
        self.game.sound.register_sound('service_previous', self.shared_sound_path + "previous_item.wav")
        self.game.sound.register_sound('service_switch_edge', self.shared_sound_path + "switch_edge.wav")
        self.game.sound.register_sound('service_save', self.shared_sound_path + "save.wav")
        self.game.sound.register_sound('service_cancel', self.shared_sound_path + "cancel.wav")
