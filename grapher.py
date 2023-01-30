import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./profiling/' + sys.argv[1])
df.Busy = df.Busy.apply(lambda x: json.loads(x))
df.Timestamp = df.Timestamp - df.Timestamp[0]

busy = np.vstack(df.Busy)
throughput = np.sum(busy, axis=1)

# Plot allocations

fig, axes = plt.subplots(busy.shape[1], 1, sharex=True, figsize=(4, 1 * busy.shape[1]))
axes = [axes] if busy.shape[1] == 1 else axes

for i in range(busy.shape[1]):
	axes[i].step(df['Timestamp'], busy[:,i], where = 'post')
	axes[i].set_ylabel('Worker %d' % i)

plt.tight_layout(pad = 0)
plt.savefig('./plots/busy.pdf')

fig, axes = plt.subplots(1, 1, sharex=True, figsize=(4, 2))

# Plot throughput

axes.step(df['Timestamp'], throughput, where = 'post')
axes.set_ylabel('Throughput')

plt.tight_layout(pad = 0)
plt.savefig('./plots/throughput.pdf')

print('Throughput = ', df.Finished.iloc[-1] / df.Timestamp.iloc[-1])

# Plot benchmark
df = pd.read_csv('./profiling/benchmarks.csv')
fig = plt.figure()
ax = plt.axes(projection='3d')
x, y, = np.array([1, 2, 3, 4]), np.array([1, 2, 3, 4])
X, Y = np.meshgrid(x, y); Z = np.zeros(X.shape)
Z = np.array(df.Throughput).reshape((4, 4))
ax.contour3D(X, Y, Z, 100, cmap='coolwarm')
ax.set_xlabel('Workers')
ax.set_ylabel('Functions')
ax.set_zlabel('Throughput');
plt.show()