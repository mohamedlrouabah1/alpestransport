import xml.etree.ElementTree as ET

tree = ET.parse('arrets.xml')
root = tree.getroot()

# Get headers
headers = ['Name', 'longitude', 'latitude', 'TransportMode', 'StopPlaceType']

# Open CSV file for writing
with open('csv_STAS/arrets.csv', 'w') as f:
    # Write headers to CSV file
    f.write(','.join(headers) + '\n')

    # Loop over members
    for member in root.findall('.//{http://www.netex.org.uk/netex}members/*'):
        row = []

        # Get Name
        name = member.find('./{http://www.netex.org.uk/netex}Name').text
        row.append(name)

        # Get Location
        location = member.find('{http://www.netex.org.uk/netex}Centroid/{http://www.netex.org.uk/netex}Location/{http://www.opengis.net/gml/3.2}pos').text
        if location is not None:
            longitude, latitude = location.split()
            row.extend([longitude, latitude])
        else:
            row.extend(['', ''])

        # Get TransportMode
        transport_mode = member.find('./{http://www.netex.org.uk/netex}TransportMode').text
        row.append(transport_mode)

        # Get StopPlaceType
        stop_place_type = member.find('./{http://www.netex.org.uk/netex}StopPlaceType')
        if stop_place_type is not None:
            row.append(stop_place_type.text)
        else:
            row.append('')

        # Get ID, SrsName, and Version
        id = member.get('id')
        version = member.get('version')
        row.extend([id, version, ''])

        # Write row to CSV file
        f.write(','.join(row) + '\n')