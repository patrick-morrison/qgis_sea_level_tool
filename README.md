# Sea Level Tool
This is designed to take styled bathymetry and convert it into dynamic sea level maps.
Created by Patrick Morrison 2022.

## Installation

This plugin can be installed using the latest release on Github. In the QGIS plugin manager, install from a zip. It will hopefully soon be available from the QGIS Plugins Repository.


## Data
You will need a sea level curve and a digital elevation model (DEM). 
There is an example curve included in this repository - a eustatic curve from the Red Sea. It was adapted from the supplementary materials of Grant et al. 2012: https://doi.org/10.1038/nature11593
A great source of bathymetry data is GEBCO. They have a tool to download data: https://www.gebco.net/data_and_products/gridded_bathymetry_data/

## Getting started
- Drag the DEM into the canvas
- Select the DEM with the elevation dropdown.
- Style DEM with singleband pseudocolour, in a way that represents the shoreline at present.
- or, optionally there there is a style button with three presets.
- Change vertical slider to move sea level.

You can also use a sea level curve.
I've built a basic one in, but you can load any csv by dropping it onto the canvas.
It must have the headings "age" and "sea_level", in ka and metres.

Red Sea level e.g.

| age   | sea_level |
|-------|-----------|
| 0     | 0         |
| 0.069 | 1.054     |
| 0.222 | 0.752     |
| 0.324 | 0.557     |
| 0.477 | 0.297     |
| 0.579 | 0.155     |
| 0.732 | -0.007    |
| 0.808 | -0.064    |
| 0.833 | -0.079    |
| 0.986 | -0.120    |

- Create csv with columns "age" and "sea_level".
- Drop it into main QGIS canvas.
- Select the layer with the curve dropdown.
- Change horizonal slider to move sea level with age.
- Toggle 'Interp.' checkbox for linear interpolation by thousand years.
- Check the 'Dec.' checkbox to increase resolution to centuries (and to increase precision on sea level). 
- In View-Decorations-Title Label you can use the sea_level and age variable to construct a dynamic map label,
 e.g.: Age: [% @age %]ka Sea level:[% @sea_level %]m 

The default curve is:
{0: 0, 10:0, 20:-120, 30:-100, 40:-80,50:-70,60:-70,70:-80,80:-50,90:-50,100:-30,110:-50,120:-10,130:5}

There is also an animation function, which will render the map canvas, or a print layout.
It iterates through every timestep from the max or min.
With sea level curve and bathymetry loaded:
- choose max and min ages
- use 'save as...' button to choose file
- animate from canvas to check it is working
- change dropdown to a custom print layout for dynamic titles, scale bars etc.
  - this print layout can also use dynamic titles: Age: [% @age %]ka Sea level:[% @sea_level %]m 
  - note this will cause QGIS to freeze until it is done, check the folder to see the images being rendered.
  - century resolution is recommended for these animations to make a smooth video.

An example ffmpeg command to render this into a video is:
```
cat $(find . -maxdepth 1 -name "*.png" | sort -V -r) |
  ffmpeg -framerate 25 -i - -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p sea_level_video.mp4
```

Embeds pyqtgraph https://www.pyqtgraph.org.

