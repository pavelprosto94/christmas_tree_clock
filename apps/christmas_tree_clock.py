try:
  if str(__file__) == "menu/app.py":
    import machine, deviceCfg
    fileA, fileB = open('/flash/apps/christmas_tree_clock.py', 'rb'), open('/flash/main.py', 'wb')
    fileB.write(fileA.read())
    fileA.close()
    fileB.close()
    deviceCfg.set_device_mode(2)
    machine.reset()
except Exception as e:
  print("run clock")
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
from machine import Timer
gc.collect()
sys.path.append("/flash/sys")
title_font,body_font=lv.font_montserrat_18,lv.font_montserrat_14
from helper import *
#from notifications import getUnreadNotificationsCount
power.setPowerLED(False)
power.setVibrationEnable(False)
from easyIO import map_value
sys.path.append("/flash/apps")
def loadPNG(path):
  with open(path,'rb') as f: data = f.read()
  img_dsc = lv.img_dsc_t({'data_size': len(data),'data': data })
  return img_dsc

def getBrightness(hh,mm):
  if hh<6:
    if ADAPTIVE_BR: return(10)
    else: return(MAX_BR)
  elif hh<12:
    if ADAPTIVE_BR: return int((hh-6)*60+mm)/(6*60)*(MAX_BR-MIN_BR)+MIN_BR
    else: return(MAX_BR)
  elif hh<18:
    return(MAX_BR)
  else:
    if ADAPTIVE_BR: return int(6*60-((hh-18)*60+mm))/(6*60)*(MAX_BR-MIN_BR)+MIN_BR
    else: return(MAX_BR)

def playAlarm():
  global wavFreez
  wavFreez = True
  wait(0.1)
  if ALARM_WAV!="None":
    while alarm_mode>-1:
      speaker.playWAV(ALARM_WAV)
      wait(0.1)
  wavFreez = False

def playNotify():
  global wavFreez
  wavFreez = True
  wait(0.1)
  if NOTIFY_WAV!="None":
    speaker.playWAV(NOTIFY_WAV)
    wait(0.1)
  wavFreez = False

def drawButtory():
  ch=1
  if (power.getChargeState()): ch=0
  but_val=6-map_value((power.getBatVoltage()), 3.7, 4.1, 0, 6)
  image2.set_offset_y(ch*40)
  image2.set_offset_x(-but_val*40)

def redrawClock():
  global x, y, xl, yl, balls_edit, timerAlarm
  while wavFreez:
    wait(0.2)
  balls_edit=False
  if alarm_mode>-1:
    for i in range(len(ball_sizes)): balls[i].set_hidden(True)
    image0.set_src(loadPNG("res/christmas/background_alarm.png"))
    image3.set_hidden(False)
    label2.set_text("Catch Santa!")
    label2.align(root,lv.ALIGN.IN_TOP_MID, 0, 218)
    label0.set_style_local_text_font(0,0,lv.font_montserrat_26)
    label0.set_pos(130, 4)
    label1.set_style_local_text_font(0,0,lv.font_montserrat_10)
    label1.set_pos(130, 34)
    x,y,xl,yl=0,random.randint(1, 11)*10,0,4
    image1.set_offset_y(28*int(xl/4))
    image1.set_offset_x(48*(xl % 4))
    image1.set_pos(0,y)
    image1.set_auto_size(False)
    image1.set_size(48,28)
    image1.set_src(loadPNG("res/christmas/santa.png"))
    if wavFreez == False: _thread.start_new_thread(playAlarm,())
    timerAlarm.init(period=1000, mode=Timer.PERIODIC, callback=drawAlarm)
  else:
    label0.set_style_local_text_font(0,0,lv.font_montserrat_48)
    label0.set_pos(180,15)
    label1.set_style_local_text_font(0,0,title_font)
    label1.set_pos(185,65)
    image0.set_src(loadPNG("res/christmas/background.png"))
    for i in range(len(ball_sizes)): balls[i].set_hidden(False)
    image3.set_hidden(True)
    label2.set_text("")
    x,y=0,0
    image1.set_offset_y(y)
    image1.set_offset_x(x)
    image1.set_pos(0,0)
    image1.set_auto_size(False)
    image1.set_size(320,240)
    image1.set_src(loadPNG("res/christmas/snow.png"))
    image1.set_hidden(False)

timerAlarm=Timer(2)
drFreez=False
def drawAlarm(Timer):
  global x, y, xl, yl, drFreez
  if alarm_mode>-1 and not drFreez:
    drFreez=True
    xl,x=xl+1,x+yl
    if xl>7: xl=0
    if x>320: yl,y=-4,random.randint(1, 11)*10
    if x<-48: yl,y=4,random.randint(1, 11)*10
    image1.set_pos(x,y)
    if yl>0: image1.set_offset_y(-28*int(xl/4))
    else: image1.set_offset_y(-28*(2+int(xl/4)))
    image1.set_offset_x(48*(xl % 4))
    drFreez=False

