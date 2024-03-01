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

class cycloidRP():

    def __init__(self, pitchDiameter=6, rollerDiameter=1, noOfRollers=6, noOfTeeth=8, webThickness=2,xOffset=0, yOffset=0):
        # Variable Parameters to be input
        self.pitchDiameter = pitchDiameter  # Diameter of the rolling circle
        self.rollerDiameter = rollerDiameter  # Diameter of a smaller circle centered on the focal point of the rolling circle
        self.noOfRollers = noOfRollers  # number of rollers (teeth) in pinion
        self.noOfTeeth = noOfTeeth  # desired number of teeth in rack assembly
        self.webThickness = webThickness  # distance from center of roller at lowest point, and bottom edge of rack
        self.yOffset = yOffset
        self.xOffset = xOffset
        # constants (DON'T CHANGE)
        self.pi = np.pi
        # calculated variables (DON'T CHANGE)
        self.rollerRadius = self.rollerDiameter / 2
        self.pitchRadius = self.pitchDiameter / 2
        self.pitchCircumference = self.pitchDiameter * self.pi
        self.rollerCircumference = self.rollerDiameter * self.pi

    def createCircle(self, radius=1, center = [0,0], start = 0, end = 360, inchResolution = .1,color='k'):
        # convert degrees to radians
        start = np.radians(start)
        end = np.radians(end)
        # estabish a list to contain the angles for which we're about to generate X & Y values
        rads = []
        # estabish 2 lists to contain the X & Y values we're about to generate

        xCoords = []
        yCoords = []
        # calculate the angular resolution needed to achieve the desired resolution in inches, given the circle dimensions
        # Triangle math for an acute isosceles triangle with 2 sides equal to the radius and the 3rd side equal to the
        #   inch resolution
        # https://www.calculator.net/triangle-calculator.html?vc=&vx=.001&vy=1&va=&vz=1&vb=&angleunits=d&x=79&y=23
        a = radius
        b = inchResolution
        c = radius
        B = np.arccos(((a**2)+(c**2)-(b**2))/(2*a*c)) # angle between line segments from center of circle
        angularResolution = B
        noOfSegments = int((end-start)/angularResolution)
        # calculate X & Y values:
        # https://www.google.com/search?q=equation+of+a+circle+in+python&rlz=1C1CHBF_enUS867US867&oq=equation+of+a+circle+in+py&aqs=chrome.1.69i57j0.7983j0j7&sourceid=chrome&ie=UTF-8#kpvalbx=_oyNZXvrADdesytMPldqq6AQ19
        t = np.linspace(start,end,noOfSegments+1) # this creates a numpy array which henceforth appears to be a single variable
        x = radius*np.cos(t)+center[0] + self.xOffset# This is a numpy function, acting on a numpy array, wh
        y = radius*np.sin(t)+center[1] + self.yOffset
        plot.plot(x, y,color)
        return (x,y)

    def createPinion(self,rotationDegrees=10, color = 'k'):
        # calculate rotational offset of pinion
        rotationRads = np.radians(-rotationDegrees) # pinion simulated to roll to the right, clockwise, so rotationDegress are inverted
        rollerAngles = np.linspace(0, 2*np.pi, self.noOfRollers+1) + rotationRads
        # calculate linear offset of Pinion based on rotational offset
        pinionCenterX = (rotationDegrees/360)*self.pitchCircumference
        pinionCenterY = self.pitchRadius

        # Create low-res (36 sides) representative pitch circle
        #self.createCircle(radius=self.pitchRadius,
                          #center=[pinionCenterX, pinionCenterY],
                          #start=0+rotationDegrees,
                          #end=360+rotationDegrees,
                          #inchResolution=self.pitchCircumference / 35)
        # Create low-res (36 sides) representative roller circle
        for i in range (0,self.noOfRollers):
            x = self.pitchRadius * np.cos(rollerAngles[i])+pinionCenterX
            y = self.pitchRadius * np.sin(rollerAngles[i])+pinionCenterY
            if i == 0:
                linecolor = 'b'
            else:
                linecolor = color
            self.createCircle(radius=self.rollerRadius,
                              center=[x, y],
                              start=0,
                              end=360,
                              inchResolution=self.rollerCircumference/35,
                              color=linecolor)



if __name__ == "__main__":

    myCycloid = cycloidRP(pitchDiameter=6, rollerDiameter=1,noOfRollers=6,yOffset=0.5)#,xOffset=-np.pi*(9/6))
    for i in range (0,360):
        myCycloid.createPinion(rotationDegrees=i,color='k')



    #myCycloid.createCircle(radius=myCycloid.rollerRadius, center=[0, 0], start=0, end=360)
    #myCircleX, myCircleY = myCycloid.createCircle(radius=3, center=[0,3], start=0, end=360)
    plot.axis("equal")
    plot.grid()
    #plot.plot(myCircleX,myCircleY)
    plot.show()
