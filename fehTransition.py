import subprocess as sb
import sys
import io
import time
import shlex
import random
import math
import numpy as np
from PIL import Image
path1 = sys.argv[1]
path2 = sys.argv[2]
morph = 0.0
theta = random.random()*math.pi*2
vec = np.array([math.cos(theta),math.sin(theta)])
ogVec = 100*vec

max = 100//int(sys.argv[3])
images = []
qualcmd="gm convert \"" +path2+"\" -quality 50 -geometry 1920x1080! png:-"
imageStart = sb.run(qualcmd,stdout=sb.PIPE,stderr=sb.PIPE,check=True,shell=True).stdout

for i in range(0,max,1):
    
    pos = ogVec-(morph*vec)
    signx=""
    if(math.copysign(1,pos[0])<0):
        signx='-'
    else:
        signx='+'
    signy=""
    if(math.copysign(1,pos[1])<0):
        signy='-'
    else:
        signy='+'
    cmdUnsplit = "gm convert - -matte -operator Opacity Assign "+ str(100-morph)+"%  png:-"
    cmd2nd = "gm composite -geometry "+signx+str(abs(int(pos[0])))+signy+str(abs(int(pos[1])))+" - \""+path1+"\" png:-"
    cmd3rd = "gm convert - -crop 1920x1080 png:-"
    #cmd1 = shlex.split(cmdUnsplit)
    #cmd1[2]=path1
    #cmd1[4]=path2
    cmd1 =cmdUnsplit
    print(cmd1)
    
    imagebuffer = sb.run(cmd1,stdout=sb.PIPE,stderr=sb.PIPE,input=imageStart,check=True,shell=True).stdout
    imagebuffer = sb.run(cmd2nd,stdout=sb.PIPE,stderr=sb.PIPE,input=imagebuffer,check=True,shell=True).stdout
    
    imagebuffer = sb.run(cmd3rd,stdout=sb.PIPE,stderr=sb.PIPE,input=imagebuffer,check=True,shell=True).stdout
    #print(imagebuffer)
    images.append(io.BytesIO(imagebuffer))
    
    
    morph=morph+float(sys.argv[3])
for i in range(len(images)):
    print(i)
    cmd2 = "feh --bg-scale -"
    #file=io.BytesIO(b'')
    #images[i].save(file,"png")
    
    feh=sb.run(cmd2,input=images[i].getvalue(),shell=True)
    
    #feh.wait();
    time.sleep(float(sys.argv[4]))
cmd3 = "feh --bg-scale \""+path2+"\""
sb.run(cmd3,stdout=sb.PIPE,stderr=sb.PIPE,shell=True)

