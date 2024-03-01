import matplotlib.pyplot as plot
import numpy as np

pitchDiameter = 6
rollerDiameter = .75
noOfRollers = 6


pi = np.pi
rollerRadius = rollerDiameter / 2
pitchRadius = pitchDiameter/2
pitchCircumference = pitchDiameter * pi
rollerCircumference = rollerDiameter * pi


#Get X/Y Values for basic seed curve
rotationAngle = np.arange(0, 2*pi, 0.1)
xValue1 = (pitchRadius * (rotationAngle - np.sin(rotationAngle)))
yValue1 = pitchRadius * (1 - np.cos(rotationAngle))
# Plot the basic seed curve
plot.plot(xValue1, yValue1)

xIntercept1 = (pitchCircumference/noOfRollers)/2
#yIntercept = (xIntercept*(1-np.cos(rotationAngle))*pitchRadius)#/(rotationAngle-pi(rotationAngle))
#formula above needs a specific angle of rotation. figure out how to calculate the angle of rotation at which


xValue2 = -xValue1 + (pitchCircumference/noOfRollers)
yValue2 = pitchRadius * (1 - np.cos(rotationAngle))
plot.plot(xValue2, yValue2)

xValue3 = [xIntercept1,xIntercept1]
yValue3 = [0,6]
plot.plot(xValue3,yValue3)











#plot.xlim(-pi, 5 * pitchRadius * pi)
plot.xlim(-pitchCircumference,pitchCircumference+1)
plot.ylim(-1, pitchRadius * 3)
plot.gca().set_aspect('equal', adjustable='box')

plot.title('Cycloid Rack Profile')

plot.grid(True, which='both')

plot.axhline(y=0, color='k')

plot.show()

# Display the sine wave

plot.show()