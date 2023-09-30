import xml.etree.ElementTree as ET

# Define the file path
file_path = ''  # Replace with the actual file path

# Parse the XML data
tree = ET.parse(file_path)
root = tree.getroot()

# Find the title of the publication
nsmap = {'dc': 'http://purl.org/dc/elements/1.1/'}
title = root.find(".//dc:title", namespaces=nsmap).text
xmlns = root.tag.split('}')[0][1:]


# Define the namespaces
namespaces = {
    'xmlns': xmlns,
    'dc': 'http://purl.org/dc/elements/1.1/'
}


# Print the title
print(f"Title: {title}")
print(f"xmlns: {xmlns}")

# Iterate over annotation elements
for annotation in root.findall(".//xmlns:annotation", namespaces=namespaces):
    # Extract UUID
    uuid_element = annotation.find(".//dc:identifier", namespaces=namespaces)
    if uuid_element is not None:
        uuid = uuid_element.text.split(":")[-1]
        # Print UUID
        print(f"UUID: {uuid}")

    # Extract text under <annotation><target>
    target_text_element = annotation.find(".//xmlns:target/xmlns:fragment/xmlns:text", namespaces=namespaces)
    if target_text_element is not None:
        target_text = target_text_element.text.strip()
        # Print Target Text
        print(f"Target Text: {target_text}")

    # Extract text under <annotation><content>
    content_text_element = annotation.find(".//xmlns:content/xmlns:text", namespaces=namespaces)
    if content_text_element is not None:
        content_text = content_text_element.text.strip()
        # Print Content Text
        print(f"Content Text: {content_text}")





