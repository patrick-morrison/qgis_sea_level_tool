---
title: 'Sea Level Tool: A QGIS Plugin for Dynamic Paleo-Sea Level Visualization and Analysis'
tags:
  - Python
  - QGIS
  - sea level
  - palaeoclimate
  - archaeology
  - geomorphology
  - palaeography
authors:
  - name: Patrick Morrison
    orcid: 0000-0000-0000-0000  # TODO: replace with your ORCID
    affiliation: 1
affiliations:
  - name: University of Western Australia, Perth, Australia
    index: 1
date: 27 March 2026
bibliography: paper.bib
---

# Summary

The Sea Level Tool is a plugin for QGIS that enables dynamic visualization of past sea levels by linking a sea level curve (a time series of sea level positions in kiloyears and metres) to a digital elevation model (DEM). The plugin adjusts the colour rendering of a raster layer in real time to reflect the land-sea boundary at any given point in time, allowing researchers to interactively explore paleo-coastlines across any region of the world. A suite of three QGIS Processing algorithms extends this functionality to batch spatial analysis, computing metrics such as subaerial exposure duration, shoreline persistence, and inundation timing across user-defined time ranges and sea level curves.

# Statement of Need

During glacial periods, global mean sea levels were substantially lower than today — reaching approximately 120 m below present at the Last Glacial Maximum (~20 ka) — exposing vast areas of continental shelf as dry land [@lambeck2014sea]. These submerged landscapes are of central interest in coastal archaeology, paleogeography, marine geology, and palaeoclimatology. Reconstructing the environments of these lost landscapes requires researchers to visualize shifting coastlines, estimate the duration of coastal exposure, and identify areas of particular archaeological or ecological significance.

Existing approaches typically require researchers to manually reclassify raster layers for each time step, write custom scripts, or use specialized modelling software that does not integrate with mainstream GIS workflows. These approaches are time-consuming, require programming proficiency, and do not support interactive exploration. No purpose-built, open-source GUI tool has been available that connects sea level curve data to live raster visualization within a desktop GIS environment.

The Sea Level Tool fills this gap. It provides an accessible, interactive interface within QGIS — the world's leading open-source desktop GIS [@qgis] — enabling researchers across disciplines to explore paleo-coastlines, produce animated maps, and compute spatial indices without requiring programming expertise.

# State of the Field

Several tools address aspects of sea level visualization and analysis, but none combine interactive GUI-driven exploration with GIS-based spatial analysis in the manner provided here.

The Generic Mapping Tools (GMT) [@wessel2019gmt] and its Python interface PyGMT are widely used for high-quality map production and support elevation-based visualizations, but they are scripting environments and do not support interactive, real-time sea level adjustment tied to a palaeoclimate curve. GRASS GIS provides the `r.lake` module for static inundation modelling [@neteler2008grass], but this is designed for individual scenarios rather than time-series exploration. QGIS's built-in Temporal Controller supports time-based layer visibility but requires pre-rendered raster layers for each time step and cannot perform dynamic symbolization from a sea level curve.

Bespoke Python or MATLAB scripts are common in the literature for specific sea level analyses, but these are rarely general-purpose tools and require adaptation for new study areas. The Sea Level Tool is designed as a general, reusable plugin that any researcher can apply to their own DEM and sea level curve of choice.

# Software Design

The Sea Level Tool is implemented as a Python plugin for QGIS using the PyQGIS API. The core visualization mechanism adjusts the minimum and maximum stretch values of a raster layer's singleband pseudocolour renderer in real time, shifting the colour ramp relative to the current sea level. Sea level curves are loaded as CSV files (with `age` in kiloyears and `sea_level` in metres) and visualized in an embedded PyQtGraph plot [@campagnola2012pyqtgraph]. The interface provides synchronized sliders and spinboxes for both sea level and age, with optional linear interpolation to support century-resolution animation.

An animation function renders sequential PNG frames across a user-defined time range from either the QGIS map canvas or a custom print layout, supporting dynamic variable expressions for map titles and annotations (e.g., `[% @age %]ka`). Four predefined colour styles (natural, earth, discrete, satellite) are provided, each pre-calibrated for sea level visualization.

Three QGIS Processing algorithms are included for batch raster analysis:

- **Subaerial Duration**: computes the cumulative time (in kiloyears) each raster cell was above sea level within a user-defined time range.
- **Shoreline Duration**: identifies cells that fell within a user-defined elevation window of the sea surface, highlighting areas of persistent coastal occupation.
- **Last Exposure**: calculates the most recent age at which each cell was subaerially exposed, providing a spatially continuous minimum-age surface for archaeological and geological interpretation.

All three algorithms accept any sea level curve loaded as a QGIS vector layer, allowing substitution of different regional or eustatic reconstructions [@grant2012rapid; @lambeck2014sea].

# Research Impact

The Sea Level Tool has been applied to the study of Australia's submerged continental shelves, including visualization of the Bass Strait land bridge connecting Tasmania to mainland Australia during glacial maxima, and analysis of drowned landscapes relevant to the initial peopling of Sahul. Integration with the SahulArch archaeological database has been used to map the relationship between site ages and contemporary shoreline positions. The plugin has been distributed through the QGIS Plugin Repository and has been used by researchers at Australian universities.

# AI Disclosure

<!-- TODO: If any generative AI tools were used in developing the software or writing this paper, describe their use here. If no AI tools were used, this section may be removed. -->

# Acknowledgements

The author thanks the QGIS Development Team and the developers of PyQtGraph for the foundational software on which this plugin is built, and the authors of the sea level reconstructions used in testing and demonstration.

# References
