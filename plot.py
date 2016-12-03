import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


x = range(100,1100,100)
for i in range(len(x)):
	x[i] = 1. - x[i] / 1000.
print x

# Sampling, avg
SA = [.0371,.0271747,.0260,.0247,.0225,.0167, .0176, .0195, .0165, .0157]
# Filtering, avg
#FA = [.0303, .0233, .0117, .0099, .0096, .0104, .0073, .0082, .0058, .0017]
FA = [.0241, .0187, .0166, .0119, .0105, .0075, .0065, .0047, .0045, .0024]

# Sampling, RMS
SR = [.0474,.0363, .0336, .0353, .0252, .0224, .0222, .0280, .0229, .0218]
# Filtering, RMS
# FR = [.0375, .0281, .0153, .0124, .0120, .0135, .0097, .0099, .0076, .0031]
FR = [.0333, .0264, .0209, .0154, .0128, .0102, .0085, .0060, .0064, .0041]


red_patch = mpatches.Patch(color='r', label='Sampling')
green_patch = mpatches.Patch(color='g', label='Filtering')
plt.legend(handles=[red_patch, green_patch])

plt.title('Sampling & Filtering: Speedup vs. Accuracy (AVG)')
plt.ylabel('Average Difference')
plt.xlabel('Speedup (%)')

plt.plot(x, SA, 'r-o', x, FA, 'g-o')
plt.axis([0, 1, 0, .05])
plt.show()



# matplotlib.pyplot.scatter(x,y)
# matplotlib.pyplot.show()