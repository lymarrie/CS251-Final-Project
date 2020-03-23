"""
Make a histogram of 2 normally distributed random numbers. adjust bin
size and location to see its effect on the plot.
"""
import numpy as np
import matplotlib.pyplot as plt

ttx_periods = np.array( [24.969,25.5158,23.9104,24.969,31.687,23.3981,24.969,23.3981,23.9104,27.2289,22.8967,23.3981,22.8967,22.4061,23.3981,24.969,26.0745,25.5158,25.5158,24.969,24.434,24.969,26.6455,23.9104,28.4345,26.6455,24.434,23.9104,25.5158,21.4561,23.9104,24.969,26.6455,25.5158,26.6455,24.434,25.5158,23.9104,24.969,24.969,27.8252,24.434,22.8967,23.3981,26.6455,26.6455,24.434,22.4061,24.969,16.9072,26.6455,20.1062,24.969,23.3981,25.5158,26.6455,28.4345,27.2289,27.2289,26.0745,26.6455,26.0745,28.4345,24.434,26.6455,24.434,24.969,24.969,23.9104,26.0745,27.2289,24.434,23.9104,22.8967,23.9104,23.9104,24.969,23.9104,24.434,26.0745,24.969,25.5158,26.0745,26.0745,25.5158,23.3981,23.9104,25.5158,24.434,24.434,24.434,23.3981,24.969,24.969,25.5158,27.8252,23.9104,25.5158,26.0745,27.2289,25.5158,26.6455,23.3981,24.434,24.969,23.9104,25.5158,26.0745,23.3981,25.5158,29.6934,26.6455,24.969,24.434,27.8252,31.008,22.8967] )

wash_periods = np.array( [21.926,21.926,24.434,24.434,23.9104,18.8412,23.9104,27.2289,23.3981,26.0745,24.434,23.9104,25.5158,23.9104,25.5158,24.969,24.969,26.6455,24.969,24.969,24.434,24.969,24.969,25.5158,24.969,25.5158,25.5158,24.434,24.969,24.969,24.969,25.5158,23.9104,26.0745,24.434,24.434,24.969,24.969,24.969,24.434,24.434,24.434,24.969,24.969,26.0745,24.969,24.969,24.434,26.0745,24.434,24.434,25.5158,26.0745,24.969,24.434,23.9104,24.969,24.434,24.434,24.434,24.969,24.969,24.969,25.5158,24.969,24.969,24.434,25.5158,25.5158,25.5158,25.5158,24.969,24.969,25.5158,24.969,24.969,25.5158,25.5158,24.969,24.969,24.969,24.969,24.434,24.434,24.434,24.969,24.969,24.969,24.434,24.969,24.434,24.969,24.969,25.5158,24.434,25.5158,24.969,24.969,25.5158,26.0745,25.5158,24.969,24.969,24.434,24.434,24.434,24.969,24.969,24.434,24.969,24.969,24.969,24.969,25.5158,24.969,26.6455,24.969] )

# coding for plotting just one
fig = plt.figure()
plt.hist( ttx_periods, bins=1000, normed=0 )

fig = plt.figure()
both = np.vstack( (ttx_periods, wash_periods ) )
print both.shape
plt.hist( both.T )
plt.show()
exit()

fig = plt.figure()
plt.scatter( ttx_periods, wash_periods )

plt.show()

exit()



# The first distribution will be slightly to the right
# of the second.
r1a = 5.05 + np.random.randn(100)*0.1
r1b = 5.05 + np.random.randn(20)
r1 = np.concatenate( (r1a, r1b), 1 )

# coding for plotting just one
fig = plt.figure()
ax = plt.subplot( 1, 1, 1 )
ax.hist( r1, bins=200, normed=0 )
plt.show()
exit()

# make a second set of numbers
r2a = 4.95 + np.random.randn(100)*0.1
r2b = 4.95 + np.random.randn(20)
r2 = np.concatenate( (r2a, r2b), 1 )
rmat = np.matrix( [r1,r2] ).T

# plot both with fine bins
fig = plt.figure()
ax = plt.subplot(111)
ax.hist(rmat, bins=50, normed=0, alpha=0.75)


# plot both with course bins, and shift the edges of the
# bins a bit for each subplot.
binsa = np.linspace(3,7,5)
fig = plt.figure()
for i in range(1,6):
    for j in range(1,6):
        ax = plt.subplot(5, 5, (j-1)*5+i );
        bins = binsa + 0.2*i+0.02*j
        ax.hist(rmat, bins=bins, normed=0, alpha=0.75)

# label the last subplot.
ax.set_xlabel('X')
ax.set_ylabel('Probability')
ax.set_xlim(3, 7)
#ax.set_ylim(0, 0.03)

# this part is necessary :)
plt.show()

# example as published on matplotlib website
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)

fig = plt.figure()
ax = fig.add_subplot(111)

# the histogram of the data
n, bins, patches = ax.hist(x, 50, normed=1, facecolor='green', alpha=0.75)

# hist uses np.histogram under the hood to create 'n' and 'bins'.
# np.histogram returns the bin edges, so there will be 50 probability
# density values in n, 51 bin edges in bins and 50 patches.  To get
# everything lined up, we'll compute the bin centers
bincenters = 0.5*(bins[1:]+bins[:-1])
# add a 'best fit' line for the normal PDF
y = mlab.normpdf( bincenters, mu, sigma)
l = ax.plot(bincenters, y, 'r--', linewidth=1)

ax.set_xlabel('Smarts')
ax.set_ylabel('Probability')
#ax.set_title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
ax.set_xlim(40, 160)
ax.set_ylim(0, 0.03)
ax.grid(True)

plt.show()
"""