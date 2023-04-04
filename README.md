# QGIS Sea Level Tool Plugin
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

![load_dem](https://user-images.githubusercontent.com/2309844/229714873-e9b5f389-4415-4a2d-93ed-32019ac9aa16.gif)

## Custom sea level curve

You can also use a sea level curve.
I've built a basic one in, but you can load any csv by dropping it onto the canvas.
It must have the headings "age" and "sea_level", in ka and metres.

- Create csv with columns "age" and "sea_level".
- Drop it into main QGIS canvas.
- Select the layer with the curve dropdown.
- Change horizonal slider to move sea level with age.
- Toggle 'Interp.' checkbox for linear interpolation by thousand years.
- Check the 'Dec.' checkbox to increase resolution to centuries (and to increase precision on sea level). 
- In View-Decorations-Title Label you can use the sea_level and age variable to construct a dynamic map label,
 e.g.: Age: [% @age %]ka Sea level:[% @sea_level %]m 
 
 ![custom_curve](https://user-images.githubusercontent.com/2309844/229716082-f086d113-7c42-40ef-bfb3-a680fabff732.gif)

The default curve is:
{0: 0, 10:0, 20:-120, 30:-100, 40:-80,50:-70,60:-70,70:-80,80:-50,90:-50,100:-30,110:-50,120:-10,130:5}

Red Sea level e.g.

| age   | sea_level |
|-------|-----------|
| 0     | 0         |
| 10    | 0         |
| 20    | -120      |
| 30    | -100      |
| 40    | -80       |
| 50    | -70       |
| 60    | -70       |
| 70    | -80       |
| 80    | -50       |
| 90    | -50       |
| 100   | -30       |
| 110   | -50       |
| 120   | -10       |
| 130   | 5         |

## Animation

There is also an animation function, which will render the map canvas, or a print layout.
It iterates through every timestep from the max or min.
With sea level curve and bathymetry loaded:
- choose max and min ages
- use 'save as...' button to choose file
- animate from canvas to check it is working
![export](https://user-images.githubusercontent.com/2309844/229715081-2fabaf62-a6ff-4f2c-93b1-6000430c0a51.gif)

- change dropdown to a custom print layout for dynamic titles, scale bars etc.
  - this print layout can also use dynamic titles: Age: [% @age %]ka Sea level:[% @sea_level %]m 
  - note this will cause QGIS to freeze until it is done, check the folder to see the images being rendered.
  - century resolution is recommended for these animations to make a smooth video.
  
![print_composer](https://user-images.githubusercontent.com/2309844/229715136-e6d49b37-484d-4fb5-9fc0-a4f771c03f0f.gif)

An example ffmpeg command to render this into a video is:
```
cat $(find . -maxdepth 1 -name "*.png" | sort -V -r) |
  ffmpeg -framerate 25 -i - -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p sea_level_video.mp4
```

Tasmania since the last glacial maximum (22ka). Note the land bridge that was present in the ice age, and how islands were formed as the sea level rose.
![tasmania](https://user-images.githubusercontent.com/2309844/229715622-94449889-e5fe-44ee-8949-e04cec3350c1.gif)

Embeds pyqtgraph https://www.pyqtgraph.org.

