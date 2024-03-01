import matplotlib.pyplot as plot
import numpy as np

pitchRadius = 1
rollerDiameter = .75
noOfRollers = 6



rollerRadius = rollerDiameter / 2
pitchCircumference = pitchRadius*2*np.pi


#Get X/Y Values for basic seed curve
rotationAngle = np.arange(0, 2*np.pi, 0.1)
xValue1 = (pitchRadius * (rotationAngle - np.sin(rotationAngle)))
yValue1 = pitchRadius * (1 - np.cos(rotationAngle))
# Plot the basic seed curve
plot.plot(xValue1, yValue1)

xIntercept = (pitchCircumference/noOfRollers)/2
#yIntercept = (xIntercept*(1-np.cos(rotationAngle))*pitchRadius)#/(rotationAngle-np.pi(rotationAngle))
#formula abone needs a specific angle of rotation. figure out how to calculate the angle of rotation at which


xValue2 = -xValue1 + (pitchCircumference/noOfRollers)
yValue2 = pitchRadius * (1 - np.cos(rotationAngle))
plot.plot(xValue2, yValue2)

xValue3 = [xIntercept,xIntercept]
yValue3 = [0,6]
plot.plot(xValue3,yValue3)
#xValue4 = [-10,10]
#yValue4 = [yIntercept,yIntercept]
#plot.plot(xValue4,yValue4)

#find intersection point:
for i in range(0,len(xValue1)):
    if xValue1[i] == xValue2[i]:
        print(yValue1[i])

#"""
for i in range (0, noOfRollers-1):
    xValue1 = xValue1 + (pitchCircumference/noOfRollers)
    yValue1 = pitchRadius * (1 - np.cos(rotationAngle))
    # Plot the basic seed curve
    plot.plot(xValue1, yValue1)
#"""

#xValueInner = (xValue * (1 - (RollerRadius/pitchRadius))) + (RollerRadius*np.pi)
#yValueInner = yValue * (1 - (RollerRadius/pitchRadius))
#plot.plot(xValueInner,yValueInner)






#plot.xlim(-np.pi, 5 * pitchRadius * np.pi)
plot.xlim(-pitchCircumference,pitchCircumference+1)
plot.ylim(-1, pitchRadius * 3)
plot.gca().set_aspect('equal', adjustable='box')

plot.title('Cycloid Rack Profile')

plot.grid(True, which='both')

plot.axhline(y=0, color='k')
#plot.axvline(x=rollerDiameter*2)

plot.show()

# Display the sine wave

plot.show()