import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# فایل شامل مختصات: هر خط "x,y,z"
filename = 'C:\\Users\\Noyan\\Dropbox\\IoUT Papers\\Fifth\\Code\\IoUT_Simulator\\coordinates.txt'

# خواندن مختصات از فایل
nodes = np.loadtxt(filename, delimiter=',')

# اختصاص رنگ: قرمز برای Z=500، آبی برای بقیه
colors = ['red' if z==500 else 'blue' for z in nodes[:,2]]

# رسم سه بعدی
fig = plt.figure(figsize=(12,9))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(nodes[:,0], nodes[:,1], nodes[:,2], c=colors, s=80)

# برچسب محور
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (depth in m)')

# عنوان شکل
ax.set_title('3D Distribution of IoUT Sensor Nodes (Red: Z=500, Blue: Other nodes)')
plt.savefig('C:\\Users\\Noyan\\Dropbox\\IoUT Papers\\Fifth\\Code\\IoUT_Simulator\\nodes_3d.pdf')
plt.show()
