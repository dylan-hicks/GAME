import matplotlib.pyplot as plt

p1, = plt.plot([1,2,3,4], [25, 22, 34, 19], 'o', label='')
p2, = plt.plot([1,2,3,4], [35, 30, 24, 31], 'ro', label='')
plt.legend(loc='upper right')

plt.axis([0, 5, 0, 40])
plt.ylabel('Lebron James and Kevin Durant PPG')
plt.xlabel('Game number')
plt.show()
