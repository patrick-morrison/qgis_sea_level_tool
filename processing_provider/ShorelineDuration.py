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
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterRasterDestination,
                       QgsExpression,
                       QgsProcessingParameterNumber,
                       QgsFeatureRequest)
from qgis import processing
import numpy as np
import math


class ShorelineDuration(QgsProcessingAlgorithm):

    INPUT_DEM = 'INPUT_DEM'
    INPUT_SEALEVEL = 'INPUT_SEALEVEL'
    INPUT_YOUNGEST = 'INPUT_YOUNGEST'
    INPUT_OLDEST = 'INPUT_OLDEST'
    INPUT_BINWIDTH = 'INPUT_BINWIDTH'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ShorelineDuration()

    def name(self):
        return 'ShorelineDuration'

    def displayName(self):
        return self.tr('Shoreline Duration')


    def shortHelpString(self):
        return self.tr("""
        This algorithm calculates the time in kiloyears a pixel has been within x (bin width) metres of sea level, based on a sea level curve.
        It is intended to represent the paleo-coastal zone over time, and highlight sea level modes. Common shorelines will show up as high values. """)

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_DEM,
                self.tr('Input DEM'),
                [QgsProcessing.TypeRaster]
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
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

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_BINWIDTH,
                self.tr('Sea level bin width (m)'),
                QgsProcessingParameterNumber.Integer,
                defaultValue=5
            )
        )


        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT,
                self.tr('Shoreline duration raster')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        source = self.parameterAsRasterLayer(
            parameters,
            self.INPUT_DEM,
            context
        )

        if source is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT_DEM))
        
        layer = self.parameterAsVectorLayer(
            parameters,
            self.INPUT_SEALEVEL,
            context
        )

        bin_width = self.parameterAsInt(
            parameters,
            self.INPUT_BINWIDTH,
            context
        )

        oldest = self.parameterAsInt(
            parameters,
            self.INPUT_OLDEST,
            context
        )

        youngest = self.parameterAsInt(
            parameters,
            self.INPUT_YOUNGEST,
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
            

        x = list(range(youngest+1, oldest+1, 1))
        y = np.interp(x, list(curve.keys()), list(curve.values()))
        curve = dict(zip(x, y))

        max_sea_level =  int(math.ceil(max(curve.values())/bin_width) * bin_width)
        min_sea_level = int(math.floor(min(curve.values())/bin_width) * bin_width)

        print(curve)

        s = range(min_sea_level,max_sea_level+1, bin_width)
            
        duration, depths = np.histogram(tuple(curve.values()), bins=s)

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
        table.append(0)
            
        table = list(map(int, table))
        
        result = processing.run(
            'native:reclassifybytable', {
                'INPUT_RASTER' : source,
                'RASTER_BAND':1,
                'TABLE': table,
                'NO_DATA':-9999,
                'RANGE_BOUNDARIES':0,
                'NODATA_FOR_MISSING':True,
                'DATA_TYPE':1,
                'OUTPUT': parameters['OUTPUT']
                },
                is_child_algorithm=True, context=context, feedback=feedback)
        
        if feedback.isCanceled():
            return {}


        return {self.OUTPUT: result['OUTPUT']}
    