def draw25sec():
  global but_state, x, y, xl, yl,drFreez
  label0.set_text(str("{:02d}:{:02d}").format(now[4],now[5]))
  label1.set_text(str("{:02d}-{:02d}-{:04d}").format(now[2],now[1],now[0]))
  if alarm_mode==-1 and not drFreez:
    drFreez=True
    if not balls_edit:
      x,y=x+random.randint(-1, 1),y+1
      if y>=240: y=0
      if x==240: x=0
      elif x<0: x=239
      image1.set_offset_y(y)
      image1.set_offset_x(x)
    if (but_state!=power.getChargeState()):
      but_state=power.getChargeState()
      drawButtory()
    drFreez=False

def draw100sec():
  global br
  if alarm_mode==-1:
    br=getBrightness(now[4],now[5])
    power.setLCDBrightness(br)
    drawButtory()

def onTouchPressed():
  global touched_pos, alarms, alarm_mode, fix_update
  if alarm_mode>-1:
    touched_pos=touch.read()
    if touched_pos[0]>=x-5 and touched_pos[0]<=x+5+48 and touched_pos[1]>=y-10 and touched_pos[1]<=y+10+28:
      image1.set_hidden(True)
      vibrating()
      timerAlarm.deinit()
      label2.set_text("")
      if alarm_mode<len(alarms):
        alarms[alarm_mode][3]=pastMinutesOfYear(now[1],now[2],now[4],now[5])
        if len(alarms[alarm_mode][2])==0:
          disableAlarm(alarms[alarm_mode][0],alarms[alarm_mode][1])
          alarms=getAlarms()
      alarm_mode,touched_pos,fix_update=-1,None,1

# def onTouchReleased():
#   pass

MAX_BR, ADAPTIVE_BR, MIN_BR, UTC_ZONE, ALARM_WAV, NOTIFY_WAV, NOTIFY_PERIODIC=ConfigLoad()
br,alarm_mode,alarm_mode_old,alarms,wavFreez=MAX_BR,-1,-1,getAlarms(),False
power.setLCDBrightness(br)
now, root = rtc.datetime(), lv.obj()
image0 = lv.img(root)
image0.set_pos(0,0)
image0.set_src(loadPNG("res/christmas/background.png"))
ball_sizes=[[107,56,118,75,11,19],[116,68,135,85,19,17],[152,75,168,95,16,20],[91,81,108,100,17,19],[134,92,150,110,16,18],[160,100,180,120,20,20],[78,110,98,136,20,26],[100,108,116,132,16,24],[140,121,160,143,20,22],[120,144,142,165,22,21],[161,133,182,163,21,30],[61,151,95,194,34,43],[135,172,179,214,44,42],]
balls=[]
ball_ind=loadChristmas()
for i in range(len(ball_sizes)):
  balls.append(lv.img(root))
  balls[i].set_pos(ball_sizes[i][0],ball_sizes[i][1])
  balls[i].set_auto_size(False)
  balls[i].set_src(loadPNG("res/christmas/ball_{}.png".format(i)))
  balls[i].set_size(ball_sizes[i][4],ball_sizes[i][5])
  balls[i].set_offset_y(ball_ind[i]*ball_sizes[i][5])
