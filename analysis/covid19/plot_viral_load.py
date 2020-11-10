import sys
import os
import glob
import numpy as np
from pyMCDS_cells import pyMCDS_cells
import matplotlib.pyplot as plt

argc = len(sys.argv)-1
print("# args=",argc)

data_dir = 'output'
if (argc < 1):
#  data_dir = int(sys.argv[kdx])
  print("Usage: provide output subdir")
  sys.exit(-1)

kdx = 1
data_dir = sys.argv[kdx]

print('data_dir = ',data_dir)

os.chdir(data_dir)
#xml_files = glob.glob('output/output*.xml')
xml_files = glob.glob('output*.xml')
os.chdir('..')
xml_files.sort()
#print('xml_files = ',xml_files)
n = len(xml_files)

ds_count = len(xml_files)
print("----- ds_count = ",ds_count)
#mcds = [pyMCDS(xml_files[i], '.') for i in range(ds_count)]
#mcds = [pyMCDS_cells(xml_files[i], '.') for i in range(ds_count)]
mcds = [pyMCDS_cells(xml_files[i], data_dir) for i in range(ds_count)]

tval = np.linspace(0, mcds[-1].get_time(), ds_count)
print('tval= ',tval)

y_load = np.array( [np.floor(mcds[idx].data['discrete_cells']['assembled_virion']).sum()  for idx in range(ds_count)] ).astype(int)
print(y_load)

# idx = 0
# for f in xml_files:
#     mcds = pyMCDS_cells(f, data_dir)
#     cell_type = mcds.data['discrete_cells']['cell_type']
#     cd8 = np.where(cell_type == 3.0)
#     mac = np.where(cell_type == 4.0)
#     neut = np.where(cell_type == 5.0)
#     t[idx] = mcds.get_time()
#     num_mac[idx] = len(mac[0])
#     num_cd8[idx] = len(cd8[0])
#     num_neut[idx] = len(neut[0])
#     idx += 1

# #plt.plot(t,num_mac,'-o',)
#plt.plot(t,num_mac, t,num_cd8, t,num_neut)
plt.plot(tval,y_load)
plt.title(data_dir)
plt.savefig(data_dir + '.png')
plt.show()
