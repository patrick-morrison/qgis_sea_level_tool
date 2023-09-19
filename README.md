# QGIS Sea Level Tool Plugin
This is designed to take styled bathymetry and convert it into dynamic sea level maps.
Created by Patrick Morrison 2022.

## Installation

This plugin can be installed using the latest release on Github. In the QGIS plugin manager, install from a zip. It will hopefully soon be available from the QGIS Plugins Repository.
Embeds pyqtgraph https://www.pyqtgraph.org.

## Data
You will need a sea level curve and a digital elevation model (DEM). 
There is an example curve included in this repository - a eustatic curve from the Red Sea. It was adapted from the supplementary materials of Grant et al. 2012: https://doi.org/10.1038/nature11593.

A great source of bathymetry data is GEBCO. They have a tool to download data: https://www.gebco.net/data_and_products/gridded_bathymetry_data/

## Getting started
- Drag the DEM into the canvas
- Select the DEM with the elevation dropdown.
- Style DEM with singleband pseudocolour, in a way that represents the shoreline at present.
- or, optionally there there is a style button with three presets.
- Change vertical slider to move sea level.

![dem2](https://user-images.githubusercontent.com/2309844/229721275-7a5a846a-eb3b-41a4-b81b-3703103703b6.gif)

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
 
![curve2](https://user-images.githubusercontent.com/2309844/229721327-4929743b-9abe-4f06-93f3-55e83b5ef8b8.gif)

The default curve is:
{0: 0, 10:0, 20:-120, 30:-100, 40:-80,50:-70,60:-70,70:-80,80:-50,90:-50,100:-30,110:-50,120:-10,130:5}

or as a table:

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

![animate2](https://user-images.githubusercontent.com/2309844/229721371-5c33e0c0-00d8-4210-ad71-b7d86b694b3e.gif)

- change dropdown to a custom print layout for dynamic titles, scale bars etc.
  - this print layout can also use dynamic titles: Age: [% @age %]ka Sea level:[% @sea_level %]m 
  - note this will cause QGIS to freeze until it is done, check the folder to see the images being rendered.
  - century resolution is recommended for these animations to make a smooth video.
  
![print2](https://user-images.githubusercontent.com/2309844/229721413-0dc216ea-cae3-447e-813a-c70b42ae163f.gif)

An example ffmpeg command to render this into a video is:
```
cat $(find . -maxdepth 1 -name "*.png" | sort -V -r) |
  ffmpeg -framerate 25 -i - -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p sea_level_video.mp4
```

Turn them into gifs:
```
ffmpeg -i sea_level_video.mp4 -vf "fps=10,scale=1080:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" tasmania.gif
```
Tasmania since the last glacial maximum (22ka). Note the land bridge that was present in the ice age, and how islands were formed as the sea level rose.

![tasmania2](https://user-images.githubusercontent.com/2309844/229721573-6b63f31d-02ee-43b3-a18e-a2bb6585b963.gif)

## Completely flexible
Any elevation layer you can draw in QGIS, you can explore and animate. What if we wanted to take the new Geoscience Australia DEM of the Bass Strait, style it naturally, add a reliefshade with Eduard, and and combine it with the Lambeck 2014 sea level curve? That's easy! This took 10 minutes:

![tasmania_highres2](https://user-images.githubusercontent.com/2309844/229951927-e374b4af-06e6-41e9-b633-5e988b1c1c16.gif)

## Sea level processing algorithms

From 1.3 the plugin includes processing algorithms for combining sea level curves and bathymetry into key indicies. 

- Subaerial duration calculates the amount of time a place was exposed (and not underwater).
- Shoreline duration visualises sea level bins - to highlight long-term coastal features.
- Last exposed calculates the most recent age a place was above water - which can help track the timing of inundation, and provides a minimum age for any sites.

![subaerial loop](https://github.com/patrick-morrison/qgis_sea_level_tool/assets/2309844/0dd903a8-5d0d-407e-a3fd-713c069944bb)


It is possible to make profiles through these products using the elevation profile tool. The gif below shows subaerial duration in green, and the shoreline positions in blue.

![profiles_loop](https://github.com/patrick-morrison/qgis_sea_level_tool/assets/2309844/d2d2211a-0848-4943-bf11-9da11a7f5aa2)


## Linking other features

The animation below using the SahulArch OSL, TL and Radiocarbon collections to visualise site. 
We can make sites show only if their radiocarbon age is with 5,000 years using this function on transparency:

```
(5000-(abs("C14 AGE"- @age*1000)))/50
```

Or in this case, we can make them accumulate by age:

```
(5000-(@age*1000-"C14_AGE"))/50
```

![first peopling loop](https://github.com/patrick-morrison/qgis_sea_level_tool/assets/2309844/b3dabb15-02a2-4e19-baca-ff6b35781203)





