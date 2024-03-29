from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from .ShorelineDuration import ShorelineDuration
from .SubaerialDuration import SubaerialDuration
from .LastExposure import LastExposure



class Provider(QgsProcessingProvider):

    def loadAlgorithms(self, *args, **kwargs):
        self.addAlgorithm(ShorelineDuration())
        self.addAlgorithm(SubaerialDuration())
        self.addAlgorithm(LastExposure())

    def id(self, *args, **kwargs):
        """The ID of your plugin, used for identifying the provider.

        This string should be a unique, short, character only string,
        eg "qgis" or "gdal". This string should not be localised.
        """
        return 'sealeveltool'

    def name(self, *args, **kwargs):
        """The human friendly name of your plugin in Processing.

        This string should be as short as possible (e.g. "Lastools", not
        "Lastools version 1.0.1 64-bit") and localised.
        """
        return self.tr('SeaLevelTool')

    def icon(self):
        """Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """
        icon_path = ':/plugins/sea_level_tool/icon.png'
        return(QIcon(icon_path))