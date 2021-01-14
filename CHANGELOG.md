# Version 1.1.0 - Unreleased

**Related Pull Request**: [#87](https://github.com/DataONEorg/collections-portals-schemas/pull/87)

**Related Milestone**: [1.1.0](https://github.com/DataONEorg/collections-portals-schemas/milestone/4)

**More Info:**
- For examples that make use of the new filter and definition capabilities, see `docs/examples/example-definitions-to-solr.md`.
- To see a visualization of the current schema, open `docs/web/index.html` in a browser.
- To see the options MetacatUI uses under the current version of the schema, see `docs/options-for-MetacatUI.md`

## 📖 Support for more complex definitions ([#70](https://github.com/DataONEorg/collections-portals-schemas/issues/70))

- The type used for the portal and collection `<definition>` element has been renamed from `DefinitionType` to `FilterGroupType` to better characterize the definition's expanded capabilities.
- In addition to the `<filter>`, `<dateFilter>`, `<numericFilter>`, and `<booleanFilter>` elements that the `DefinitionType` comprised, the replacement `FilterGroupType` may now also contain an optional `<operator>` and `<exclude>` element, as well as multiple `<filterGroup>` elements.
- `<filterGroup>` elements are also of type `FilterGroupType`. This means that definitions can now contain nested filter groups.
- `<operator>` is used to specify how the filters in the definition should be combined to create the definition query. Previously, it was up to the parser to determine whether the filters should be `AND`'ed or `OR`'ed together (MetacatUI used `AND` in most cases, but `OR` for some special cases).
- `<exclude>` is used to negate the entire filter group. Setting `exclude` to true means that any datasets that would match the query defined by the filter group should be omitted from the results.

## 🔘 Specify a different filter operator for fields vs values ([#83](https://github.com/DataONEorg/collections-portals-schemas/issues/83), [#84](https://github.com/DataONEorg/collections-portals-schemas/issues/84))
  - In addition to the `<operator>` already included in `<filter>` elements, filters may now also contain a `<fieldsOperator>` element. The `<operator>` is used to specify how multiple `<value>` elements should be joined, while the `<fieldsOperator>` is used to specify how multiple `<field>` elements should be joined. Previously, it was up to the parser to determine whether the AND or OR set in `<operator>` should be applied to both values and fields when creating a query (MetacatUI was applying operator to both).

## 📑 New and improved portal sections ([#85](https://github.com/DataONEorg/collections-portals-schemas/issues/85), [#79](https://github.com/DataONEorg/collections-portals-schemas/issues/79), [#80](https://github.com/DataONEorg/collections-portals-schemas/issues/80))
  - The `<content>` element in `ContentSectionType` is now optional (previously one was required)
  - The `<content>` element has also been switched from the EML `txt:TextType` to a `complexType` that accepts any number of `xs:any` elements with "lax" content processing. This allows for the development of more complex section types that can render content other than just markdown.
  - MetacatUI will take advantage of these more flexible section elements by:
    - Explicitly defining Metrics and Data sections as `<section>` elements, rather than using a portal `<option>` element to show or hide them.
    - Metric and Data sections will then be able to make use of the section's `<label>`, `<title>`, and `<introduction>` elements, allowing users to change the name and introductory text of their Metrics and Data sections.
    - The type of section will be specified using the `<option>` element within the `<section>`
    - Any `<option>` elements that are set in the root `<portal>` element but that are specific to the Metrics or Data Sections will be moved to within the relevenat `<section>` element
    - Sections will be ordered using the same order that the `<section>` elements appear in the XML, or will otherwise use an `<option>` element for placement

## 📚 Schema & Portal documentation ([#90](https://github.com/DataONEorg/collections-portals-schemas/issues/90))

- The Collections and Portals schemas are now documented using HTML documents found in the `docs/web/schema` directory(these can be run locally), as well as the diagrams found in the `/img` sub-directory.
- Added more `appinfo` documentation to elements

## ⭐️ Minor enhancements:

- Allow an image, icon, and description for each `<choice>` element within `ChoiceType`, as well as for both the true (`<trueOptions>`) and the false (`<falseOptions>`) options in `UIToggleFilterType` elements. - [#78](https://github.com/DataONEorg/collections-portals-schemas/issues/78)
- Allow `<image>` and `<option>` elements within `<associatedParty>` - [#86](https://github.com/DataONEorg/collections-portals-schemas/issues/86)
- Allow `<option>` elements in UIFilterGroupsType (i.e. the custom search filter `<filterGroups>`)
- Make indentation and white space consistent
