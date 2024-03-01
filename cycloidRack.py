#TODO:
# Create a "resolution" function to increase divisions of pi.
#   -Or better yet, have it define somehow define distance between points, so that there is some uniformity in the
#       arcs. (as it stands, distance between points starts expanding as Y dimension increases)
# Implement better version of cycloid tangent function from Tesla23 on AAC
# create pinion circle representation from input parameters
# Create optional viewing of roller paths
# create a GUI
# investigate possible meshing tolerance variable per Winegrower on hobby-machinist
# option to include semicircle ends of rack for MFG in sections butted together
# investigate possible need for units (mm/inches)
# recapture the pointed crown of the tooth by stopping the spline/polyline exactly at the x-intercept instead
#   of at some point near it
# Have the code generate splines and arcs instead of polylines, then "flatten" (per cmartinez on AAC) if such function
#   is available in ezdxf

import matplotlib.pyplot as plot
import numpy as np
#import csv
import ezdxf

# Variable Parameters to be input
pitchDiameter = 90 # Diameter of the rolling circle
rollerDiameter = 22 # Diameter of a smaller circle centered on the focal point of the rolling circle
noOfRollers = 7 # number of rollers (teeth) in pinion
noOfTeeth = 14 # desired number of teeth in rack assembly
webThickness = 10 # distance from center of roller at lowest point, and bottom edge of rack


# Variable Parameters to be input
pitchDiameter = 27 # Diameter of the rolling circle
rollerDiameter = 2 # Diameter of a smaller circle centered on the focal point of the rolling circle
noOfRollers = 12 # number of rollers (teeth) in pinion
noOfTeeth = 12 # desired number of teeth in rack assembly
webThickness = 10 # distance from center of roller at lowest point, and bottom edge of rack

# constants (DON'T CHANGE)
pi = np.pi
# calculated variables (DON'T CHANGE)
rollerRadius = rollerDiameter / 2
pitchRadius = pitchDiameter/2
pitchCircumference = pitchDiameter * pi
rollerCircumference = rollerDiameter * pi

# create lists of X&Y values for the final rack tooth profile. We will add to these lists at various points along the process.
finalXvalues = []
finalYvalues = []

# this is a vertical line where the positive and the negative cycloids converge
xIntercept = (pitchCircumference/noOfRollers)/2
plot.plot([xIntercept,xIntercept],[0,10], '--')




# Get X/Y Values for basic cycloid curve
# create a numpy array containing radian values of a complete revolution of the circle in increments of .1
rotationAngle = np.arange(0, 2*pi, 0.1)
#print(rotationAngle)
xValuesA = (pitchRadius * (rotationAngle - np.sin(rotationAngle))) # create a numpy array containing x values of the cycloid
yValuesA = pitchRadius * (1 - np.cos(rotationAngle))# create a numpy array containing y values of the cycloid
# Plot the basic cycloid curve
plot.plot(xValuesA, yValuesA, '--') # draw a dashed line for visual reference only

# second cycloid is offset in the X axis by the period of the roller interval and in the negative direction
def offsetSecondCycloid(input):
    return -input + (pitchCircumference / noOfRollers)
xValuesB = offsetSecondCycloid(xValuesA)
yValuesB = yValuesA
plot.plot(xValuesB, yValuesB, '--') # draw a dashed line for visual reference only

# Create 2 lists to contain the x & y values of the inner offset curve.
innerXvaluesA = []
innerYvaluesA = []
outerXvaluesA = []
outerYvaluesA = []
innerXvaluesB = []
innerYvaluesB = []
outerXvaluesB = []
outerYvaluesB = []
# cycle through all values of rotation angles and find the equations of the line segments which make up the cycloid
for i in range (0,len(rotationAngle)-1):
    # Find equation of the line between this point and the next point
    X1A, Y1A = xValuesA[i], yValuesA[i] # this point
    X2A, Y2A = xValuesA[i + 1], yValuesA[i + 1] # next point
    M = (Y2A - Y1A) / (X2A - X1A) # Find the slope using the two points
    # we now have all the values for the y=mx+b equation which describes this segment of the cycloid curve
    # now we need to find a line perpendicular to this line segment and a point on that line a given distance away
    tangentSlope = np.arctan(1 / M)  # inverse slope (in radians) is the tangent of the cycloid
    if rotationAngle[i] < 3.1:
        innerX = X2A + np.cos(tangentSlope) * rollerRadius
        innerY = Y2A - np.sin(tangentSlope) * rollerRadius
        outerX = X2A - np.cos(tangentSlope) * rollerRadius
        outerY = Y2A + np.sin(tangentSlope) * rollerRadius
    else:
        innerX = X1A - np.cos(tangentSlope) * rollerRadius
        innerY = Y1A + np.sin(tangentSlope) * rollerRadius
        outerX = X2A + np.cos(tangentSlope) * rollerRadius
        outerY = Y2A - np.sin(tangentSlope) * rollerRadius
    innerXvaluesA.append(innerX)
    innerYvaluesA.append(innerY)
    outerXvaluesA.append(outerX)
    outerYvaluesA.append(outerY)
    innerXvaluesB.append(offsetSecondCycloid(innerX))
    innerYvaluesB.append(innerY)
    outerXvaluesB.append(offsetSecondCycloid(outerX))
    outerYvaluesB.append(outerY)

