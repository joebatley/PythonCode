"""   
      File to import Data fiels from Blaatand and display content.

      Aim: to be able to plot! hahahaha
      
"""
      


# Enthought library imports
from enable.api import Component, ComponentEditor

# Chaco imports

from chaco.example_support import COLOR_PALETTE
from chaco.api import add_default_axes, add_default_grids, \
        OverlayPlotContainer, PlotLabel, ScatterPlot, create_line_plot
from chaco.api import ArrayPlotData, VPlotContainer, \
    Plot
from chaco.plotscrollbar import PlotScrollBar
from chaco.tools.api import PanTool, ZoomTool
from enthought.enable.api import ColorTrait, LineStyle, KeySpec
from enthought.enable.component_editor import ComponentEditor
from enthought.chaco.api import marker_trait, Plot, ToolbarPlot, ArrayPlotData, PlotAxis, PlotGraphicsContext
from traitsui.tabular_adapter import TabularAdapter
from enthought.chaco.tools.simple_zoom import SimpleZoom
from enthought.chaco.tools.api import BetterSelectingZoom
#from enthought.chaco2.api import ArrayPlotData, Plot, PlotGraphicsContext


# Traits Imports
from traits.api import *
from traitsui.api import *
from enthought.traits.ui.api import View, Item, Group, ListEditor, InstanceEditor, TabularEditor, EnumEditor
from traitsui.ui_editors.array_view_editor \
    import ArrayViewEditor
    
# TK import - reads in file name - used as was easier to link to Stoner class
#import tkFileDialog

# Other Imports
import Stoner as SC
from scipy.special import jn
from numpy import *
from numpy.random \
    import random
import os





class ArrayAdapter(TabularAdapter):

    font        = Font('Courier 10')
    alignment   = 'right'
    format      = '%.3e'
    index_text  = Property
    data=Instance(SC.DataFile)
    width=75.0
        

    def _get_index_text(self):
        return str(self.row)



