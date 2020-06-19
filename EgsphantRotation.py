##############################################
#   Author: Katerina Chytra                  #   
#   Last update: 28/8/2018                   #
##############################################
# coding= utf-8
import numpy as np
#file = input('Egsphant filename to rotate (without '.egsphant'):') 
#file='phant_to_rotate'
#file='new'
file='Rudolf_head.header'
f = open('{file:s}.egsphant'.format(file=file), 'r')
angle = int(input('Set the angle: '))
while np.mod(angle,abs(90)) != 0:
      print('Wrong angle. Only multiples of 90 are allowed.')
      angle = int(input('Set the angle:'))
      
plane = input('Set the plane (xy,zx,zy): ')
while plane!='xy' and plane!='zx' and plane!='zy':
    print('Wrong plane input.')
    plane = input('Set the plane (xy,zx,zy):')

#LOAD STRINGS FROM FILE----------------
lines = f.readlines()
matNumS = lines[0]
matNum = int(matNumS)
materials = lines[1:matNum+1]
lineNum = matNum+1
dummy = lines[lineNum]
cells = list(lines[lineNum+1].split())
nx,ny,nz = (int(cells[i]) for i in range(3)) 
VoxelBounds = lines[lineNum+2:lineNum+5]
xBounds,yBounds,zBounds = (VoxelBounds[i] for i in range(3))
lineNum = lineNum+5
phanMatLoad = lines[lineNum:lineNum+nz*(ny+1)-1] #phanMatLoad = lines[9:43]; nz-1 = num of \n
lineNum = lineNum+nz*(ny+1)
phanDensLoad = lines[lineNum:lineNum+nz*(ny+1)-1]
#---------------------------------------
#--
def CleanPhanLoad(phanLoad):
    for i in range (len(phanLoad)):   #remove \n from strings
        phanLoad[i] = phanLoad[i].strip()
    phanLoad = list(filter(None,phanLoad)) #remove empty elements and '\n' 
    return phanLoad  
#--
phanMatLoad = CleanPhanLoad(phanMatLoad)
phanDensLoad = CleanPhanLoad(phanDensLoad)
phanMatLoad = np.reshape(phanMatLoad,(nz,ny)) #(nz,ny)) #type(phanMatLoad) = array
phanDensLoad = list(phanDensLoad[i].split() for i in range(len(phanDensLoad)))
phanDens = np.reshape(phanDensLoad,(nz,ny,nx))
#---
#EACH STRING INTO SEPARATE MATERIAL---------------------------------------
row,slice,phanMat = ([] for i in range(3))   
for i in range(nz): 
    for j in range(ny): 
        s = phanMatLoad[i,j]
        for k in range(len(s)):   
                row.append(s[k])
        slice.append(row)  
        row=[]
    phanMat.append(slice)
    slice = []
phanMat = np.reshape(phanMat,(nz,ny,nx))  
#ROTATION-----------------------------------------------------------------
#---initialization of  BoundsRot--
xBoundsRot = xBounds
yBoundsRot = yBounds
zBoundsRot = zBounds
angleModulo=np.mod(angle/90,2)
#(0,1)=(z,y); (0,2)=(z,x); (2,1)=(x,y)
if plane == 'xy': 
    A = (2,1)
    if angleModulo!=0: 
        xBoundsRot = yBounds
        yBoundsRot = xBounds		
elif plane == 'zy':
    A = (0,1)
    if angleModulo!=0: 
        yBoundsRot = zBounds
        zBoundsRot = yBounds	    
elif plane == 'zx':
    A = (0,2)   
    if angleModulo!=0: 
         xBoundsRot = zBounds
         zBoundsRot = xBounds	   
if abs(angle) == 90: n = 1  
elif abs(angle) == 180: n = 2
elif abs(angle) == 270: n = 3
if angle < 0: n = -n

phanMatRot = np.rot90(phanMat,n,A)
phanDensRot = np.rot90(phanDens,n,A) 
 
rz,ry,rx =(phanMatRot.shape[i] for i in range(3)) 
spaces=' ' * 3 
cellsRot=spaces+str(rx)+spaces+str(ry)+spaces+str(rz)
VoxelBoundsRot=[]
VoxelBoundsRot.append(xBoundsRot)  
VoxelBoundsRot.append(yBoundsRot)
VoxelBoundsRot.append(zBoundsRot)

#Write In NEW .EGSPHANT FILE------------------------------
file2 = '{file:s}{angle:d}{plane:s}.egsphant'.format(file = file, angle=angle, plane=plane)
with open(file2, 'w') as f2:
    f2.write(matNumS+''.join(materials)+dummy+cellsRot+'\n'+''.join(VoxelBoundsRot))
    for i in range(rz):
        for j in range(ry):
            f2.write(''.join(phanMatRot[i,j,:])+'\n')
        f2.write('\n')
         
    for i in range(rz):
        for j in range(ry):
            pDR = phanDensRot[i,j,:]
            k=0
            f2.write(' '*3)
            while k < rx:
                f2.write(pDR[k]+' '*(26-len(pDR[k]))) 
                k+=1
            f2.write('\n')
        f2.write(''+'\n')
f.close()
f2.close()
print('Lets check {file:s}{angle:d}{plane:s}.egsphant if the phantom has been rotated correctly.'.format(file = file, angle=angle, plane=plane))