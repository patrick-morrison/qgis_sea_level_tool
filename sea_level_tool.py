# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SeaLevelTool
                                 A QGIS plugin
 This allows you to adjust sea level according to sea level curves
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2022-12-23
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Patrick Morrison
        email                : patrick.morrison@research.uwa.edu.au
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt, QEventLoop
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QFileDialog
from qgis.core import Qgis, QgsProject, QgsMapLayerProxyModel, QgsExpressionContextUtils, QgsMapRendererSequentialJob, QgsLayoutExporter, QgsFeatureRequest,QgsExpression
import numpy as np
import os

from . import pyqtgraph as pg

# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the DockWidget
from .sea_level_tool_dockwidget import SeaLevelToolDockWidget
import os.path



class SeaLevelTool:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SeaLevelTool_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&SeaLevelTool')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'SeaLevelTool')
        self.toolbar.setObjectName(u'SeaLevelTool')

        #print "** INITIALIZING SeaLevelTool"

        self.pluginIsActive = False
        self.dockwidget = None


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SeaLevelTool', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/sea_level_tool/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Sea Level Curve'),
            callback=self.run,
            parent=self.iface.mainWindow())
        

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING SeaLevelTool"
        self.dockwidget.level.setValue(0)

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD SeaLevelTool"

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&SeaLevelTool'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
    
    def adjust_levels(self, type, changed):
        level_box = self.dockwidget.level.value()*10
        level_slider = self.dockwidget.level_slider.value()/10

        if type == 'slider':
            self.dockwidget.level_slider.sliderMoved.disconnect()
            self.dockwidget.level_slider.setValue(level_box)
            self.dockwidget.level_slider.sliderMoved.connect(lambda v: self.adjust_levels('box', v))

        if type == 'box':
            self.dockwidget.level.valueChanged.disconnect()
            self.dockwidget.level.setValue(level_slider)
            self.dockwidget.level.valueChanged.connect(lambda v: self.adjust_levels("slider", v))

    def adjust_ages(self, type, changed):
        age_box = self.dockwidget.age.value()*10
        age_slider = self.dockwidget.age_slider.value()/10

        if type == 'slider':
            self.dockwidget.age_slider.sliderMoved.disconnect()
            self.dockwidget.age_slider.setValue(age_box)
            self.dockwidget.age_slider.sliderMoved.connect(lambda v: self.adjust_ages('box', v))

        if type == 'box':
            self.dockwidget.age.valueChanged.disconnect()
            self.dockwidget.age.setValue(age_slider)
            self.dockwidget.age.valueChanged.connect(lambda v: self.adjust_ages("slider", v))

    def set_level_max(self, v):
        self.dockwidget.level.setMaximum(v)
        self.dockwidget.level_min.setMaximum(v)
        self.dockwidget.level_slider.setMaximum(v*10)
    def set_level_min(self, v):
        self.dockwidget.level.setMinimum(v)
        self.dockwidget.level_max.setMinimum(v)
        self.dockwidget.level_slider.setMinimum(v*10)

    def set_oldest(self, v):
        self.dockwidget.age.setMaximum(v)
        self.dockwidget.youngest.setMaximum(v)
        self.dockwidget.age_slider.setMaximum(v*10)
    def set_youngest(self, v):
        self.dockwidget.age.setMinimum(v)
        self.dockwidget.oldest.setMinimum(v)
        self.dockwidget.age_slider.setMinimum(v*10)
    
    def msl(self):
        global total_change
        total_change = 0
    
    def render(self):
        global age

        layout_name = self.dockwidget.composer_box.currentText()

        def append_age(filename, age):
            name, ext = os.path.splitext(filename)
            return f"{name}_{age}ka{ext}"


        if layout_name == 'Map Canvas':
            settings = self.iface.mapCanvas().mapSettings()
            renderer = QgsMapRendererSequentialJob(settings)
            event_loop = QEventLoop()
            renderer.finished.connect(event_loop.quit)
            renderer.start()
            event_loop.exec_()

            img = renderer.renderedImage()
            img.save(append_age(chosen_filename, age))
        else:
            project = QgsProject.instance()
            manager = project.layoutManager()
            layout = manager.layoutByName(layout_name)
            exporter = QgsLayoutExporter(layout)
            exporter.exportToImage(append_age(chosen_filename, age), QgsLayoutExporter.ImageExportSettings())

    def animate(self):

        if self.dockwidget.dec_check.isChecked():
            times_ten = list(range(self.dockwidget.youngest.value()*10, self.dockwidget.oldest.value()*10+1, 1))
            years = [round(x * 0.1, 1) for x in times_ten]
        else:
            years = list(range(self.dockwidget.youngest.value(), self.dockwidget.oldest.value()+1, 1))

        for year in years:
            self.change_age(year)
            self.render()
            

    def change_sea(self, level):
        try:
            global total_change
            sea_level = level-total_change

            global bath

            items = bath.renderer().shader().rasterShaderFunction().colorRampItemList()
                
            for item in items:
                item.value += sea_level
                    
            total_change += sea_level
            self.h_bar.setPos(total_change)
            QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(),'sea_level',total_change)
                
            bath.renderer().shader().rasterShaderFunction().setColorRampItemList(items)
            bath.triggerRepaint()
            bath.emitStyleChanged()

        except NameError:
            self.iface.messageBar().pushMessage("No elevation data!", "Select DEM", level=Qgis.Warning, duration=5)
        
        except AttributeError:
            self.iface.messageBar().pushMessage("Wrong layer style", "Change to singleband pseudocolour", level=Qgis.Warning, duration=5)


    def select_raster_fields(self):
        global bath
        if self.dockwidget.level.value != 0:
            self.dockwidget.level.setValue(0)
        bath = self.dockwidget.raster_layer_box.currentLayer()
        self.dockwidget.style_button.setEnabled(True)
        self.dockwidget.animate_button.setEnabled(True)
        self.dockwidget.fileButton.setEnabled(True)
        self.dockwidget.composer_box.setEnabled(True)
        

    def select_curve_fields(self):
        global curve

        request = QgsFeatureRequest()
        data = self.dockwidget.curve_layer_box.currentLayer()
        clause = QgsFeatureRequest.OrderByClause(QgsExpression('to_real(age)'), ascending=True)
        orderby = QgsFeatureRequest.OrderBy([clause])
        request.setOrderBy(orderby)

        if data:
            curve = {}
            for feature in data.getFeatures(request):
                age = float(feature["age"])
                level = float(feature["sea_level"])
                curve[age] = level
        else:
             curve = {0: 0, 10:0, 20:-120, 30:-100, 40:-80,50:-70,60:-70,70:-80,80:-50,90:-50,100:-30,110:-50,120:-10,130:5}

        self.dockwidget.level_min.setValue(min(list(curve.values())))
        self.dockwidget.level_max.setValue(max(list(curve.values())))
        self.dockwidget.oldest.setValue(max(list(curve.keys())))
        self.dockwidget.youngest.setValue(min(list(curve.keys())))

        global curve_interp

        if self.dockwidget.interp_check.isChecked():
            if self.dockwidget.dec_check.isChecked():
                times_ten = list(range(self.dockwidget.youngest.value()*10, self.dockwidget.oldest.value()*10+1, 1))
                x = [x * 0.1 for x in times_ten]
            else:
                x = list(range(self.dockwidget.youngest.value(), self.dockwidget.oldest.value()+1, 1))
            
            
            y = np.interp(x, list(curve.keys()), list(curve.values()))
            curve = dict(zip(x, y))
        
        pen = pg.mkPen(color=(0, 0, 0), width=3)
        graph = self.dockwidget.curve_graph
        graph.clear()
        graph.plot(list(curve.keys()),list(curve.values()), symbol='o', pen=pen, symbolSize=10)
        graph.addItem(self.h_bar)
        graph.addItem(self.v_bar)

        self.change_age(self.dockwidget.age.value())


    def update_curve(self):
        global total_change
        total_change = 0

    def change_resolution(self):
        self.select_curve_fields()
        if self.dockwidget.level.value != 0:
            self.dockwidget.level.setValue(0)
        if self.dockwidget.age.value != 0:
            self.dockwidget.age.setValue(0)

        if self.dockwidget.dec_check.isChecked():
            self.dockwidget.level.setSingleStep(.1)
            self.dockwidget.level.setDecimals(1)
            self.dockwidget.level_slider.setSingleStep(1)

            self.dockwidget.age.setSingleStep(.1)
            self.dockwidget.age.setDecimals(1)
            self.dockwidget.age_slider.setSingleStep(1)
        else:
            self.dockwidget.age.setSingleStep(1)
            self.dockwidget.age.setDecimals(0)
            self.dockwidget.age_slider.setSingleStep(10)

            self.dockwidget.level.setSingleStep(1)
            self.dockwidget.level.setDecimals(0)
            self.dockwidget.level_slider.setSingleStep(10)


    def change_age(self, new_age):
        global age
        age = new_age
        closest_age = min(curve, key=lambda x:abs(x-age))
        self.dockwidget.level.setValue(curve[closest_age])
        QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(),'age',age)
        self.v_bar.setPos(age)

    def showDialog(self):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("Set Raster Style")
            msgBox.setText("Overwrite raster style with bathy/topo.")
            msgBox.setInformativeText("""Default is cpt-city/mby from -400 to 250. 
             \nNatural is cpy-city/wiki-scotland from -60 to 50.
             \n Discrete is blues from 0 to -30 to -120m, & green above 0.
             \n Set map title (View->Decorations) according to variables:
             \n [% @sea_level %]m [% @age %]ka
             \n Make a print layout and select it for custom renders.
             """)

            msgBox.setStandardButtons(msgBox.Cancel)
            msgBox.setDefaultButton(msgBox.Cancel)
            msgBox.setEscapeButton(msgBox.Cancel)

            default_button = msgBox.addButton('Default', msgBox.ActionRole)
            default_button.clicked.connect(lambda v: self.changeStyle('default'))

            natural_button = msgBox.addButton('Natural', msgBox.ActionRole)
            natural_button.clicked.connect(lambda v: self.changeStyle('natural'))

            discrete_button = msgBox.addButton('Earth', msgBox.ActionRole)
            discrete_button.clicked.connect(lambda v: self.changeStyle('earth'))

            discrete_button = msgBox.addButton('Discrete', msgBox.ActionRole)
            discrete_button.clicked.connect(lambda v: self.changeStyle('discrete'))

            msgBox.exec()

    def changeStyle(self, style):
        global bath
        path = os.path.dirname(os.path.abspath(__file__))
        if total_change !=0:
            self.change_sea(0)

        if style == 'default':
            default = path + "/styles/sea_level_default_style.qml"
            bath.loadNamedStyle(default)
        
        if style == 'natural':
            natural = path + "/styles/sea_level_natural_style.qml"
            bath.loadNamedStyle(natural)

        if style == 'discrete':
            discrete = path + "/styles/sea_level_discrete_style.qml"
            bath.loadNamedStyle(discrete)

        if style == 'earth':
            earth = path + "/styles/sea_level_earth2_style.qml"
            bath.loadNamedStyle(earth)

        bath.triggerRepaint()
        bath.emitStyleChanged()
    
    def select_output_file(self):
        global chosen_filename
        chosen_filename, _filter = QFileDialog.getSaveFileName(
            self.dockwidget, "Save render as","", '*.png')
        name, ext = os.path.splitext(chosen_filename)
        name = os.path.basename(name)
        self.dockwidget.filename_display.setText(f"{name}_{age}ka{ext}")

    def update_layouts(self):
        selected = self.dockwidget.composer_box.currentText()
        layouts_list = QgsProject.instance().layoutManager().printLayouts()
        self.dockwidget.composer_box.clear()
        self.dockwidget.composer_box.addItems(['Map Canvas'])
        self.dockwidget.composer_box.addItems([layout.name() for layout in layouts_list])
        if selected in [layout.name() for layout in layouts_list]:
            self.dockwidget.composer_box.setCurrentText(selected)
        else:
            self.dockwidget.composer_box.setCurrentText('Map Canvas')

    #--------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING SeaLevelTool"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)

            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = SeaLevelToolDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.dockwidget)
            self.dockwidget.show()
        
        global bath
        #bath = QgsProject.instance().mapLayersByName('bath')[0]
        self.dockwidget.raster_layer_box.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.dockwidget.raster_layer_box.layerChanged.connect(self.select_raster_fields)
        self.dockwidget.raster_layer_box.setCurrentIndex(0)
        #bath = self.dockwidget.raster_layer_box.currentLayer()
        self.msl()

        self.dockwidget.curve_layer_box.setFilters(QgsMapLayerProxyModel.NoGeometry)
        self.dockwidget.curve_layer_box.layerChanged.connect(self.select_curve_fields)
        self.dockwidget.curve_layer_box.setCurrentIndex(0)

        
        #Set title decoration to [% @sea_level %]m
        project = QgsProject.instance()
        global sea_level
        QgsExpressionContextUtils.setProjectVariable(project,'sea_level',total_change)
        self.dockwidget.animate_button.clicked.connect(self.animate)

        global curve
        curve = {0: 0, 10:0, 20:-120, 30:-100, 40:-80,50:-70,60:-70,70:-80,80:-50,90:-50,100:-30,110:-50,120:-10,130:5}
        self.dockwidget.interp_check.stateChanged.connect(self.select_curve_fields)
        self.dockwidget.dec_check.stateChanged.connect(self.change_resolution)

        global age
        age = 0
        QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(),'age',age)

        pen = pg.mkPen(color=(0, 0, 0), width=3)
        graph = self.dockwidget.curve_graph
        graph.plot(list(curve.keys()),list(curve.values()), symbol='o', pen=pen, symbolSize=10)
        styles = {'color':'b', 'font-size':'12px'}
        graph.setLabel('left', 'Sea level (m)', **styles)
        graph.setLabel('bottom', 'Age (ka)', **styles)
        graph.showGrid(x=True, y=True)
        graph.invertX(True)
        current_pen = pg.mkPen(color='b', width=2, style=QtCore.Qt.DotLine)
        self.h_bar = pg.InfiniteLine(movable=False, angle=0,pos=0,pen=current_pen)
        graph.addItem(self.h_bar)
        self.v_bar = pg.InfiniteLine(movable=False, angle=90,pos=0,pen=current_pen)
        graph.addItem(self.v_bar)

        layouts_list = QgsProject.instance().layoutManager().printLayouts()
        self.dockwidget.composer_box.clear()
        self.dockwidget.composer_box.addItems(['Map Canvas'])
        self.dockwidget.composer_box.addItems([layout.name() for layout in layouts_list])
        QgsProject.instance().layoutManager().layoutAdded.connect(self.update_layouts)
        QgsProject.instance().layoutManager().layoutRemoved.connect(self.update_layouts)
        QgsProject.instance().layoutManager().layoutRenamed.connect(self.update_layouts)

        self.dockwidget.level.valueChanged.connect(lambda v: self.change_sea(v))
        self.dockwidget.level_slider.valueChanged.connect(lambda v: self.change_sea(v/10))

        self.dockwidget.level.valueChanged.connect(lambda v: self.adjust_levels('slider', v))
        self.dockwidget.level_slider.sliderMoved.connect(lambda v: self.adjust_levels("box", v))

        self.dockwidget.age.valueChanged.connect(lambda v: self.adjust_ages('slider', v))
        self.dockwidget.age_slider.sliderMoved.connect(lambda v: self.adjust_ages("box", v))

        self.dockwidget.level_min.valueChanged.connect(lambda v: self.set_level_min(v))
        self.dockwidget.level_max.valueChanged.connect(lambda v: self.set_level_max(v))

        self.dockwidget.age.valueChanged.connect(lambda v: self.change_age(v))
        self.dockwidget.age_slider.valueChanged.connect(lambda v: self.change_age(v/10))

        self.dockwidget.oldest.valueChanged.connect(lambda v: self.set_oldest(v))
        self.dockwidget.youngest.valueChanged.connect(lambda v: self.set_youngest(v))
        self.dockwidget.style_button.clicked.connect(self.showDialog)

        self.dockwidget.fileButton.clicked.connect(self.select_output_file)
