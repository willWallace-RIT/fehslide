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
thread =int(sys.argv[6])
threadstr=""
if(thread==1):
    threadstr="-limit threads 1 "
morph = 0.0
theta = random.random()*math.pi*2
vec = np.array([math.cos(theta),math.sin(theta)])
max = 100//int(sys.argv[3])

ratio=1920.0/1080.0
transitionResHeight=int(sys.argv[5])
transitionRes=str(int(transitionResHeight*ratio))+"x"+str(transitionResHeight)

scale = (transitionResHeight*(30.0/426))/100.0
ogVec = (100*scale*vec)
pipe1cmd = "mktemp"
pipe2cmd = "mktemp"
tempStr1= sb.check_output(pipe1cmd,shell=True).decode('utf-8').replace('\n','')

tempStr2= sb.check_output(pipe2cmd,shell=True).decode('utf-8').replace('\n','')
images = []
qual1cmd="gm convert "+threadstr+"\"" +path1+"\" -quality 100 -geometry "+transitionRes+"! "+ tempStr1 +"| gm convert "+threadstr+"\"" +path2+"\" -quality 100 -geometry "+transitionRes+"! "+ tempStr2


qualStart1 = sb.run(qual1cmd,stdout=sb.PIPE,stderr=sb.PIPE,shell=True).stdout
#qualStart2 = sb.run(qual2cmd,stdout=sb.PIPE,stderr=sb.PIPE,shell=True).stdout


for i in range(0,max,1):
    
    pos = ogVec-(scale*morph*vec)
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
    #cmdUnsplit = "gm convert - -matte -operator Opacity Assign "+ str(100-morph)+"%  png:-"
    cmd2nd = "gm composite "+threadstr+"-geometry "+signx+str(abs(int(pos[0])))+signy+str(abs(int(pos[1])))+" "+tempStr2+" "+tempStr1+"  -dissolve "+str(int(morph))+" png:-"
    #cmd2nd = "gm composite "+tempStr2+" "+tempStr1+"  -dissolve "+str(int(morph))+" png:-"
    cmd3rd = "gm convert "+threadstr+"- -crop "+transitionRes+" png:-"
    #cmd1 = shlex.split(cmdUnsplit)
    #cmd1[2]=path1
    #cmd1[4]=path2
    cmd1 =cmd2nd
    print(cmd1)
    
    imagebuffer = sb.run(cmd1,stdout=sb.PIPE,stderr=sb.PIPE,input=qualStart1,check=True,shell=True).stdout
    #imagebuffer = sb.run(cmd2nd,stdout=sb.PIPE,stderr=sb.PIPE,input=imagebuffer,check=True,shell=True).stdout
    
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

cmd3 = "rm "+tempStr1
sb.run(cmd3,stdout=sb.PIPE,stderr=sb.PIPE,shell=True)
cmd3 = "rm "+tempStr2
sb.run(cmd3,stdout=sb.PIPE,stderr=sb.PIPE,shell=True)

