#
# cell_tracker.py - plot 2-D cell tracks associated with PhysiCell .svg files
#
# Usage:
#  python cell_track_plotter.py <start tracking index> <step interval for tracking> <# of samples to include> <save image> <show image>" 
#  python cell_track_plotter.py <start tracking index> <step interval for tracking> <# of samples to include> 
# 
# Dependencies include matplotlib and numpy. We recommend installing the Anaconda Python3 distribution.
#
# Examples (run from directory containing the .svg files):
#  See below line 239 in "if __name__ == '__main__':"
#
# Author: Randy Heiland, modified by John Metzcar (Twitter - @jmetzcar)
#
import sys
import xml.etree.ElementTree as ET
import numpy as np
import glob
import matplotlib.pyplot as plt
import math

def plot_cell_tracks(starting_index: int, sample_step_interval: int, number_of_samples: int, output_plot: bool,
                     show_plot: bool):

    """
    Produces savable image of cell positional history, plotted as arrows (quiver plot) with final cell positions plotted as a cirle.
    Slight modification of the function in cell_track_plotter. The modification allows for tracking the index of a series
    of inputs such that outputs of this function can be appropriate indexed and compiled into a movie.

    sample_step_interval * number_of_samples - starting_index yields the trail length in time steps. number_of_samples provides
    the number of intervals plotted per image. 

    Parameters
    ----------
    starting_index :
        Integer index of the PhysiCell SVG output to begin trackign at
    sample_step_interval :
        Interval (number of time steps (SVGs)) to sample at. A value of 2 would add a tracking point for every other SVG
    number_of_samples :
        Number of SVGs to process (total)/Length of cell positional history. Number of samples * sample size step interval provides the index of the final SVG to process
    output_plot :
        Save plot flag (required to produce a movie from resulting images)
    show_plot :
        Show plot flag (for processing many images in a loop, this should likely be set to false. Images have to be closed manually)
    naming_index :
        Unique to this function. Index used in naming output file of plot_cell_tracks function - filename = output + naming_index.png and leading zeros as needed.
    Returns
    -------
    Null :
        Produces a png image from the input PhysiCell SVGs.
    """
    
    maxCount = starting_index

    d={}   # dictionary to hold all (x,y) positions of cells

    """ 
    --- for example ---
    In [141]: d['cell1599'][0:3]
    Out[141]: 
    array([[ 4900.  ,  4900.  ],
           [ 4934.17,  4487.91],
           [ 4960.75,  4148.02]])
    """

    ####################################################################################################################
    ####################################            Generate list of file indices to load       ########################
    ####################################################################################################################

    endpoint = starting_index + sample_step_interval*number_of_samples
    file_indices = np.linspace(starting_index, endpoint, num=number_of_samples, endpoint=False)
    print(file_indices)

    ####### Uncomment for statement below to generate a random list of file names versus the prespecifed list. ########
    ####### Leaving for historical record. If used, the inputs would need to be a single integer,       ########
    ####### versus the three integers required to generate the prespecified list. Also, remove the other for statement. ########
    # count = 0
    #
    # for fname in glob.glob('snapshot*.svg'):
    #     print(fname)
    # # for fname in['snapshot00000000.svg', 'snapshot00000001.svg']:
    # # for fname in['snapshot00000000.svg']:
    # #   print(fname)
    #   count += 1
    #   if count > maxCount:
    #     break


    ####################################################################################################################
    ####################################        Main loading and processing loop                ########################
    ####################################################################################################################

    for file_index in file_indices:
        fname = "%0.8d" % file_index
        fname = 'snapshot' + fname + '.svg'# https://realpython.com/python-f-strings/
        print(fname)

        ##### Parse XML tree into a dictionary called 'tree" and get root
        # print('\n---- ' + fname + ':')
        tree=ET.parse(fname)

        # print('--- root.tag, root.attrib ---')
        root=tree.getroot()
        #  print('--- root.tag ---')
        #  print(root.tag)
        #  print('--- root.attrib ---')
        #  print(root.attrib)
        #  print('--- child.tag, child.attrib ---')

        numChildren = 0

        ### Find branches coming from root - tissue parents
        for child in root:
            #  print(child.tag, child.attrib)
            #    print('attrib=',child.attrib)
            #  if (child.attrib['id'] == 'tissue'):

            if 'width' in child.attrib.keys():
                #### Assumes square domains
                plot_spatial_length = float(child.attrib['width'])
                # print(plot_spatial_length)

            ##### Find the tissue tag and make it child
            if 'id' in child.attrib.keys():
            #      print('-------- found tissue!!')
                tissue_parent = child
                break

        #  print('------ search tissue')

        ### find the branch with the cells "id=cells" among all the branches in the XML root
        for child in tissue_parent:
        #    print('attrib=',child.attrib)
            if (child.attrib['id'] == 'cells'):
            #      print('-------- found cells!!')
                cells_parent = child
                break
            numChildren += 1

        ### Search within the cells branch for all indiviual cells. Get their locations
        num_cells = 0
        #  print('------ search cells')
        for child in cells_parent:
        #    print(child.tag, child.attrib)
        #    print('attrib=',child.attrib)

            # Find the locations of the cells within the cell tags
            for circle in child:
            #      print('  --- cx,cy=',circle.attrib['cx'],circle.attrib['cy'])
                  xval = float(circle.attrib['cx'])

                  # should we test for bogus x,y locations??
                  if (math.fabs(xval) > 10000.):
                      print("xval=",xval)
                      break
                  yval = float(circle.attrib['cy'])
                  if (math.fabs(yval) > 10000.):
                      print("xval=",xval)
                      break

                  # Pull out the cell's location. If ID not already in stack to track, put in new cell in dictionary
                  if (child.attrib['id'] in d.keys()):
                      d[child.attrib['id']] = np.vstack((d[child.attrib['id']], [ float(circle.attrib['cx']), float(circle.attrib['cy']) ]))
                  else:
                      d[child.attrib['id']] = np.array( [ float(circle.attrib['cx']), float(circle.attrib['cy']) ])
                  break

        #    if (child.attrib['id'] == 'cells'):
        #      print('-------- found cells!!')
        #      tissue_child = child

            #### num_cells becomes total number of cells per frame/sample
            num_cells += 1
        print(fname,':  num_cells= ',num_cells)

    ####################################################################################################################
    ####################################        Plot cell tracks and other options              ########################
    ####################################################################################################################

    fig = plt.figure(figsize=(8,8))
    ax = fig.gca()
    ax.set_aspect("equal")
    #ax.set_xticks([])
    #ax.set_yticks([]);
    #ax.set_xlim(0, 8); ax.set_ylim(0, 8)

    #print 'dir(fig)=',dir(fig)
    #fig.set_figwidth(8)
    #fig.set_figheight(8)

    count = 0

    # weighting = np.linspace(0.0001, 3.5, num=number_of_samples)
    #
    # weighting = np.log10(weighting)

    ##### Extract and plot position data for each cell found
    for key in d.keys():
        if (len(d[key].shape) == 2):
            x = d[key][:,0]
            y = d[key][:,1]

            # plt.plot(x, y,'-')  # plot doesn't seem to allow weighting or size variation at all in teh connections ...  # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.arrow.html or https://stackoverflow.com/questions/7519467/line-plot-with-arrows-in-matplotlib
            # plt.scatter(x, y, s = weighting) - scatter allows weighting but doens't connect ...
            # plt.scatter(x, y, s=weighting) # could try a non-linear weighting ...

            #### Plot cell track as a directed, weighted (by length) path
            plt.quiver(x[:-1], y[:-1], x[1:] - x[:-1], y[1:] - y[:-1], scale_units='xy', angles='xy', scale=1, minlength = 0.001, headwidth=1.5, headlength=4)

            #### Plot final cell position
            plt.scatter(x[-1],y[-1], s = 3.5)

        elif (len(d[key].shape) == 1):
            x = d[key][0]
            y = d[key][1]

            plt.scatter(x, y, s=3.5)

        else:
            print(key, " has no x,y points")

    #### Build plot frame, titles, and save data
    plt.ylim(0, plot_spatial_length)
    plt.xlim(0, plot_spatial_length)

    title_str = "Starting at frame {}, sample interval of {} for {} total samples".format(starting_index, sample_step_interval, number_of_samples)
    plt.title(title_str)

    # could change to the custom in the movie output or some other more better output if desired.
    output_folder = ''
    snapshot = str(starting_index) + '_' + str(sample_step_interval) + '_' + str(number_of_samples)

    # Plot output
    if output_plot is True:
        plt.savefig(output_folder + snapshot + '.svg')
    if show_plot is True:
        plt.show()
    # plt.close()

