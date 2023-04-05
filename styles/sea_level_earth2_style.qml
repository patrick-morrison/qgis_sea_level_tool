<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" maxScale="0" minScale="1e+08" version="3.28.2-Firenze" styleCategories="AllStyleCategories">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>0</Searchable>
    <Private>0</Private>
  </flags>
  <temporal mode="0" fetchMode="0" enabled="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <elevation band="1" zoffset="0" symbology="Line" enabled="0" zscale="1">
    <data-defined-properties>
      <Option type="Map">
        <Option type="QString" name="name" value=""/>
        <Option name="properties"/>
        <Option type="QString" name="type" value="collection"/>
      </Option>
    </data-defined-properties>
    <profileLineSymbol>
      <symbol clip_to_extent="1" force_rhr="0" type="line" is_animated="0" name="" frame_rate="10" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" locked="0" pass="0" enabled="1">
          <Option type="Map">
            <Option type="QString" name="align_dash_pattern" value="0"/>
            <Option type="QString" name="capstyle" value="square"/>
            <Option type="QString" name="customdash" value="5;2"/>
            <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="customdash_unit" value="MM"/>
            <Option type="QString" name="dash_pattern_offset" value="0"/>
            <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="dash_pattern_offset_unit" value="MM"/>
            <Option type="QString" name="draw_inside_polygon" value="0"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="line_color" value="255,158,23,255"/>
            <Option type="QString" name="line_style" value="solid"/>
            <Option type="QString" name="line_width" value="0.6"/>
            <Option type="QString" name="line_width_unit" value="MM"/>
            <Option type="QString" name="offset" value="0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="ring_filter" value="0"/>
            <Option type="QString" name="trim_distance_end" value="0"/>
            <Option type="QString" name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="trim_distance_end_unit" value="MM"/>
            <Option type="QString" name="trim_distance_start" value="0"/>
            <Option type="QString" name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="trim_distance_start_unit" value="MM"/>
            <Option type="QString" name="tweak_dash_pattern_on_corners" value="0"/>
            <Option type="QString" name="use_custom_dash" value="0"/>
            <Option type="QString" name="width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </profileLineSymbol>
    <profileFillSymbol>
      <symbol clip_to_extent="1" force_rhr="0" type="fill" is_animated="0" name="" frame_rate="10" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleFill" locked="0" pass="0" enabled="1">
          <Option type="Map">
            <Option type="QString" name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="color" value="255,158,23,255"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="offset" value="0,0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="outline_color" value="35,35,35,255"/>
            <Option type="QString" name="outline_style" value="no"/>
            <Option type="QString" name="outline_width" value="0.26"/>
            <Option type="QString" name="outline_width_unit" value="MM"/>
            <Option type="QString" name="style" value="solid"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </profileFillSymbol>
  </elevation>
  <customproperties>
    <Option type="Map">
      <Option type="bool" name="WMSBackgroundLayer" value="false"/>
      <Option type="bool" name="WMSPublishDataSourceUrl" value="false"/>
      <Option type="int" name="embeddedWidgets/count" value="0"/>
      <Option type="QString" name="identify/format" value="Value"/>
    </Option>
  </customproperties>
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option type="QString" name="name" value=""/>
      <Option name="properties"/>
      <Option type="QString" name="type" value="collection"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling zoomedInResamplingMethod="bilinear" zoomedOutResamplingMethod="bilinear" maxOversampling="2" enabled="false"/>
    </provider>
    <rasterrenderer band="1" type="singlebandpseudocolor" opacity="1" alphaBand="-1" classificationMax="1999.8" nodataColor="" classificationMin="-3000.2">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader colorRampType="INTERPOLATED" clip="0" classificationMode="1" labelPrecision="0" minimumValue="-3000.1999999999998" maximumValue="1999.8">
          <colorramp type="gradient" name="[source]">
            <Option type="Map">
              <Option type="QString" name="color1" value="0,0,0,255"/>
              <Option type="QString" name="color2" value="255,255,255,255"/>
              <Option type="QString" name="direction" value="ccw"/>
              <Option type="QString" name="discrete" value="0"/>
              <Option type="QString" name="rampType" value="gradient"/>
              <Option type="QString" name="spec" value="rgb"/>
              <Option type="QString" name="stops" value="0.4;0,0,100,255;rgb;ccw:0.5;0,0,100,255;rgb;ccw:0.589768;42,73,150,255;rgb;ccw:0.594;45,74,144,255;rgb;ccw:0.599;71,137,208,255;rgb;ccw:0.6;150,195,222,255;rgb;ccw:0.6002;244,243,221,255;rgb;ccw:0.6004;244,243,221,255;rgb;ccw:0.6006;106,142,106,255;rgb;ccw:0.62;89,151,89,255;rgb;ccw:0.64;75,142,75,255;rgb;ccw:0.64;66,135,66,255;rgb;ccw:0.66;77,133,79,255;rgb;ccw:0.67;61,141,73,255;rgb;ccw:0.74;116,120,77,255;rgb;ccw:0.9;220,220,220,255;rgb;ccw"/>
            </Option>
          </colorramp>
          <item label="-3000" value="-3000.2000000000007" alpha="255" color="#000000"/>
          <item label="-1000" value="-1000.1999999999997" alpha="255" color="#000064"/>
          <item label="-500" value="-500.1999999999998" alpha="255" color="#000064"/>
          <item label="-51" value="-51.361999999999945" alpha="255" color="#2a4996"/>
          <item label="-30" value="-30.199999999999992" alpha="255" color="#2d4a90"/>
          <item label="-5" value="-5.200000000000002" alpha="255" color="#4789d0"/>
          <item label="0" value="-0.2" alpha="255" color="#96c3de"/>
          <item label="1" value="0.8" alpha="255" color="#f4f3dd"/>
          <item label="2" value="1.8" alpha="255" color="#f4f3dd"/>
          <item label="3" value="2.8" alpha="255" color="#6a8e6a"/>
          <item label="100" value="99.80000000000001" alpha="255" color="#599759"/>
          <item label="200" value="199.79999999999995" alpha="255" color="#4b8e4b"/>
          <item label="200" value="199.79999999999995" alpha="255" color="#428742"/>
          <item label="300" value="299.7999999999999" alpha="255" color="#4d854f"/>
          <item label="350" value="349.7999999999999" alpha="255" color="#3d8d49"/>
          <item label="700" value="699.8000000000002" alpha="255" color="#74784d"/>
          <item label="1500" value="1499.8000000000004" alpha="255" color="#dcdcdc"/>
          <item label="2000" value="1999.8000000000004" alpha="255" color="#ffffff"/>
          <rampLegendSettings useContinuousLegend="1" maximumLabel="" minimumLabel="" suffix="" orientation="2" prefix="" direction="0">
            <numericFormat id="basic">
              <Option type="Map">
                <Option type="invalid" name="decimal_separator"/>
                <Option type="int" name="decimals" value="6"/>
                <Option type="int" name="rounding_type" value="0"/>
                <Option type="bool" name="show_plus" value="false"/>
                <Option type="bool" name="show_thousand_separator" value="true"/>
                <Option type="bool" name="show_trailing_zeros" value="false"/>
                <Option type="invalid" name="thousand_separator"/>
              </Option>
            </numericFormat>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast gamma="1" brightness="0" contrast="0"/>
    <huesaturation grayscaleMode="0" colorizeOn="0" saturation="0" colorizeRed="255" colorizeGreen="128" colorizeBlue="128" colorizeStrength="100" invertColors="0"/>
    <rasterresampler zoomedOutResampler="bilinear" maxOversampling="2" zoomedInResampler="bilinear"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
