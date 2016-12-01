import numpy as np
import matplotlib.pyplot as pl
import time
import sys

# -- Needed to timr our simulation -- #
start = time.time()

# -- Create a 500x500x4 matrix to be used for our crater map -- #
image = np.zeros([500, 500, 4])

def genCratersize():
    bucket = np.random.logseries(0.8)
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
        # - Calculate which  - #
        drawCalc = (radius * radius) - ((i-origin[0]) * (i-origin[0]))
        if drawCalc < 0:
            ylim = -int(( -drawCalc) ** .5)
        else:
            ylim = int( drawCalc ** .5)
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
    Inputs:
        blankimage
    Returns:
        cratermap:
        count:
        uniquelist:
    """

    count = 0
    unique = .001
    uniquelist = []
    cratersatstep = []
    cratermap = blankimage
    while True:
        if len(cratersatstep) > 10000:
            smallAvg = np.average(cratersatstep[-100:])
            bigAvg = np.average(cratersatstep[-1000:])
            if abs( smallAvg - bigAvg ) < (bigAvg * (1 - 0.99)):
                return cratermap, count, uniquelist, cratersatstep

        if count%1000 == 0:
            pl.imshow(image)
            pl.savefig('NonUniform'+str(count/1000)+'.png')
            pl.clf()

        impactsize = genCratersize()

        if impactsize < 10:
            continue
        count += 1

        # -- Generate the location for the center of the crater -- #
        x = int(np.random.rand()*500.)
        y = int(np.random.rand()*500.)

        cratermap = drawCircle(cratermap, int(impactsize / 2.), [x,y], unique)
        uniquelist = np.unique(cratermap[:,:,0])
        cratersatstep.append(len(uniquelist))

        unique += .001

    return cratermap, count, uniquelist, cratersatstep

image, totalcount, visible, cratercount = simImpacts(blankimage=image)

total = time.time() - start

print("""We have %i visible craters.
Our area saw %i impactors.
This equates to %.2e years taken to reach saturation.

This simulation took %f seconds to run.""" %(len(visible), totalcount, totalcount*1000, total))

pl.imshow(image)
pl.savefig('NonUniformSaturation.png')
pl.clf()

pl.scatter(np.linspace(0,len(cratercount), len(cratercount)), cratercount)
pl.xlabel('Time')
pl.ylabel('Visible Craters')
pl.title('Visible Craters vs Time')
pl.savefig('VisibleCratersvsTimeNonUniform.png')
