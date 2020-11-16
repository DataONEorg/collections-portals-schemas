# Options for displaying portals that are supported by MetacatUI

The following document describes options that affect the display of portals in [MetacatUI](https://github.com/NCEAS/MetacatUI). For the most up-to-date list, see [MetacatUI documentation](https://nceas.github.io/metacatui/).

## Portal color options

The following display options can be included in portals as `<option>` elements. These options are parsed by MetacatUI to determine the color to use in displaying the portal and the portal builder.

| optionName | optionValue | Description |
|------------|-------------|-------------|
| primaryColor | Hex color code | The most frequent color, represented via hexadecimal color code, to use in the portal page UI |
| secondaryColor | Hex color code | The second most frequent color, represented via hexadecimal color code, to use in the portal page UI |
| accentColor | Hex color code | The least frequent color, represented via hexadecimal color code, to use in the portal page UI |

## Section types

The following values can be included in the portal section `<sectionType>` element, and will determine how MetacatUI renders the content or contentSource in each section.

| sectionType | Description |
|------------|-------------|
| markdown | The default - a freeform section that renders the markdown contained in the `<content>` `<markdown>` element as HTML, and may optionally include an `<image>` element to be used as a hero image for that section |
| metrics | Displays numbers and figures that summarize the portal's collection of data |
| members | Display a list of each person or organization that are defined as associatedParty elements |
| dataCatalog | Shows a searchable list of the portal's collection of datasets |
| feverVisualization | Shows a Fluid Earth Viewer and requires a `<contentSource>` element |

## Section options

When the `<sectionType>` element is set to `dataCatalog`, the following options can be set in the section as `<option>` elements and will affect the display of the map in that section.

| optionName | optionValue | Description |
|------------|-------------|-------------|
| mapZoomLevel | Integer | A zoom level to use for a map |
| mapCenterLatitude | Latitude | The geographic latitude on which the map should be centered |
| mapCenterLongitude | Longitude | The geographic longitude on which the map should be centered |
| mapShapeHue | Three digit hue code | A hue to use for shape and/or marker colors on the map, represented by a 3-digit hue number. |

## Section order

MetacatUI will display sections in the same order in which they occur in the portal document.
