'''
500x500km crater simulation project, with uniform impactor size (nonUniform size)

Written by:
    Kyle Crabb
    Tarek Mackler
'''

import numpy as np
import matplotlib.pyplot as pl
import time

# -- Needed to time our simulation -- #
start = time.time()

# -- Create a 500x500x4 matrix to be used for our crater map -- #
image = np.zeros([500, 500, 4])

def genCratersize():
    """
        Generate the size of a crater. This produce a logarithmic distribution,
        that is the distribution should be linear in log-log space.
        Inputs:
            none
        Returns:
            cratersize: 
                integer; the size of a crater
    """
    # - Generate which 'bucket' we will pull the value from - #
    bucket = np.random.logseries(0.8)

    # - Generate a random number in the bucket - #
    cratersize = int(np.random.uniform(10*bucket, 20*bucket))
    return cratersize

def drawCircle(image, radius, origin, unique):
    """
        This function will take paramaters and use them to draw a filled
        circle onto an image.
        Courtesy of:
            http://stackoverflow.com/questions/39862709/generate-coordinates-in-grid-that-lie-within-a-circle
        Inputs:
            image:
                The image array to draw on
            radius:
                The radius of the circle
            origin:
                The point to use as the center of the circle
            unique:
                A value used to keep track of how many circles have been drawn 
                later on in the simulation
        Returns:
            image:
                Returns an array of the same dimensions as the input image
                with a filled circle drawn on it
    """

    # - Set the width of the circle in the +x direction to the radius - #
    xlim = int(radius)

    # -- Code to draw the circle -- #
    for i in range(origin[0] - xlim, origin[0] + (xlim + 1)):
        # - If we would draw outside of our image array, skip the iteration - #
        if (i > 499) or (i < 0):
            continue
        # - Calculate how we will draw the crater in the -+y direction from the
        #   origin - #
        drawCalc = (radius * radius) - ((i-origin[0]) * (i-origin[0]))
        if drawCalc < 0:
            ylim = -int(( -drawCalc) ** .5)
        else:
            ylim = int( drawCalc ** .5)
        # - This loop actually draws the circle - #
        for j in range(origin[1] - ylim, origin[1] + (ylim + 1)):
            if (j > 499) or (j < 0):
                continue
            image[i][j][0] = unique
            image[i][j][1] = unique
            image[i][j][2] = unique
            image[i][j][3] = 1

    return(image)

def simImpacts(blankimage):
    """
    Takes a blank immage array and draws craters until we hit "saturation"
    Inputs:
        blankimage:
            3D array in shape: [x-coordinates][y-coordinates][RGBA array]
    Returns:
        cratermap:
            3D array of same shape as blank image, with craters drawn
        count:
            how many total impacts we have had
        uniquelist:
            A list of unique RGB values in the array
        cratersatstep:
            An array of how many craters were visible at each iteration
    """

    # - Init Vars - #
    count = 0
    unique = .001
    uniquelist = []
    cratersatstep = []
    cratermap = blankimage

    # -- Loop until saturation -- #
    while True:
        # - Wait until we have had at least 10000 impacts - #
        if len(cratersatstep) > 10000:
            # - We calculate average by comparing the average of the last 1000
            #   to the average of the last 100 - #
            smallAvg = np.average(cratersatstep[-100:])
            bigAvg = np.average(cratersatstep[-1000:])
            # - If we have reached saturation we can leave the loop - #
            if abs( smallAvg - bigAvg ) < (bigAvg * (1 - 0.99)):
                return cratermap, count, uniquelist, cratersatstep

        # - Save an image every 1000 impacts - #
        if count%1000 == 0:
            pl.imshow(image)
            pl.title('Nonuniform Craters after '+str(int(count))+' Impactors')
            pl.savefig('../images/NonUniform'+str(int(count/1000))+'.png')
            pl.clf()

        # - Get a size of the crater - #
        impactsize = genCratersize()

        # - If the crater we got is less than 10km, skip this iteration - #
        if impactsize < 10:
            continue
        # - Increment our impactors - #
        count += 1

        # -- Generate the location for the center of the crater -- #
        x = int(np.random.rand()*500.)
        y = int(np.random.rand()*500.)

        # - Pass variables to the draw function - #
        cratermap = drawCircle(cratermap, int(impactsize / 2.), [x,y], unique)
        # - Get how many craters we have visible - #
        uniquelist = np.unique(cratermap[:,:,0])
        # - Keep track of how many craters are visible at each step - #
        cratersatstep.append(len(uniquelist))

        # - Keep unique value unique - #
        unique += .001

    return cratermap, count, uniquelist, cratersatstep

# - SIMULATE - #
image, totalcount, visible, cratercount = simImpacts(blankimage=image)

total = time.time() - start

# - Give the user pertinent information - #
print("""We have %i visible craters.
Our area saw %i impactors.
This equates to %.2e years taken to reach saturation.

This simulation took %f seconds to run.""" %(len(visible), totalcount, totalcount*1000, total))

# - Generate a saturated image - #
pl.imshow(image)
pl.title('Craters at Saturation')
pl.savefig('../images/NonUniformSaturation.png')
pl.clf()

# - Plot how many craters are visible at each time step - #
pl.scatter(np.linspace(0,len(cratercount), len(cratercount)), cratercount)
pl.xlabel('Time (x1000)')
pl.ylabel('Visible Craters')
pl.title('Visible Craters vs Time (NonUniform)')
pl.savefig('../images/VisibleCratersvsTimeNonUniform.png')