plot.plot(innerXvaluesA, innerYvaluesA, '--')
plot.plot(outerXvaluesA, outerYvaluesA,'--')
plot.plot(innerXvaluesB, innerYvaluesB,'--')
plot.plot(outerXvaluesB, outerYvaluesB,'--')
#finalXvalues.append(rollerRadius)# to correct a mesh/face issue caused by errant first vertice
#finalYvalues.append(0)
for i in range(0, len(innerYvaluesA)):
    if innerYvaluesA[i] > 0: # to correct a mesh/face issue caused by errant first vertice
        if innerXvaluesA[i] < xIntercept:
            finalXvalues.append(innerXvaluesA[i])
            finalYvalues.append(innerYvaluesA[i])
innerXvaluesB.reverse()
innerYvaluesB.reverse()
for i in range(len(innerYvaluesB)):
    if innerXvaluesB[i] > xIntercept:
        finalXvalues.append(innerXvaluesB[i])
        finalYvalues.append(innerYvaluesB[i])


# Plot a circle representing the roller, at the end of the first downward slope
# formula of a circle: (x-h)^2 + (y-k)^2 = r^2, where
# h,k is the center of the circle and r is the radius
# since the circle is centered at unk,0, it is simply:
# (x-h)^2 + y^2 = r^2
# Rearrange for X
# (x-h)^2 = r^2 - y^2
# x - h = sqrt(r^2 - y^2)
# x = sqrt(r^2 - y^2) + h
rollerCircleRadians = np.arange(0, 2*pi, 0.1)
rollerCircleXvalues = []
rollerCircleYvalues = []
h = (pitchCircumference / noOfRollers)
for i in range (0,len(rollerCircleRadians)):
    rollerCircleYvalues.append(np.sin(rollerCircleRadians[i]) * rollerRadius)
    n = rollerCircleRadians[i]
    if n >= 0 and n < 0.5*pi:
        rollerCircleXvalues.append(np.sqrt(rollerRadius**2 - rollerCircleYvalues[i]**2) + h)
    elif n >= 0.5*pi and n < 1.5* pi:
        rollerCircleXvalues.append(-np.sqrt(rollerRadius ** 2 - rollerCircleYvalues[i] ** 2) + h)
    else:
        rollerCircleXvalues.append(np.sqrt(rollerRadius ** 2 - rollerCircleYvalues[i] ** 2) + h)
    #print(rollerCircleRadians[i], rollerCircleXvalues[i],rollerCircleYvalues[i])
plot.plot(rollerCircleXvalues, rollerCircleYvalues, '--')

for i in range (0,len(rollerCircleRadians)):
    if rollerCircleRadians[i]>pi:
        finalXvalues.append(rollerCircleXvalues[i])
        finalYvalues.append(rollerCircleYvalues[i])


###################################################################################
######## DUPLICATE FINAL X & Y VALUES BY # OF ROLLERS##############################
###################################################################################

rackXcoords = []
rackYcoords = []
rackXcoords.append(rollerRadius)
rackYcoords.append(0)
for i in range (0,noOfTeeth):
    if i < noOfTeeth-1:
        for j in range(0,len(finalXvalues)):
            rackXcoords.append(finalXvalues[j]+((pitchCircumference/noOfRollers)*i))
            rackYcoords.append(finalYvalues[j])
    else:
        for j in range(0, len(finalXvalues)):
            if finalYvalues[j] >= 0:
                rackXcoords.append(finalXvalues[j] + ((pitchCircumference / noOfRollers) * i))
                rackYcoords.append(finalYvalues[j])
finalVertice = rackXcoords[len(rackXcoords)-1] # final X-value
#create a vertice straight down from final vertice
rackXcoords.append(finalVertice)
rackYcoords.append(-webThickness)
#create a vertice straight down from very first vertice
rackXcoords.append(rackXcoords[0])
rackYcoords.append(-webThickness)
#create one final vertice the same coordinates as the very first vertice to complete the shape
rackXcoords.append(rackXcoords[0])
rackYcoords.append(rackYcoords[0])


plot.plot(finalXvalues,finalYvalues)
plot.plot(rackXcoords,rackYcoords)

# Create a new DXF document.
doc = ezdxf.new(dxfversion='R2010')

# Create new table entries (layers, linetypes, text styles, ...).
#doc.layers.new('TEXTLAYER', dxfattribs={'color': 2})

# DXF entities (LINE, TEXT, ...) reside in a layout (modelspace,
# paperspace layout or block definition).
msp = doc.modelspace()
#points = (rackXcoords[0], rackYcoords[0])
points = []
for i in range (0,len(rackYcoords)):
    point = (rackXcoords[i], rackYcoords[i])
    print(point)
    points.append(point)
msp.add_lwpolyline(points)

# Save DXF document.
doc.saveas('test3.dxf')


plot.ylim(-3, pitchRadius * 3)
plot.xlim(-1)
plot.gca().set_aspect('equal', adjustable='box')

plot.title('Cycloid Rack Profile')

plot.grid(True, which='both')

plot.axhline(y=0, color='k')

plot.show()