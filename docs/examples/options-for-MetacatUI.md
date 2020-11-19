# Options for displaying portals that are supported by MetacatUI

The following document describes options that affect the display of portals in [MetacatUI](https://github.com/NCEAS/MetacatUI). For the most up-to-date list, see [MetacatUI documentation](https://nceas.github.io/metacatui/).

## Portal options

### Color

The following display options can be included in portals as `<option>` elements. These options are parsed by MetacatUI to determine the color to use in displaying the portal and the portal builder.

| optionName | optionValue | Description |
|------------|-------------|-------------|
| primaryColor | Hex color code | The most frequent color, represented via hexadecimal color code, to use in the portal page UI |
| secondaryColor | Hex color code | The second most frequent color, represented via hexadecimal color code, to use in the portal page UI |
| accentColor | Hex color code | The least frequent color, represented via hexadecimal color code, to use in the portal page UI |

## Section attributes

### type

The following values can be included in the portal section `type` attribute, and will determine how MetacatUI renders the content in each section.

| sectionType | Description |
|------------|-------------|
| freeform | The default - a freeform section that renders the freeform contained in the `<content>` `<markdown>` element as HTML, and may optionally include an `<image>` element to be used as a hero image for that section |
| metrics | Displays numbers and figures that summarize the portal's collection of data |
| members | Display a list of each person or organization that are defined as associatedParty elements |
| dataCatalog | Shows a searchable list of the portal's collection of datasets |
| feverVisualization | Shows a Fluid Earth Viewer |

### Other attributes

In all section types, set the order by adding an `order` attribute to the section element

| attributeName | optionValue | Description |
|------------|-------------|-------------|
| weight | Integer | A number indicating the importance or position of the section relative to others |

## Section options

### `dataCatalog`

When the section's `type` attribute is set to `dataCatalog`, the following options can be set in the section as `<option>` elements and will affect the display of the map in that section.

| optionName | optionValue | Description |
|------------|-------------|-------------|
| mapZoomLevel | Integer | A zoom level to use for a map |
| mapCenterLatitude | Latitude | The geographic latitude on which the map should be centered |
| mapCenterLongitude | Longitude | The geographic longitude on which the map should be centered |
| mapShapeHue | Three digit hue code | A hue to use for shape and/or marker colors on the map, represented by a 3-digit hue number. |