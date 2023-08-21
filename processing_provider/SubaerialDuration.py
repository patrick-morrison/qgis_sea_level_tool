# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterRasterDestination,
                       QgsExpression,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterNumber,
                       QgsFeatureRequest)
from qgis import processing
import numpy as np
import math


class SubaerialDuration(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT_DEM = 'INPUT_DEM'
    INPUT_SEALEVEL = 'INPUT_SEALEVEL'
    INPUT_YOUNGEST = 'INPUT_YOUNGEST'
    INPUT_OLDEST = 'INPUT_OLDEST'
    INPUT_BINWIDTH = 'INPUT_BINWIDTH'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return SubaerialDuration()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'SubaerialDuration'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Subaerial Duration')


    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Example algorithm short description")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_DEM,
                self.tr('Input DEM'),
                [QgsProcessing.TypeRaster]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_SEALEVEL,
                self.tr('Input sea level curve'),
                [QgsProcessing.TypeVector],
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_YOUNGEST,
                self.tr('Youngest (ka)'),
                QgsProcessingParameterNumber.Integer,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_OLDEST,
                self.tr('Oldest (ka)'),
                QgsProcessingParameterNumber.Integer,
                defaultValue=65
            )
        )

        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT,
                self.tr('Subaerial duration raster')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        source = self.parameterAsRasterLayer(
            parameters,
            self.INPUT_DEM,
            context
        )

        # If source was not found, throw an exception to indicate that the algorithm
        # encountered a fatal error. The exception text can be any string, but in this
        # case we use the pre-built invalidSourceError method to return a standard
        # helper text for when a source cannot be evaluated
        if source is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT_DEM))
        
        layer = self.parameterAsVectorLayer(
            parameters,
            self.INPUT_SEALEVEL,
            context
        )

        curve = {}
        request = QgsFeatureRequest()
        clause = QgsFeatureRequest.OrderByClause(QgsExpression('to_real(age)'), ascending=True)
        orderby = QgsFeatureRequest.OrderBy([clause])
        request.setOrderBy(orderby)

        for feature in layer.getFeatures(request):
            age = float(feature["age"])
            level = float(feature["sea_level"])
            curve[age] = level
            
        oldest = 65
        youngest = 0
        bin_width = 1

        max_sea_level =  math.ceil(max(curve.values()))
        min_sea_level = math.floor(min(curve.values()))

        x = list(range(youngest, oldest+1, 1))
        y = np.interp(x, list(curve.keys()), list(curve.values()))
        curve = dict(zip(x, y))

        s = range(min_sea_level,max_sea_level+1, bin_width)
            
        duration, depths = np.histogram(tuple(curve.values()), bins=s)
        duration = np.cumsum(duration)

        table = []

        table.append(-9999)
        table.append(depths[0])
        table.append(0)

        for n in range(0,len(duration), 1):
            table.append(depths[n])
            table.append(depths[n+1])
            table.append(duration[n])

        table.append(depths[len(duration)])
        table.append(9999)
        table.append(oldest)
            
        table = list(map(int, table))
        
        result = processing.run(
            'native:reclassifybytable', {
                'INPUT_RASTER' : source,
                'RASTER_BAND':1,
                'TABLE': table,
                'NO_DATA':-9999,
                'RANGE_BOUNDARIES':0,
                'NODATA_FOR_MISSING':True,
                'DATA_TYPE':5,
                'OUTPUT': parameters['OUTPUT']
                },
                is_child_algorithm=True, context=context, feedback=feedback)
        
        if feedback.isCanceled():
            return {}

        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {self.OUTPUT: result['OUTPUT']}
    