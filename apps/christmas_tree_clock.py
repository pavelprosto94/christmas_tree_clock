from m5stack import lv, rtc, speaker, power, touch
style, rootLoading  = lv.style_t(), lv.obj()
style.init()
style.set_bg_color(0,lv.color_hex(0x000))
style.set_text_color(0,lv.color_hex(0xf0f0f0))
rootLoading.add_style(0,style)
label = lv.label(rootLoading)
label.set_text('Loading...')
label.align(rootLoading,lv.ALIGN.CENTER, 0, 0)
lv.disp_load_scr(rootLoading)
from uiflow import wait
wait(0.01)
import sys, time, random, _thread, gc, os
gc.collect()
sys.path.append("/flash/sys")
label.set_text('Loading...1')
title_font,body_font=lv.font_montserrat_18,lv.font_montserrat_14
from helper import *
from notifications import getUnreadNotificationsCount
power.setPowerLED(False)
power.setVibrationEnable(False)
from easyIO import map_value
sys.path.append("/flash/apps")
label.set_text('Loading...1')
os.mkdir("/flash/res/christmas_tree_clock/")
label.set_text('Loading...!')