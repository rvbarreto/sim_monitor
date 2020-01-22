from netCDF4 import Dataset
import matplotlib.pyplot as plt

# get u v data from numerical simulation
dataset = Dataset(
    '/home/ricardo-velho/Documents/layer_model/mediterranean_skeleton_simulation.nc',
    'rs')

t = range(0, dataset.dimensions['time'].size)
dt = dataset.groups['time_variables']['dt'].getValue().data * 1.
print_t = dataset.groups['time_variables']['print_t'].getValue().data * 1.
t = (t*dt*print_t)/(60*60*24)

Q1 = dataset.groups['sources']['gibraltar_maw']['source_Q'][:].data
Q2 = dataset.groups['sources']['gibraltar_liw']['source_Q'][:].data
Q3 = dataset.groups['sources']['aegean_maw']['source_Q'][:].data
Q4 = dataset.groups['sources']['aegean_liw']['source_Q'][:].data

plt.plot(t, Q1)
plt.savefig('Q1.png')
plt.plot(t, Q2)
plt.savefig('Q2.png')
plt.plot(t, Q3)
plt.savefig('Q3.png')
plt.plot(t, Q4)
plt.savefig('Q4.png')
