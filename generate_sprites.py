from PIL import Image, ImageDraw
from pathlib import Path
P=Path(__file__).parent/'sprites'; P.mkdir(exist_ok=True)
C={'o':'#211a1a','hair':'#31292a','h2':'#403334','skin':'#a95e34','light':'#bb7140','shade':'#854625','beard':'#332726','b2':'#44332e','shirt':'#704538','s2':'#57342d','s3':'#865244','pants':'#35333c','p2':'#24232b','white':'#fff2d7','shoe':'#c5bda9','gold':'#ffbd43','purple':'#b9a0f2','laptop':'#777482','screen':'#454353','coffee':'#e9d8bd'}
def sprite(state,i):
 im=Image.new('RGBA',(48,48)); d=ImageDraw.Draw(im)
 def r(x,y,w,h,c): d.rectangle((x,y,x+w-1,y+h-1),fill=C.get(c,c))
 def p(coords,c): d.polygon(coords,fill=C.get(c,c))
 def star(x,y,c='gold'):
  r(x,y-2,1,5,c); r(x-2,y,5,1,c)
 def arm(x,y,side,pose):
  if pose=='up':
   r(x,y-4,5,8,'o'); r(x+1,y-3,3,3,'skin'); r(x+1,y,3,3,'s3')
  else:
   r(x,y,5,8,'o'); r(x+1,y+1,3,4,'shirt'); r(x+1,y+5,3,2,'skin')
 # movement stays anchored except celebration
 dy=([0,0,-1,-1,0,0][i] if state=='idle' else [0,-2,-4,-4,-2,0][i] if state=='celebrating' else 0)
 # draw character on separate layer, translate at end
 r(15,35,18,5,'o'); r(16,35,16,4,'pants'); r(16,39,7,4,'o'); r(25,39,7,4,'o'); r(17,39,5,2,'p2'); r(26,39,5,2,'p2'); r(14,41,9,4,'o'); r(25,41,9,4,'o'); r(15,42,7,2,'white'); r(26,42,7,2,'white'); r(15,44,7,1,'shoe'); r(26,44,7,1,'shoe')
 # sweater and arms
 p([(15,27),(32,27),(35,30),(35,37),(13,37),(13,30)],'o'); r(15,29,18,7,'shirt'); r(16,30,16,1,'s3'); r(15,35,18,1,'s2'); r(18,28,12,2,'s2')
 left='up' if state=='celebrating' or state=='idle' and i in (1,2,3) or state=='thinking' else 'down'
 right='up' if state=='celebrating' else 'down'
 arm(10,29,-1,left); arm(33,29,1,right)
 # head silhouette: wide rounded, cropped hair
 p([(17,4),(30,4),(30,5),(34,5),(34,7),(36,7),(36,10),(38,10),(38,16),(40,16),(40,22),(37,22),(37,25),(34,25),(34,27),(30,27),(30,29),(18,29),(18,27),(14,27),(14,25),(11,25),(11,22),(8,22),(8,16),(10,16),(10,10),(12,10),(12,7),(14,7),(14,5),(17,5)],'o')
 p([(17,6),(31,6),(31,7),(34,7),(34,9),(36,9),(36,16),(12,16),(12,10),(14,10),(14,8),(17,8)],'hair')
 r(18,6,4,1,'h2'); r(25,7,5,1,'h2'); r(14,9,3,1,'h2'); r(32,9,2,1,'h2'); r(22,8,2,1,'h2')
 # face and ears
 p([(15,10),(32,10),(32,12),(35,12),(35,17),(36,17),(36,22),(33,25),(29,27),(19,27),(15,25),(12,22),(12,17),(13,17),(13,12),(15,12)],'skin')
 r(9,17,3,4,'shade'); r(10,17,1,3,'light'); r(37,17,2,4,'shade'); r(37,17,1,3,'light')
 r(15,12,18,1,'light'); r(14,13,1,3,'light'); r(33,13,1,3,'shade')
 # brows and eyes
 r(15,14,5,1,'o'); r(28,14,5,1,'o')
 closed=state=='sleeping' or state=='idle' and i==5
 if closed:
  r(15,17,5,1,'o'); r(28,17,5,1,'o')
 else:
  r(14,15,6,4,'white'); r(28,15,6,4,'white'); r(17,15,3,4,'o'); r(28,15,3,4,'o'); r(17,15,1,1,'white'); r(29,15,1,1,'white')
 r(22,18,4,1,'shade'); r(23,17,2,1,'light')
 # beard/moustache, grin
 p([(12,20),(14,20),(14,22),(17,23),(19,21),(21,20),(27,20),(29,21),(31,23),(34,22),(34,20),(36,20),(36,23),(33,26),(29,28),(19,28),(15,26),(12,23)],'beard')
 r(16,24,2,1,'b2'); r(19,26,10,1,'b2'); r(30,24,2,1,'b2')
 if state=='sleeping': r(22,23,4,1,'skin')
 elif state=='thinking': r(22,22,5,1,'skin'); r(24,23,3,1,'light')
 else:
  r(19,22,10,3,'o'); r(20,22,8,1,'white'); r(21,23,6,1,'white'); r(22,24,4,1,'skin')
 # overlay props after head and body
 if state=='coding':
  r(13,29,22,11,'o'); r(14,30,20,9,'laptop'); r(15,31,18,7,'screen'); r(12,39,24,2,'o'); r(13,39,22,1,'laptop'); r(23,33,2,2,'purple'); r(15+(i%3)*5,36,3,1,'purple'); r(10,34,4,3,'skin'); r(34,34,4,3,'skin')
 if state=='thinking':
  r(10,22,3,5,'o'); r(11,23,2,3,'skin'); r(10,26,4,2,'shirt')
 if state=='recharging':
  y=28 if i in (2,3) else 32
  r(30,y,10,8,'o'); r(31,y+1,6,6,'coffee'); r(37,y+2,3,4,'coffee'); r(37,y+3,2,2,'o'); r(32,y+1,4,1,'shade'); r(31,y+6,4,1,'shoe'); r(28,y+5,4,3,'skin')
 if dy: 
  moved=Image.new('RGBA',(48,48)); moved.paste(im,(0,dy)); im=moved; d=ImageDraw.Draw(im)
 if state=='idle' and i in (1,2,3): star(6,25,'gold')
 if state=='celebrating':
  star(5,10+(i%3),'gold'); star(42,18-(i%3),'gold'); r(7,3,2,2,'purple'); r(40,5,2,2,'purple')
 if state=='thinking':
  # pixel question mark
  y=2-(i%2); r(40,y,5,1,'purple'); r(44,y+1,1,3,'purple'); r(42,y+3,3,1,'purple'); r(42,y+4,1,2,'purple'); r(42,y+7,1,1,'purple')
 if state=='recharging':
  y=22-(i%3); r(33,y,1,3,'coffee'); r(35,y-2,1,3,'coffee')
 if state=='sleeping':
  for x,y in [(39,10-(i%3)),(43,4-(i%2))]:
   r(x,y,4,1,'purple'); r(x+2,y+1,1,1,'purple'); r(x+1,y+2,1,1,'purple'); r(x,y+3,4,1,'purple')
 return im
states=['idle','coding','thinking','celebrating','recharging','sleeping']
for state in states:
 sheet=Image.new('RGBA',(48*6,48)); frames=[sprite(state,i) for i in range(6)]
 for i,frame in enumerate(frames):sheet.paste(frame,(48*i,0))
 sheet.save(P/f'{state}.png',optimize=True)
# large contact sheet for verification
preview=Image.new('RGB',(48*6,48*6),'#f3ede6')
for j,state in enumerate(states):
 for i in range(6):
  f=sprite(state,i);preview.paste(f,(i*48,j*48),f)
preview.resize((1152,1152),Image.Resampling.NEAREST).save(Path(__file__).parent/'sprite-preview.png')
