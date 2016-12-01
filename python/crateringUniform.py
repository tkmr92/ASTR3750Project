'''
500x500km crater simulation project, with uniform impactor size (10km radius craters)

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
        if (i > (len(image) - 1)) or (i < 1):
            continue
        # - Calculate how we will draw the y+- part of the circle - #
        drawCalc = (radius * radius) - ((i-origin[0]) * (i-origin[0]))
        if drawCalc < 0:
            ylim = -int(( -drawCalc) ** .5)
        else:
            ylim = int( drawCalc ** .5)
        # - Draw the circle - #
        for j in range(origin[1] - ylim, origin[1] + (ylim + 1)):
            # - If we are outside of our image, skip to next iteration - #
            if (j > (len(image) - 1)) or (j < 1):
                continue
            image[i][j][0] = unique
            image[i][j][1] = unique
            image[i][j][2] = unique
            image[i][j][3] = 1

    return(image)

def simImpacts(blankimage):
    """
        Takes a blank image array and draws craters on it until every pixel
        of the image is filled with a crater
    Inputs:
        blankimage:
            3-D array, where dimensions 1 and 2 are the size of the image.
            3rd dimension must be an RGBA array
    Returns:
        cratermap:
            3-D array of similar description to blankimage, saturated with 'craters'
        count:
            The amount of impactors that hit our 'surface'
        uniquelist:
            A list of unique values (used to identify unique craters)
        cratersvisible:
            An array of how many craters were visible at each timestep
    """

    # - Initialize variables - #
    count = 0
    unique = .001
    uniquelist = []
    cratersatstep = []
    cratermap = blankimage

    # -- Loop until saturation -- #
    while True:
        # - Wait until we have at least 10000 iterations before checking if we
        #   have reached saturation - #
        if len(cratersatstep) > 10000:
            # - We calculate average by comparing the average of the last 1000
            #   to the average of the last 100 - #
            smallAvg = np.average(cratersatstep[-100:])
            bigAvg = np.average(cratersatstep[-1000:])
            # - If we have reached saturation we can leave the loop - #
            if abs( smallAvg - bigAvg ) < (bigAvg * (1 - 0.99)):
                return cratermap, count, uniquelist, cratersatstep

        # - Every 1000 impacts we should save an image so we can compare - #
        if count%1000 == 0:
            pl.imshow(image)
            pl.title('Uniform Craters after '+str(int(count))+' Impactors')
            pl.savefig('../images/Uniform'+str(int(count/1000))+'.png')
            pl.clf()

        # --- BEGIN SIMULATION CODE --- #
        # - Increment our impactor count - #
        count += 1

        # - Generate the location for the center of the crater - #
        x = int(np.random.rand()*500.)
        y = int(np.random.rand()*500.)

        # - All of our impactors are the same size since this is our uniform sim - #
        impactsize = 10

        # - Pass our image array, the impact size (divided by 2 for radius)
        #   origin of the impact, and a unique color value to drawCircle function - #
        cratermap = drawCircle(cratermap, int(impactsize / 2.), [x,y], unique)
        # - Get all of the unique color values still in cratermap - #
        uniquelist = np.unique(cratermap[:,:,0])
        # - Keep track of how many craters we can see at each step of the loop - #
        cratersatstep.append(len(uniquelist))

        # - Add to our unique value to keep it unique! - #
        unique += .001
        
    return cratermap, count , uniquelist, cratersvisible


# - SIMULATE - #
image, totalcount, visible, cratercount = simImpacts(blankimage=image)

# - Calculate how long it took to run the simulation - #
total = time.time() - start

# - Tell the user the pertinent info - #
print("""We have %i visible craters.
Our area saw %i impacters.
This equates to %.2e years taken to reach saturation.

This simulation took %f seconds to run.""" %(len(visible), totalcount, totalcount*1000, total))

# - Save our final crater image - #
pl.imshow(image)
pl.savefig("../images/uniformSaturation.png")
pl.title('Craters at Saturation')
pl.clf()

# - Generate a plot of how many craters we have visible at each step in time - #
pl.scatter(np.linspace(0,len(cratercount), len(cratercount)), cratercount)
pl.xlabel('Time')
pl.ylabel('Visible Craters')
pl.title('Visible Craters vs Time (Uniform)')
pl.savefig('../images/VisiblecratersvsTimeUniform.png')
