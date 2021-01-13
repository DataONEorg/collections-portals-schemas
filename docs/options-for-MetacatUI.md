# Options for displaying portals that are supported by MetacatUI

The following document describes options that affect the display of portals in [MetacatUI](https://github.com/NCEAS/MetacatUI). For the most up-to-date list, see [MetacatUI documentation](https://nceas.github.io/metacatui/).

`<option>` elements can be included **within** the following elements:

- `<portal>` (root)
- `<section>`
- `<associatedParty>`
- any of the `UIOptionsType` type elements that are included in `UIFilterType` elements: 
    - `<filterOptions>` (within types `UIFilterType`, `UIDateFilterType`, and `UIBooleanFilterType`)
    - `<trueOptions>` and `<falseOptions>` (within type `UIToggleFilterType`)
    - `<choiceOptions>` (within type `ChoiceType`, used as a `<choice>` element within `UIChoiceFilterType`)
- `<filterGroup>` of type `<UIFilterGroupType>`

`<option>` elements are of type `OptionType`, and follow the structure

```
<option>
  <optionName></optionName>
  <optionValue></optionValue>
</option>
```

Currently, MetacatUI makes use of options set in the `<portal>` and `<section>` elements.

## Portal options

### Color

The following display options can be set within the `<portal>` (root) element. These options are parsed by MetacatUI to determine the color to use in displaying the portal and the portal builder.

| optionName | optionValue | Description |
|------------|-------------|-------------|
| primaryColor | Hex color code | The most frequent color, represented via hexadecimal color code, to use in the portal page UI |
| secondaryColor | Hex color code | The second most frequent color, represented via hexadecimal color code, to use in the portal page UI |
| accentColor | Hex color code | The least frequent color, represented via hexadecimal color code, to use in the portal page UI |

## Section options

The options below are used by MetacatUI to determine how to render the content within each `<section>` element. These options should be set in `<section>` elements.

### Section type

MetacatUI uses the `type` option to determine what kind of page to render.

| optionName | optionValue | Description |
|------------|------------|-------------|
| type | freeform | The default - a freeform section that renders the freeform contained in the `<content>` `<markdown>` element as HTML, and may optionally include an `<image>` element to be used as a hero image for that section |
| type | metrics | Displays numbers and figures that summarize the portal's collection of data |
| type | members | Display a list of each person or organization that are defined as associatedParty elements |
| type | dataCatalog | Shows a searchable list of the portal's collection of datasets |
| type | feverVisualization | Shows a Fluid Earth Viewer |

#### Options for `dataCatalog` section types

When the section's `type` option is set to `dataCatalog`, the following additional options will affect the display of the map in this section type.

| optionName | optionValue | Description |
|------------|-------------|-------------|
| mapZoomLevel | Integer | A zoom level to use for a map |
| mapCenterLatitude | Latitude | The geographic latitude on which the map should be centered |
| mapCenterLongitude | Longitude | The geographic longitude on which the map should be centered |
| mapShapeHue | Three digit hue code | A hue to use for shape and/or marker colors on the map, represented by a 3-digit hue number. |

#### Options for `metrics` section types

TODO: We may eventually want to use metrics section options to allow users to show/hide certain metrics and data visualizations

### Section placement

MetacatUI orders sections using the same implicit ordering of `<section>` elements in the document, unless an explicit `placement` option is specified within sections. 

| optionName | optionValue | Description |
|------------|-------------|-------------|
| placement | Integer | The relative position of a section compared to other sections |

Different types of portal layouts are under development, and in those layouts, the placement option may take values such as "topLeft", "topRight", "bottomLeft", "bottomRight".