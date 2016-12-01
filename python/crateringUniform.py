import numpy as np
import matplotlib.pyplot as pl
import time

# -- Needed to timr our simulation -- #
start = time.time()

# -- Create a 50x50x4 matrix to be used for our crater map -- #
image = np.zeros([50, 50, 4])

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
    cratermap = blankimage
    while 0 in cratermap[:][:][0]:
        # - Pass to draw function to draw the actual crater generated by the impact - #
        count += 1
        #  - This should only examine the 3rd index of our image array
        #    which is itself an array of rgba values for that particular
        #    pixel. If each pixel is not empty, that is if the values in
        #    our rgba are nonzero, then we have reached saturation and can
        #    break from the loop - #

        # -- Generate the location for the center of the crater -- #
        x = int(np.random.rand()*50)
        y = int(np.random.rand()*50)

        cratermap[x][y][0] += 0.1
        cratermap[x][y][1] += 0.1
        cratermap[x][y][2] += 0.1
        cratermap[x][y][3] =  1

    return cratermap, count

image, totalcount = simImpacts(blankimage=image)
temp = []
visible = 1
cratercount = 1
total = time.time() - start

print("""We have %i visible craters.
Our area saw %i impacters.
This equates to %.2e years taken to reach saturation.
At the point of saturation, we find that there are %i craters.

This simulation took %i seconds to run.""" %(visible, totalcount, totalcount*1000, cratercount, total))


pl.imshow(image)
pl.show()
