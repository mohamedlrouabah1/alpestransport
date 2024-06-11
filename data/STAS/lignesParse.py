import csv
import xml.etree.ElementTree as ET

# Open the NeTEx file
tree = ET.parse('lignes.xml')
root = tree.getroot()

# Open the CSV file and write headers
with open('csv_STAS/lignes.csv', mode='w') as csv_file:
    fieldnames = ['name', 'transport_mode', 'public_code', 'operator_name', 'operator_website']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Loop over all the relevant elements in the NeTEx file
    for line in root.findall(".//{http://www.netex.org.uk/netex}Line"):
        name = line.find("{http://www.netex.org.uk/netex}Name").text
        transport_mode = line.find("{http://www.netex.org.uk/netex}TransportMode").text
        public_code = line.find("{http://www.netex.org.uk/netex}PublicCode").text

        operator_name = ''
        operator_website = ''

        for operator in root.findall(".//{http://www.netex.org.uk/netex}Operator"):
            if operator.find("{http://www.netex.org.uk/netex}Name").text == 'STAS':
                operator_name = operator.find("{http://www.netex.org.uk/netex}Name").text
                operator_website = operator.find("{http://www.netex.org.uk/netex}ContactDetails/{http://www.netex.org.uk/netex}Url").text

        # Write the data to the CSV file
        writer.writerow({'name': name, 'transport_mode': transport_mode, 'public_code': public_code, 'operator_name': operator_name, 'operator_website': operator_website})
