import os
import xml.etree.ElementTree as ET

# Define the directory containing the XML files
xml_dir = './exemple'

# Get a list of all the XML files in the directory
xml_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]

# Create a new root element to hold the merged data
merged_root = ET.Element('merged')

# Loop through each XML file and merge its data into the new root element
for xml_file in xml_files:
    # Parse the XML file and get its root element
    xml_tree = ET.parse(os.path.join(xml_dir, xml_file))
    xml_root = xml_tree.getroot()

    # Loop through each child element of the root element and append it to the new root element
    for child in xml_root:
        merged_root.append(child)

# Create a new XML tree with the merged root element
merged_tree = ET.ElementTree(merged_root)

# Write the merged XML tree to a file
merged_tree.write('merged.xml', encoding='utf-8', xml_declaration=True)
