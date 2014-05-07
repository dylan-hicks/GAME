import matplotlib.pyplot as plt
import numpy as np

plt.plot([1,2,3,4], [25, 22, 34, 19], 'o', label='')
#plt.plot([1,2,3,4], [35, 30, 24, 31], 'ro', label='')
x = [1, 2, 3, 4]
p = np.polyfit(x, [25, 22, 34, 19], 1)
plt.plot(x,np.polyval(p,x),'r-',label="Best fit")
plt.legend(loc='upper right')

plt.axis([0, 5, 0, 40])
plt.ylabel('Lebron James and Kevin Durant PPG')
plt.xlabel('Game number')
plt.show()
