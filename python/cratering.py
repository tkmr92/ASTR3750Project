import numpy as np
import matplotlib.pyplot as pl
import time

start = time.time()
	# Used to test how long the program runs.

image = np.zeros([500, 500, 4])
	# Create a 500 x 500 x 4 'matrix' for image.

def drawCircle(image, radius, origin):
    """
        Courtesy of:
            http://stackoverflow.com/questions/39862709/generate-coordinates-in-grid-that-lie-within-a-circle
        Inputs:
        Returns:
    """
    # print("Drawing a new circle")
    # coords = []
    originx = origin[0]
    originy = origin[1]
    xlim = int(radius)
    # - This doesn't work quite as intended yet 
    #   this should create a crater centered at orignx, originy, but is only
    #   creating semicircles (probably thanks to the abs() code- #
    for i in range(originx - xlim, originx + (xlim + 1)):
        # - TODO: Fix this so that it's not broken.
        #   the abs() part broke this, but without it we get complex numbers.
        #   once that is fixed, this should work brilliantly - #
        '''
		Kyle's notes. The problem seems to be that the "rows" value (I don't knw if x or y) is effecting 
		the circle size some how. Theoretically, if this were only producing semicircles, creating a ylim
		of the opposite value should draw the other half. There was this issue of tirangular structures being
		drawn. It comes from the i values possibly being around 500. 500 * 500 will produce a huge circle.
        '''
        if i > 499:
            continue
        if i < 1:
            continue
        ylimUp= int((abs((radius * radius) - ((i-originx) * (i-originx))))**0.5)
        ylimDown= - ylimUp
        for j in range(originy - ylimUp, originy + (ylimUp + 1)):
            if j > 499:
                continue
            if j < 1:
                continue
            # coords.append([i,j])
            image[i][j][0] += 0.1
            image[i][j][1] += 0.1
            image[i][j][2] += 0.1
            image[i][j][3]  = 1
        for j in range(originy - ylimDown, originy + (ylimDown + 1)):
            if j > 499:
                continue
            if j < 1:
                continue
            # coords.append([i,j])
            image[i][j][0] += 0.1
            image[i][j][1] += 0.1
            image[i][j][2] += 0.1
            image[i][j][3]  = 1
    return(image)


def simImpacts(blankimage):
    """
    Inputs:
    Returns:
    """

    count = 0
    cratermap = blankimage
    while 0 in cratermap[:][:][0]:
        count += 1
       # if count == 100:
       #     return cratermap, count
        #  - This should only examine the 3rd index of our image array
        #    which is itself an array of rgba values for that particular
        #    pixel. If each pixel is not empty, that is if the values in
        #    our rgba are nonzero, then we have reached saturation and can
        #    break from the loop - #

        # -- Generate the location for the center of the crater -- #
        x = int(np.random.rand()*500)
        y = int(np.random.rand()*500)

        # -- Mark the center of the crater -- #
        cratermap[x][y][0] += 0.1
        cratermap[x][y][1] += 0.1
        cratermap[x][y][2] += 0.1
        cratermap[x][y][3]  = 1

        # -- Generate and draw a crater for our impact -- #
        # - *10 here to make sure that our crater sizes are (mostly) above 10km - #
        impactsize = int(np.random.lognormal(1, 1, 1) * 10)
        if impactsize < 10:
            # - If we didn't get a crater at least 10km in size, skip to next iteration - #
            continue
        # - Pass to draw function to draw the actual crater generated by the impact - #
        cratermap = drawCircle(cratermap, int(impactsize/2), [x,y])
        # - commented code is deprecated - #
        # for pixel in impactcrater:
        #     xval = pixel[0]
        #     yval = pixel[1]
        #     if xval > 499:
        #         continue
        #     if xval < 1:
        #         continue
        #     if yval > 499:
        #         continue
        #     if yval < 1:
        #         continue
        #     cratermap[xval][yval][0] += 0.1
        #     cratermap[xval][yval][1] += 0.1
        #     cratermap[xval][yval][2] += 0.1
        #     cratermap[xval][yval][3]  = 1
        print(count)
    return cratermap, count

image, cratercount = simImpacts(blankimage=image)

print("""%i craters were generated.
This equates to %.2e years taken to reach saturation.""" %(cratercount, cratercount*1000))
total = time.time() - start
print("Time taken to run simulation: %f seconds" %(total))
pl.imshow(image)
pl.show()
