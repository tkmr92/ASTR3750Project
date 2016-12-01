import numpy as np
import matplotlib.pyplot as pl
import time

# -- Needed to timr our simulation -- #
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
        # - Calculate which how we will draw the y+- part of the circle - #
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
                # print(smallAvg)
                # print(bigAvg)
                return cratermap, count, uniquelist, cratersatstep
        impactsize = 10

        count += 1
        # if count == 100:
        #     return cratermap, count #, uniquelist, cratersvisible
        if count%1000 == 0:
            pl.imshow(image)
            pl.savefig('Uniform'+str(count/1000)+'.png')
            pl.clf()
        #  - This should only examine the 3rd index of our image array
        #    which is itself an array of rgba values for that particular
        #    pixel. If each pixel is not empty, that is if the values in
        #    our rgba are nonzero, then we have reached saturation and can
        #    break from the loop - #

        # -- Generate the location for the center of the crater -- #
        x = int(np.random.rand()*500.)
        y = int(np.random.rand()*500.)

        # -- Generate and draw a crater for our impact -- #
        # - *10 here to make sure that our crater sizes are (mostly) above 10km - #
        cratermap = drawCircle(cratermap, int(impactsize / 2.), [x,y], unique)
        uniquelist = np.unique(cratermap[:,:,0])
        cratersatstep.append(len(uniquelist))
        unique += .001
        # cratersvisible.append(len(uniquelist))

        
        # print("Total craters: %i  Visible craters: %i" %(count, len(uniquelist)))
    return cratermap, count , uniquelist, cratersvisible

image, totalcount, visible, cratercount = simImpacts(blankimage=image)

total = time.time() - start

print("""We have %i visible craters.
Our area saw %i impacters.
This equates to %.2e years taken to reach saturation.

This simulation took %f seconds to run.""" %(len(visible), totalcount, totalcount*1000, total))


# normalize=np.max(image[:][:][0:2])
# image[:][:][0:2] = image[:][:][0:2] / normalize
pl.imshow(image)
pl.savefig("uniformSaturation.png")
pl.clf()

pl.scatter(np.linspace(0,len(cratercount), len(cratercount)), cratercount)
pl.xlabel('Time')
pl.ylabel('# Craters Visible')
pl.title('Visible Craters vs Time')
pl.savefig('VisiblecratersvstimeUniform.png')
