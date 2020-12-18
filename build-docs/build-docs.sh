#!/bin/bash

# This file has been modified from NCEAS's EML build script, see:
# https://github.com/NCEAS/eml/blob/master/bin/build_schema_documentation.sh

# usage: ./build-docs/build-docs.sh
# run script from the root of the Collections & Portals schemas directory
 
# actions:
# 1. runs a transform on all the schema files, to prep them for buiding documentation

# 2. runs the Oxygen documentation generator. assumes you have a license for both Oxygen Editor and Oxygen Scripting

# 3. copies O2 output to the $ROOT/docs/schema

# 4. Removes tmp files

set -e
set -o pipefail

# The location of the .XSD schema files
INPUT='./schemas';
# A temporary directory that this script will remove at the end
TMP_OUT='./tmp';

if [[ ! -d $TMP_OUT ]]; then
	mkdir $TMP_OUT;
fi

TEMPLATE='./build-docs/app-info-to-doc.xsl';

# Path to Oxygen's schemaDocumentation script, may vary
O2_SCRIPT='/Applications/oxygen/scripts/schemaDocumentation.sh';

# Oxygen script will place its output at this dir, starting from same dir that contains the input xsd.
# only seem to be able to control output to a dir below the dir holding the xsd files
# we will use the dir name later, to move output
O2_OUTPUT_DIR='docs';

# The name of the documentation index file right now is called "index.html".
O2_OUTPUT_INDEX='index.html';
O2_OUTPUT="$O2_OUTPUT_DIR/$O2_OUTPUT_INDEX";

# locaton of final documentation (note that this is anchored at PWD, root of the checkout)
OUTPUT='./docs/web';

# loop through schema files and xform
COUNTER=0;

# 1. for Oxygen, transform the xsd files, moving appinfo node to documentation, with basic text formatting (see xsl)
for inputfile in "$INPUT"/*xsd;

do
	# echo $inputfile;
	filename=$(basename "$inputfile");
	echo "$filename"; 
	xsltproc "$TEMPLATE" "$INPUT/$filename" > "$TMP_OUT/$filename"
	(( COUNTER ++ ));
done

echo "processed $COUNTER files from $INPUT to $TMP_OUT using $TEMPLATE"; echo;

# run the Oxygen XML editor's documenation generator and put output in a tmp area that mirrors the docs dir 
echo "O2_OUTPUT = $O2_OUTPUT";
"$O2_SCRIPT" "$TMP_OUT/portals.xsd" -cfg:build-docs/oxygen_documentation_settings.xml

# copy O2 output to the main documentation area
if [[  -d $OUTPUT ]]; then
	rm -r "$OUTPUT"
fi
cp -r "$TMP_OUT/$O2_OUTPUT_DIR" "$OUTPUT" ;
echo "cp -r $TMP_OUT/$O2_OUTPUT_DIR $OUTPUT ";
echo "Top of schema documentation is $OUTPUT/$O2_OUTPUT_INDEX ";


# # tmp files are not tracked in git.
rm -r "$TMP_OUT"