image2,image1,image3=lv.img(root),lv.img(root),lv.img(root)
image1.set_pos(0,0)
image1.set_auto_size(False)
image1.set_size(320,240)
image1.set_src(loadPNG("res/christmas/snow.png"))
image2.set_pos(20,8)
image2.set_auto_size(False)
image2.set_size(40,40)
image2.set_src(loadPNG("res/christmas/bat.png"))
image3.set_pos(0,190)
image3.set_src(loadPNG("res/christmas/back.png"))
root.add_style(0,style)
label0,label1,label2 = lv.label(root),lv.label(root),lv.label(root)
label0.set_pos(180,15)
label0.set_style_local_text_font(0,0,lv.font_montserrat_48)
label0.set_text(str("{:02d}:{:02d}").format(now[4],now[5]))
label1.set_pos(185,65)
label1.set_style_local_text_font(0,0,title_font)
label1.set_text(str("{:02d}-{:02d}-{:04d}").format(now[2],now[1],now[0]))
label2.set_style_local_text_font(0,0,title_font)
label2.set_style_local_text_color(0,0,lv.color_hex(0xf0a010))
label2.set_text("initialization...")
label2.align(root,lv.ALIGN.IN_TOP_MID, 0, 216)
drawButtory()
x,y,xl,yl = 0,0,0,0
lv.disp_load_scr(root)
gc.collect()
wait(3)
image3.set_hidden(True)
label2.set_text("")
balls_edit,fix_update,run,but_state,touched_pos,touched_time,touched_cord=False,0,True,power.getChargeState(),None,0,None
try:
  while run:
    if balls_edit:
      if touch.status():
        if touched_time==0:
          touched_time,touched_cord=time.ticks_ms(),touch.read()
        elif time.ticks_ms()-touched_time>1000:
          vibrating()
          image1.set_hidden(False)
          image3.set_hidden(True)
          label2.set_text("")
          balls_edit=False
          saveChristmas(ball_ind)
          touched_time=-1
      elif touched_time!=0:
        if time.ticks_ms()-touched_time<500 and touched_time!=-1:
          for i in range(len(ball_sizes)):
            if touched_cord[0]>=ball_sizes[i][0] and touched_cord[1]>=ball_sizes[i][1] and touched_cord[0]<=ball_sizes[i][2] and touched_cord[1]<=ball_sizes[i][3]:
              ball_ind[i]=ball_ind[i]+1
              if ball_ind[i]>4: ball_ind[i]=0
              balls[i].set_offset_y(ball_ind[i]*ball_sizes[i][5])
              vibrating()
              break
        touched_time=0
    else:
      if fix_update%5==0:
        if (alarm_mode!=alarm_mode_old):
          alarm_mode_old=alarm_mode
          redrawClock()
          fix_update=1
          power.setLCDBrightness(MAX_BR)
        #draw05sec()
        if not run:
          break
        if fix_update%25==0:
          now = rtc.datetime()
          for i,al in enumerate(alarms):
            if al[0]==now[4] and al[1]==now[5]:
              if al[3]<pastMinutesOfYear(now[1],now[2],now[4],now[5]):
                if len(al[2])==0: alarm_mode=i
                elif now[3] in al[2]: alarm_mode=i
          draw25sec()
          if fix_update%100==0:
            draw100sec()
      elif fix_update>250:
        fix_update=1
        #gc.collect()
      elif touch.status():
        if touched_time==0:
          touched_time,touched_cord=time.ticks_ms(),touch.read()
          onTouchPressed()
          if br!=MAX_BR:
            while drFreez: wait(0.1)
            br=MAX_BR
            power.setLCDBrightness(br)
            fix_update=1
            vibrating()
        elif touched_time!=-1 and alarm_mode==-1:
          if time.ticks_ms()-touched_time>500:
            if distance(touched_cord,touch.read())<3:
              touched_time=-1
              if (touch.read()[1]) > 230:
                if (touch.read()[0])<315 and (touch.read()[0])>225:
                  vibrating()
                  lv.disp_load_scr(rootLoading)
                  wait(0.01)
                  exec(open("/flash/apps/apps_explorer.py").read(),{})
                  lv.disp_load_scr(root)
                  MAX_BR, ADAPTIVE_BR, MIN_BR, UTC_ZONE, ALARM_WAV, NOTIFY_WAV, NOTIFY_PERIODIC=ConfigLoad()
                  fix_update=1
                elif (touch.read()[0])<215 and (touch.read()[0])>115:
                  vibrating()
                  lv.disp_load_scr(rootLoading)
                  wait(0.01)
                  from Alarm_explorer import alarmExplorer
                  subscreen=alarmExplorer()
                  lv.disp_load_scr(root)
                  subscreen.delete()
                  alarms=getAlarms()
                  fix_update=1
                elif (touch.read()[0])<105 and (touch.read()[0])>5:
                  vibrating()
                  lv.disp_load_scr(rootLoading)
                  wait(0.01)
                  from Notify_explorer import notificationsExplorer  
                  subscreen=notificationsExplorer(body_font, title_font)
                  lv.disp_load_scr(root)
                  subscreen.delete()
                  #NotifyUpdate()
                  fix_update=1
              elif (touch.read()[1]) < 220:
                if not wavFreez and image1.is_visible():
                  vibrating()
                  balls_edit=True
                  image1.set_hidden(True)
                  image3.set_hidden(False)
                  label2.set_text("Edit tree. Hold to save.")
                  label2.align(root,lv.ALIGN.IN_TOP_MID, 0, 218)
      else:
        if touched_time!=0:
          #if touched_pos!=None and touched_time!=-1:
          #  onTouchReleased()
          touched_time=0
    fix_update+=1
    if balls_edit or alarm_mode>-1: wait(0.05)
    else: wait(0.4)
except Exception as e:
  label.set_pos(0,0)
  label.set_text(str(e))
  lv.disp_load_scr(rootLoading)