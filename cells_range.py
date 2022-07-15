#from pyMCDS_new import pyMCDS
from pyMCDS_cells_new import pyMCDS_cells
import numpy as np

#mcds = pyMCDS('output00000000.xml','.')  
mcds = pyMCDS_cells('output00000000.xml','.')  
tmins = mcds.get_time()
print('time (mins)=',tmins)

print(mcds.data['discrete_cells'].keys())
#print(mcds.data['discrete_cells']['ID'])
ncells = len(mcds.data['discrete_cells']['ID'])
print('num cells= ',ncells)

xvals = mcds.data['discrete_cells']['position_x']
yvals = mcds.data['discrete_cells']['position_y']
zvals = mcds.data['discrete_cells']['position_z']
print("x range: ",xvals.min(), xvals.max())
print("y range: ",yvals.min(), yvals.max())
print("z range: ",zvals.min(), zvals.max())
