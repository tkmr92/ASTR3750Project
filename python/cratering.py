import numpy as np
import matplotlib.pyplot as pl
import time

start = time.time()

image = np.zeros([500, 500, 4])

def simImpacts(blankimage):
    """
    """

    count = 0
    cratermap = blankimage
    while 0 in blankimage[:][:][0]:
        count += 1
        #  - This should only examine the 3rd index of our image array
        #    which is itself an array of rgba values for that particular
        #    pixel. If each pixel is not empty, that is if the values in
        #    our rgba are nonzero, then we have reached saturation and can
        #    break from the loop - #
        x = np.random.rand()*500
        y = np.random.rand()*500
        # - Do something here to generate the size of an impact 
        #   (discard anything under 10km) and then draw a circle around
        #   the impact - #

        cratermap[x][y][0] += 0.1
        cratermap[x][y][1] += 0.1
        cratermap[x][y][2] += 0.1
        cratermap[x][y][3]  = 1
    return cratermap, count

image, cratercount = simImpacts(blankimage=image)

print("""%i craters were generated.
This equates to %.2e years taken to reach saturation.""" %(cratercount, cratercount*1000))
total = time.time() - start
print("Time taken to run simulation: %f seconds" %(total))
pl.imshow(image)
pl.show()
