# Building the Collections & Portals schema documentation

The `build-docs` directory contains files required to create documentation for the Collection and Portals schemas. The instructions below show to to generate the HTML and image files contained in the `docs/web` directory.

## Requirements

To build this documentation, you will need the following:

1. [Oxygen **All Platforms** distribution (Windows, Linux/Unix, etc)](https://www.oxygenxml.com/xml_editor/download_oxygenxml_editor.html?os=Other), version 23.0. Only the distribution for all platforms contains the `schemaDocumentation.sh` script we need to build the documentation. See installation instructions for each platform further down on the download page.
2. [Java](https://www.java.com/en/) installed, in order to install Oxygen.
3. A license for Oxygen XML Editor. A [30 day trial](https://www.oxygenxml.com/xml_editor/register.html) is available.
4. An Oxygen Scripting license. Trial scripting licenses are available by request by emailing sales@oxygenxml.com. Copy your Oxygen Scripting license key in a file named `scriptinglicensekey.txt` and save it in the main application directory (the parent directory of Oxygen's "scripts" directory).

## How to build the docs after making edits to the Collections or Portals schemas

1. Check that the value set for `O2_SCRIPT` in the `build-docs.sh` file is correct. This path should lead to the `schemaDocumentation.sh` shell script that comes with the "All Platforms" distribution of Oxygen.
2. From the root of the `collections-portals-schemas` directory, run the build script: `./build-docs/build-docs.sh`
 
## Resources:

- The build scripts used here were based off of those in [NCEAS's EML repository](https://github.com/NCEAS/eml)
- [Scripting Oxygen documentation](https://www.oxygenxml.com/doc/versions/23.0/ug-editor/topics/scripting_oxygen.html)
- [Webinar: Automate XML processing with Oxygen XML Scripting](https://www.oxygenxml.com/events/2020/webinar_automate_xml_processing_with_oxygen_xml_scripting.html)