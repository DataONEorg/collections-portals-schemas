# Example definitions translated to Solr queries

The following examples demonstrate how a definition element should be translated into the [Solr](https://lucene.apache.org/solr/) query syntax.

Note that in these examples, as well as in [MetacatUI](https://github.com/NCEAS/MetacatUI), ` AND (-obsoletedBy:* AND formatType:METADATA)` is added to the end of all portal queries regardless of what's contained in the definition element.

## **Example 1:** A nested filter group that is excluded from the rest of the query (🆕 since version 1.1.0)

A filter group within the definition element can be used to exclude a set of results, such as data that was collected within a geographic region.

The definition below matches metadata where "ant" is a keyword and site contains the word "America", but does not have geographic coordinates that are located within a specified bounding box.

**Portal/Collection XML**
```xml
<definition>
  <filter>
    <field>siteText</field>
    <value>America</value>
    <matchSubstring>true</matchSubstring>
  </filter>
  <filter>
    <field>keywordsText</field>
    <value>ant</value>
  </filter>
  <filterGroup>
    <numericFilter>
      <field>northBoundCoord</field>
      <max>54</max>
    </numericFilter>
    <numericFilter>
      <field>eastBoundCoord</field>
      <max>-62</max>
    </numericFilter>
    <numericFilter>
      <field>southBoundCoord</field>
      <max>44</max>
    </numericFilter>
    <numericFilter>
      <field>westBoundCoord</field>
      <max>-79</max>
    </numericFilter>
    <exclude>true</exclude>
    <operator>AND</operator>
  </filterGroup>
  <operator>AND</operator>
</definition>
```

**Solr query string**
```
(
  siteText:*America* AND
  keywordsText:ant AND
  -(
    northBoundCoord:[* TO 54] AND
    eastBoundCoord:[* TO -62] AND
    southBoundCoord:[* TO 44] AND
    westBoundCoord:[* TO -79]
  )
)
AND (-obsoletedBy:* AND formatType:METADATA)
```

## **Example 2:** Different operators for the field and value elements within a filter (🆕 since version 1.1.0)

When there are multiple fields and values within a filter element, a different operator can be specified for the fields than for the values.

This definition finds metadata where either the title, abstract, or keywords contain both "climate" and "salmon".

**Portal/Collection XML**
```xml
<definition>
  <filter>
    <field>title</field>
    <field>abstract</field>
    <field>keywordsText</field>
    <operator>AND</operator>
    <value>salmon</value>
    <value>climate</value>
    <fieldsOperator>OR</fieldsOperator>
  </filter>
</definition>
```

**Solr query string**
```
(
  title:(*salmon* AND *climate*) OR
  abstract:(*salmon* AND *climate*) OR
  keywordsText:(*salmon* AND *climate*)
)
AND (-obsoletedBy:* AND formatType:METADATA)
```

Note that the same query shown above can be constructed using using multiple filters, but this method is tedious and repetitive:

**Portal/Collection XML**
```xml
<definition>
  <filter>
    <field>title</field>
    <operator>AND</operator>
    <value>salmon</value>
    <value>climate</value>
  </filter>
  <filter>
    <field>abstract</field>
    <operator>AND</operator>
    <value>salmon</value>
    <value>climate</value>
  </filter>
  <filter>
    <field>keywordsText</field>
    <operator>AND</operator>
    <value>salmon</value>
    <value>climate</value>
  </filter>
  <operator>OR</operator>
</definition>
```

## **Example 3:** Different operators within vs between filter groups (🆕 since version 1.1.0)

Complex definitions can be built by using different operators within filter groups vs. between filter groups.

The definition below matches datasets where:
1. The author's last name is "Kim" **AND** is NOT one of three specific datasets, **OR**
2. It's part of the "My Project" project **AND** has the "Special Word" keyword, **OR**
3. Is part of award #123 **AND** data was collected between the years 2013 and 2020.

**Portal/Collection XML**
```xml
<definition>
  <filterGroup>
    <filter>
      <field>authorLastName</field>
      <value>Kim</value>
    </filter>
    <filter>
      <field>identifier</field>
      <operator>OR</operator>
      <value>urn:uuid:a843239b-6d04-4019-9835-6e3c8e3418c8</value>
      <value>urn:uuid:30a28104-6814-497a-8f72-7fecb36cb721</value>
      <value>urn:uuid:83b718dd-d709-466e-bf0d-0710a71e7a20</value>
      <exclude>true</exclude>
    </filter>
    <operator>AND</operator>
  </filterGroup>
  <filterGroup>
    <filter>
      <field>projectText</field>
      <value>My Project</value>
    </filter>
    <filter>
      <field>keywordsText</field>
      <value>Special Word</value>
    </filter>
    <operator>AND</operator>
  </filterGroup>
  <filterGroup>
    <filter>
      <field>awardNumber</field>
      <value>123</value>
    </filter>
    <dateFilter>
      <field>beginDate</field>
      <field>endDate</field>
      <min>2013-01-01T00:00:00Z</min>
      <max>2020-12-31T23:59:59Z</max>
    </dateFilter>
    <operator>AND</operator>
  </filterGroup>
  <operator>OR</operator>
</definition>
```

**Solr query string**
```
(
  (
    authorLastName:Kim AND
    -(
       identifier: urn\:uuid\:a843239b-6d04-4019-9835-6e3c8e3418c8 OR
                   urn\:uuid\:30a28104-6814-497a-8f72-7fecb36cb721 OR
                   urn\:uuid\:83b718dd-d709-466e-bf0d-0710a71e7a20
    )
  )
  OR
  (
    projectText:"My Project" AND
    keywordsText:"Special Word"
  )
  OR
  (
    awardNumber:123 AND
    (
      beginDate:[2013-01-01T00:00:00Z TO 2020-12-31T23:59:59Z] AND
      endDate:[2013-01-01T00:00:00Z TO 2020-12-31T23:59:59Z]
    )
  )
)
AND (-obsoletedBy:* AND formatType:METADATA)
```
