from netCDF4 import Dataset
import numpy as np
# import gc
import matplotlib.pyplot as plt



def setNanMask(size, r, dx):
    mask = np.ones(size)
    mid_i = int(size[0]/2)
    mid_j = int(size[1]/2)
    for i in range(0, size[0]):
        for j in range(0, size[1]):
            diagonal = np.sqrt((i-mid_i)**2+(j-mid_j)**2)*dx
            if (diagonal > r):
                mask[i, j] = 0.0
    mask = mask.reshape(size[0]*size[1])
    return mask


def applyNanMask(data, mask):
    data = data.reshape(len(data)**2)
    data = data*mask
    data[data == 0.0] = float('NaN')
    return data


def getTransportAbs(U, V):
    speed = np.sqrt(U**2+V**2)
    return speed


# get u v data from numerical simulation
dataset = Dataset(
    '/home/ricardo-velho/Documents/layer_model/mediterranean_simulation_3.nc',
    'r')

t = dataset.dimensions['time'].size - 1
dt = dataset.groups['time_variables']['dt'].getValue().data * 1.
print_t = dataset.groups['time_variables']['print_t'].getValue().data * 1.
day = (t*dt*print_t)/(60*60*24)

y = dataset.dimensions['lat'].size
x = dataset.dimensions['lon'].size

layer = 5 - 1
U = dataset.groups['state_variables']['u'][t][layer]
V = dataset.groups['state_variables']['v'][t][layer]

h = dataset.groups['state_variables']['depth'][t][layer] - dataset.groups['state_variables']['depth'][t][layer -1]

U[h == 0] = float('NaN')
V[h == 0] = float('NaN')

# get speed
transport = getTransportAbs(U, V)

# set numerical simulation numeric labels
X_num, Y_num = np.meshgrid(np.arange(1, x+1, 1),
                           np.arange(1, y+1, 1))

fig = plt.figure(num=None, figsize=(16.35, 8.9), dpi=150, facecolor='w', edgecolor='k')
axs = fig.add_axes([0.05, 0.1, 1.05, 0.85 ])
fig.tight_layout()
font = {'weight': 'bold'}
font_y = {'size': 14,
          'weight': 'bold'}

cmax = transport.data.max()  # speed_phys_83.data.max()
cmin = transport.data.min()

sp2 = axs.pcolormesh(X_num, Y_num, transport,
                     cmap=plt.cm.bone_r,
                     vmin=cmin, vmax=cmax)

# set labels
axs.set_title('DAY n° ' + str(day) + ' @ surface', fontdict=font)
axs.set_xlabel('X (n of cells)')
axs.set_ylabel('Y (n of cells)')
cbar = fig.colorbar(sp2, ax=axs)
cbar.ax.set_title('m²/s')

# add quivers
Q = axs.quiver(X_num[::4, ::4],
               Y_num[::4, ::4],
               U[::4, ::4],
               V[::4, ::4],
               color='r',
               scale=1,
               scale_units='xy')
# qk = axs.quiverkey(Q, 0.80, 0.05, 1,
#                    r'$2.5 \frac{cm}{s}$', labelpos='E',
#                    coordinates='axes')

plt.savefig('surface_transports_day_' + str(int(day)) + '.png')
#plt.show()
