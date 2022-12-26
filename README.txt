# Sea Level Tool
This is designed to take styled bathymetry and convert it into dynamic sea level maps.
Created by Patrick Morrison 2022.

- Style DEM with singleband pseudocolour, in a way that represents the shoreline at present.
- or, optionally there there is a style button with three presets.
- Select the DEM with the elevation dropdown.
- Change vertical slider to move sea level.

You can also use a sea level curve.
I've built a basic one in, but you can load any csv by dropping it onto the canvas.
It must have the headings "age" and "sea_level", in ka and metres.

- Create csv with "age" and "sea_level".
- Drop it into main QGIS canvas.
- Select the layer with the curve dropdown.
- Change horizonal slider to move sea level with age.
- Toggle 'Interp.' checkbox for linear interpolation by thousand years.

The default curve is:
{0: 0, 10:0, 20:-120, 30:-100, 40:-80,50:-70,60:-70,70:-80,80:-50,90:-50,100:-30,110:-50,120:-10,130:5}

There is also an animation function, which will render the map canvas, or a layout.
It iterates through every thousand years from the max or min.
With sea level curve and bathymetry loaded:
- choose max and min ages
- use 'save as...' button to choose file
- animate from canvas to check it is working
- change dropdown to a custom layout for dynamic titles, scale bars etc.

Requires pyqtgraph: https://landscapearchaeology.org/2018/installing-python-packages-in-qgis-3-for-windows/

