import os
import signal
import subprocess

import json
from urllib2 import Request, urlopen, URLError

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

# Notes
# DFP9 = Samsung TV
# DFP5 = NEC Monitor
# DFP11 = Asus Monitor

DIR_NAME = os.path.dirname(__file__)
INDICATOR_ID = 'CEC-TV'
INDICATOR_ICON = DIR_NAME + "/res/icon-dark-theme.svg"
INDICATOR_TITLE = 'TV Control'

CEC_PHYSICAL_ADDRESS = "/dev/ttyACM0"

MIRROR_TV = "xrandr --output DFP9 --auto --right-of DFP5"
EXTEND_TV = "xrandr --output DFP9 --auto --right-of DFP11"

ENABLE_TV = "on 0"
DISABLE_TV = "standby 0"
SOURCE_TV = "tx 1F:82:40:00"
SOURCE_PC = "tx 10:9D:40:00"

def main():
    indicator = appindicator.Indicator.new(INDICATOR_ID, INDICATOR_ICON, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(INDICATOR_ID)    
    gtk.main()

def build_menu():
    menu = gtk.Menu()

    menuTvMirror = gtk.MenuItem('Mirror TV')
    menuTvMirror.connect('activate', TvMirror)
    menu.append(menuTvMirror)
    
    menuTvExtend = gtk.MenuItem('Extend TV')
    menuTvExtend.connect('activate', TvExtend)
    menu.append(menuTvExtend)

    menu.append(gtk.SeparatorMenuItem("Options"))

    menuTvEnable = gtk.MenuItem('Turn On')
    menuTvEnable.connect('activate', TvEnable)
    menu.append(menuTvEnable)

    menuTvDisable = gtk.MenuItem('Turn Off')
    menuTvDisable.connect('activate', TvDisable)
    menu.append(menuTvDisable)
    
    menu.append(gtk.SeparatorMenuItem("Options"))
    
    menuTvSetPCActive = gtk.MenuItem('PC Active')
    menuTvSetPCActive.connect('activate', ChangeSourceToTV)
    menu.append(menuTvSetPCActive)

    menuTvSetTVActive = gtk.MenuItem('TV Active')
    menuTvSetTVActive.connect('activate', ChangeSourceToPC)
    menu.append(menuTvSetTVActive)
    
    menu.append(gtk.SeparatorMenuItem("Options"))
    
    menuQuit = gtk.MenuItem('Quit')
    menuQuit.connect('activate', ExitIndicator)
    menu.append(menuQuit)
    
    menu.show_all()
    
    return menu

def GetCommand(cecCmd):
    return "echo '" + cecCmd + "' | cec-client -s " + CEC_PHYSICAL_ADDRESS

def BashExecute(command):
    subprocess.check_output(['bash','-c', command])

def Notify(msg):
    notify.Notification.new(INDICATOR_TITLE, msg, None).show()

# Mirror TV
def TvMirror(_):
    BashExecute(MIRROR_TV)
    Notify("Reflecting Secondary Display to TV")
    
# Extend TV
def TvExtend(_):
    BashExecute(EXTEND_TV)
    Notify("Extending the display to TV")

# Turn on TV
def TvEnable(_):      
    BashExecute(GetCommand(ENABLE_TV))
    Notify("Turning on TV")
    
# Turn off TV
def TvDisable(_):       
    BashExecute(GetCommand(DISABLE_TV))
    Notify("Turning off TV")

# Set TV source to display television
def ChangeSourceToTV(_):       
    BashExecute(GetCommand(SOURCE_TV))
    Notify("Changing Display Source to TV")

# Set TV source to display PC
def ChangeSourceToPC(_):       
    BashExecute(GetCommand(SOURCE_PC))
    Notify("Changing Display Source to PC")

# Quit 
def ExitIndicator(_):
    notify.uninit()
    gtk.main_quit()
   
# Finish 
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()