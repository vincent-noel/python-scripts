import sys
import os
import glob
import numpy as np
from pyMCDS_cells import pyMCDS_cells
import matplotlib.pyplot as plt

argc = len(sys.argv)-1
print("# args=",argc)

#data_dir = 'output'
if (argc < 1):
#  data_dir = int(sys.argv[kdx])
  print("Usage: provide output subdir")
  sys.exit(-1)

kdx = 1
data_dir = sys.argv[kdx]
print('data_dir = ',data_dir)
os.chdir(data_dir)
xml_files = glob.glob('output*.xml')
os.chdir('..')
xml_files.sort()
#print('xml_files = ',xml_files)

ds_count = len(xml_files)
print("----- ds_count = ",ds_count)
mcds = [pyMCDS_cells(xml_files[i], data_dir) for i in range(ds_count)]

tval = np.linspace(0, mcds[-1].get_time(), ds_count)
print('tval= ',tval)

# count epi cells still live 
y_live = np.array( [(np.count_nonzero((mcds[idx].data['discrete_cells']['cell_type'] == 1) & (mcds[idx].data['discrete_cells']['cycle_model'] < 100) == True)) for idx in range(ds_count)] )

# count epi cells infected
y_infected = np.array( [(np.count_nonzero((mcds[idx].data['discrete_cells']['cell_type'] == 1) & (mcds[idx].data['discrete_cells']['virion'] > 1.) == True)) for idx in range(ds_count)] )

# count epi cells dead
y_dead = np.array( [(np.count_nonzero((mcds[idx].data['discrete_cells']['cell_type'] == 1) & (mcds[idx].data['discrete_cells']['cycle_model'] >= 100) == True)) for idx in range(ds_count)] )

plt.plot(tval, y_live, label='live', linewidth=2)  #, color='lime')
plt.plot(tval, y_infected, label='infected', linewidth=2)
plt.plot(tval, y_dead, label='dead', linewidth=2)

plt.legend(loc='center left', prop={'size': 10})
plt.xticks([1440,2*1440, 3*1440, 4*1440, 5*1440, 6*1440, 7*1440, 8*1440, 9*1440, 10*1440], ('1', '2','3','4','5','6','7','8','9','10'))
plt.title(data_dir)
plt.xlabel('Time (days)')
plt.ylabel('Number of cells')
plt.savefig(data_dir + '.png')
plt.show()