if __name__ == '__main__':

    ####################################################################################################################
    ####################################            Usage example and input loading             ########################
    ####################################################################################################################

    if (len(sys.argv) == 6):
        usage_str = "Usage: %s <start tracking index> <step interval for tracking> <# of samples to include> <save image> <show image>" % (
        sys.argv[0])
        # print(usage_str)
        starting_index = int(sys.argv[1])
        sample_step_interval = int(sys.argv[2])
        number_of_samples = int(sys.argv[3])
        save_plot = bool(sys.argv[4])
        show_plot = bool(sys.argv[5])

        # print("e.g.,")
        # eg_str = "%s 0 1 10 indicates start at 0, go up by ones, and stop when you 10 samples" % (sys.argv[0])
        # print(eg_str)

        plot_cell_tracks(starting_index, sample_step_interval, number_of_samples, save_plot, show_plot)


    elif (len(sys.argv) == 4):
        usage_str = "Usage: %s <start tracking index> <step interval for tracking> <# of samples to include>" % (
        sys.argv[0])
        # print(usage_str)
        starting_index = int(sys.argv[1])
        sample_step_interval = int(sys.argv[2])
        number_of_samples = int(sys.argv[3])

        # print("e.g.,")
        # eg_str = "%s 0 1 10 indicates start at 0, go up by ones, and stop when you 10 samples" % (sys.argv[0])
        # print(eg_str)

        plot_cell_tracks(starting_index, sample_step_interval, number_of_samples, False, True)

    else:
        print('\nInput 3 arguments to produce and show plot only')
        usage_str = "Usage: %s <start tracking index> <step interval for tracking> <# of samples to include> \n" % (
        sys.argv[0])
        print(usage_str)
        print('Input 5 arguments to directly control saving and showing the plots')
        usage_str = "Usage: %s <start tracking index> <step interval for tracking> <# of samples to include> <save image> <show image> \n" % (
        sys.argv[0])
        print(usage_str)
        exit(1)

