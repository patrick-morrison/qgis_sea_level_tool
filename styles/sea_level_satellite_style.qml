<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" maxScale="0" minScale="1e+08" version="3.28.2-Firenze" styleCategories="AllStyleCategories">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>0</Searchable>
    <Private>0</Private>
  </flags>
  <pipe>
    <provider>
      <resampling zoomedInResamplingMethod="bilinear" zoomedOutResamplingMethod="bilinear" maxOversampling="2" enabled="false"/>
    </provider>
    <rasterrenderer band="1" type="singlebandpseudocolor" opacity="1" alphaBand="-1" classificationMax="1999.8" nodataColor="" classificationMin="-3000.2">
      <rastershader>
        <colorrampshader colorRampType="INTERPOLATED" clip="0" classificationMode="1" labelPrecision="0" minimumValue="-3000.2" maximumValue="1999.8">
          <colorramp type="gradient" name="qgis_satellite_natural_v3_full">
            <Option type="Map">
              <Option type="QString" name="color1" value="8,28,52,255"/>
              <Option type="QString" name="color2" value="245,245,243,255"/>
              <Option type="QString" name="direction" value="ccw"/>
              <Option type="QString" name="discrete" value="0"/>
              <Option type="QString" name="rampType" value="gradient"/>
              <Option type="QString" name="spec" value="rgb"/>
              <Option type="QString" name="stops" value="0.000000;8,28,52,255;rgb;ccw:0.240040;11,45,77,255;rgb;ccw:0.400040;18,64,97,255;rgb;ccw:0.480040;28,95,130,255;rgb;ccw:0.540040;43,128,161,255;rgb;ccw:0.570040;62,152,181,255;rgb;ccw:0.584040;86,179,199,255;rgb;ccw:0.592040;120,203,211,255;rgb;ccw:0.596040;158,219,220,255;rgb;ccw:0.598040;187,230,228,255;rgb;ccw:0.599040;205,236,232,255;rgb;ccw:0.599640;217,240,235,255;rgb;ccw:0.600040;230,239,238,255;rgb;ccw:0.600240;238,230,211,255;rgb;ccw:0.600440;234,220,190,255;rgb;ccw:0.600640;167,187,131,255;rgb;ccw:0.606040;154,174,122,255;rgb;ccw:0.624040;138,160,107,255;rgb;ccw:0.660040;111,133,87,255;rgb;ccw:0.740040;123,106,81,255;rgb;ccw:0.840040;155,140,118,255;rgb;ccw:0.900040;208,203,196,255;rgb;ccw:1.000000;245,245,243,255;rgb;ccw"/>
            </Option>
          </colorramp>
          <item label="-3000" value="-3000" alpha="255" color="#081c34"/>
          <item label="-1000" value="-1000" alpha="255" color="#124061"/>
          <item label="-600" value="-600" alpha="255" color="#1c5f82"/>
          <item label="-150" value="-150" alpha="255" color="#3e98b5"/>
          <item label="-40" value="-40" alpha="255" color="#78cbd3"/>
          <item label="-10" value="-10" alpha="255" color="#bbe6e4"/>
          <item label="-5" value="-5" alpha="255" color="#cdece8"/>
          <item label="-2" value="-2" alpha="255" color="#d9f0eb"/>
          <item label="0" value="0" alpha="255" color="#e6efee"/>
          <item label="1" value="1" alpha="255" color="#eee6d3"/>
          <item label="2" value="2" alpha="255" color="#eadcbe"/>
          <item label="3" value="3" alpha="255" color="#a7bb83"/>
          <item label="120" value="120" alpha="255" color="#8aa06b"/>
          <item label="300" value="300" alpha="255" color="#6f8557"/>
          <item label="700" value="700" alpha="255" color="#7b6a51"/>
          <item label="1500" value="1500" alpha="255" color="#d0cbc4"/>
        </colorrampshader>
      </rastershader>
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
    </rasterrenderer>
    <brightnesscontrast gamma="1" brightness="0" contrast="0"/>
    <huesaturation grayscaleMode="0" colorizeOn="0" saturation="0" colorizeRed="255" colorizeGreen="128" colorizeBlue="128" colorizeStrength="100" invertColors="0"/>
    <rasterresampler zoomedOutResampler="bilinear" maxOversampling="2" zoomedInResampler="bilinear"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
