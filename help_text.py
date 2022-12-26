help_text = """<html>
<h1>Sea Level Tool</h1>

This is designed to take styled bathymetry and convert it into dynamic sea level maps. Created by Patrick Morrison 2022.

<ol>
    <li>Style DEM with singleband pseudocolour, in a way that represents the shoreline at present.</li>
    <li>Select the DEM with the elevation dropdown.</li>
    <li>Change vertical slider to move sea level.</li>
</ol>

You can also use a sea level curve.
I've built a basic one in, but you can load any csv by dropping it onto the canvas.
It must have the headings "age" and "sea_level", in ka and metres.

<ol>
    <li>Create csv with "age" and "sea_level".</li>
    <li>Drop it into main QGIS canvas.</li>
    <li>Select the layer with the curve dropdown.</li>
    <li>Change horizonal slider to move sea level with age.</li>
    <li>Toggle 'Interp.' checkbox for linear interpolation by thousand years.</li>
</ol>

The default curve is:
{0: 0, 10:0, 20:-120, 30:-100, 40:-80,50:-70,60:-70,70:-80,80:-50,90:-50,100:-30,110:-50,120:-10,130:5}
<table>
    <tr>
      <td>age</td>
      <td>sea_level</td> 
    </tr>
    <tr>
      <td>0</td>
      <td>0</td> 
    </tr>
    <tr>
        <td>10</td>
        <td>0</td> 
    </tr>
      <tr>
        <td>20</td>
        <td>120</td> 
      </tr>
      <tr>
        <td>30</td>
        <td>120</td> 
      </tr>
      <tr>
        <td>40</td>
        <td>-80</td> 
      </tr>
      <tr>
        <td>50</td>
        <td>-70</td> 
      </tr>
      <tr>
        <td>60</td>
        <td>-70</td> 
      </tr>
      <tr>
        <td>70</td>
        <td>-80</td> 
      </tr>
      <tr>
        <td>80</td>
        <td>-50</td> 
      </tr>
      <tr>
        <td>90</td>
        <td>-50</td> 
      </tr>
      <tr>
        <td>1000</td>
        <td>-30</td> 
      </tr>
      <tr>
        <td>110</td>
        <td>-50</td> 
      </tr>
      <tr>
        <td>120</td>
        <td>-10</td> 
      </tr>
      <tr>
        <td>120</td>
        <td>5</td> 
      </tr>
  </table>
  </html>"""