#===============================================================================
# # Import File Class.
#===============================================================================
class DataWindow (HasTraits):
    """ Import file object """
    
    ######################### IMPORT DATA ##################################
    
    num = Int(1, desc = "Number of files to be imported", label = "Number of Files")
    file = Str()
    file_name = Str(desc = "Pick File", label = "File Name")  #Name of the selected file
    workingpath = Str(label = 'Directory')
    open = Button('Open')   
    headers = List(['x','y','z'],label = 'Column Headers')
    columns = Array(comparison_mode = NO_COMPARE)
    notes = Str('Notes',label = 'Notes')
    data_dict = {}
    adapter = ArrayAdapter()

        
    def _columns_changed(self):
        columns = self.columns
        
    def _open_fired ( self ):
        """ gets file info
        """
        #self.file = tkFileDialog.askopenfilename(title = 'Pick file to plot.') 
        
        self.workingpath = self.file.rpartition('/')[0]
        self.file_name = self.file.rpartition('/')[2]
        extension = '.' + self.file.rpartition('/')[2].rpartition('.')[2]
        self.file = SC.DataFile(False)
        data = self.file
        self.headers = data.column_headers
        self.columns = data.data
        self.notes = data.metadata['Notes']
        print self.notes
        i=0
        print self.headers
        for item in data.column_headers:
          self.data_dict[item] = self.columns[:,i]
          i = i + 1
          print 'ITEM = ' + item
          print 'I = ' + str(i)  
          
        self.cols=data.column_headers
        self.numpy_data=data.data
        cols=[(data.column_headers[i], i) for i in range(len(data.column_headers))]
        cols[:0]=[("index", "index")]
        self.adapter.columns=cols

        
     
    

    ########################## PLOT SETUP ############################
    
    
    xcol = Enum(values = 'headers')
    ycol = Enum(values = 'headers')
    plot = Instance(Component)
    color = ColorTrait("blue")
    line_style = LineStyle
    line_width = Float(1.0)    
    


    
    def _plot_default(self):
      container = OverlayPlotContainer(spacing=1000, padding_left=75, padding_top=10,padding_bottom=10,padding_right=10)
      self.columns = random((5,10))
      super(DataWindow, self).__init__()
      x = linspace(-14, 14, 100)
      y = sin(x) * x**3
      self.plotdata = ArrayPlotData(x = x, y = y)
      toolbar_location = 'bottom'
      plot = ToolbarPlot(self.plotdata)
      self.renderer = plot.plot(("x", "y"), type='line', color="blue")[0]
      x_axis = PlotAxis(orientation='bottom',title=self.xcol,mapper=plot.x_mapper,tick_in = 0)
      plot.underlays.append(x_axis)
      y_axis = PlotAxis(orientation='left',title=self.ycol, mapper=plot.y_mapper,tick_in = 0)
      #plot.y_axis.tick_label_formatter=lambda val: "%.3e"%val
      #plot.x_axis.tick_label_formatter=lambda val: "%.3e"%val#.rstrip("0").rstrip(".")
      plot.underlays.append(y_axis)
      plot.set(resizable='hv')
      self.plot = plot
      plot.title = self.notes
      # Add pan and zoom to the plot
      #plot.tools.append(PanTool(plot, constrain_key="shift"))
      #plot.tools.append(PanTool(plot, drag_button="right"))
      zoom = BetterSelectingZoom(plot, tool_mode='box',drag_button="right", always_on=True)
      plot.overlays.append(zoom)
      return plot


    @on_trait_change('notes,headers,xcol,ycol,data_dict,scale_x,scale_y')  
    def updateplot (self):
      self.plot=self._plot_default()
      self.renderer=self.plot.components[0]
      self.plotdata.set_data('y',self.data_dict[self.ycol]*self.scale_y)
      self.plotdata.set_data('x',self.data_dict[self.xcol]*self.scale_x)
      self.renderer.title = self.notes
     
      
        
    def __init__(self):
      self.plot=self._plot_default()
      self.renderer=self.plot.components[0]  
 
    def _color_changed(self):
        self.renderer.color = self.color

    def _line_style_changed(self):
        self.renderer.line_style = self.line_style

    def _line_width_changed(self):
        self.renderer.line_width = self.line_width   
        
    

    ############################## MANIPULATE DATA ################################
      
    scale_x = Float(1.0)
    scale_y = Float(1.0)
    
    
    
      
    ############################## DATA WINDOW VIEW ###############################
        
    def trait_view(self, parent=None):      
        group1 = Item('plot', editor=ComponentEditor(), show_label=False)
        
        group2= Group(
                Item( 'open', show_label = False ),
                Item('_'),
                VGroup(
                      Item( 'file_name', style = 'text', width = 400),
                      Item( 'workingpath', style = 'text', width = 400)
                      ),
                Item('_'),
                Item('notes', style = 'custom', height = 10),
                Item('_'),
                Group(
                      Item('headers', style = 'readonly', height = 200),
                      scrollable = True
                      ),
                label="Open")
          
        group3 = HGroup(Item( 'columns',style = 'readonly',show_label = False,width = 40,resizable = True,editor = TabularEditor(adapter = self.adapter)),label="Data")
        
        group4 = VGroup(HGroup(  
                               Item('xcol', label = 'X axis'),
                               Item('ycol', label = 'Y axis'),
                               ),
                        Item('color', label="Color", style="simple"),
                        Item('line_style', label="Line Style"),
                        Item('line_width', label="Width"),
                        Item('_'),
                        Item('scale_x'),
                        Item('scale_y'),
                        label="Plot Details")
 

        traits_view = View(HGroup(group1,Tabbed(group2, group3,group4)),
                  width=1524, 
                  height=1068, 
                  resizable=True, 
                  title="Stoner Plotter",  
                  #handler=MenuController
                  )
        return traits_view
        



#===============================================================================
# # Puts the Plot and Data widgets together in main windoe.
#===============================================================================

class MainWindow(HasTraits):

    datawindow = Instance(DataWindow)
    #figure = Instance(Figure)
    
    
    view = View(Group(
                      Item('datawindow', style="custom"),
                      show_labels=False,
                      ),
                resizable=True,
                #height=750, width=1200,
                buttons   = ['OK', 'Cancel'])

    

if __name__ == "__main__":
    mainwindow = MainWindow(datawindow = DataWindow())
    mainwindow.configure_traits()



'''
    def plot_container(self):
      
      container = OverlayPlotContainer(spacing=1000, padding_left=20, padding_top=10,padding_bottom=10,padding_right=10)
      
      plot=self._plot_default()
      container.add(plot)
      
      x_axis = PlotAxis(orientation='bottom',title=self.xcol,mapper=plot.x_mapper,tick_in = 0)
      plot.underlays.append(x_axis)
      y_axis = PlotAxis(orientation='left',title=self.ycol, mapper=plot.y_mapper,tick_in = 0)
      plot.underlays.append(y_axis)
      
      # Add pan and zoom to the plot
      container.tools.append(PanTool(plot, constrain_key="shift"))
      #plot.tools.append(PanTool(plot, drag_button="right"))
      zoom = BetterSelectingZoom(plot, tool_mode='box',drag_button="right", always_on=True)
      container.overlays.append(zoom)
      
      self.plot=container
      return container
'''

    