import sys
import os
import re
import hashlib
import xml.etree.ElementTree as ET

# Initiate annotation input file
annot_file = ''
# Define annotation folder
annot_folder = '' # replace with annotation local folder
# Define result folder root
folder_name = 'result' # replace with target folder

def extract_content_between_heading_and_uuid(content):
    # Extract content between heading and UUID using regular expressions
    match = re.search(r'#.*\n\n(.*)\n\nUUID: `.*`', content, re.DOTALL)

    if match:
        extracted_content = match.group(1)
        return extracted_content.strip()
    else:
        return None

def write_md_file(filename, uuid, title, author, content_text, target_text):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"---\n")
            file.write(f"type: book-annotation\n")
            file.write(f'''book-title: "{title}"\n''')
            file.write(f'''book-author: "{author}"\n''')
            file.write(f'''title: "{content_text}"\n\n''')
            file.write(f"tags: []\n")
            file.write(f"---\n")
            file.write(f"# {content_text}\n\n")
            file.write(f"{target_text}\n\n\n")   
            file.write(f"UUID: `{uuid}`\n\n")

# Read input line by line
for line in sys.stdin:
    # Process each line (you can replace this with your processing logic)
    annot_file = line.strip()

    # Print to stdout files in process
    print(annot_file)

    annot_file_complete_name = os.path.join(annot_folder, annot_file)

    # Create the individual annotation markdown files ny parsing the xml
    if annot_file_complete_name:
        # Parse the XML data
        tree = ET.parse(annot_file_complete_name)
        root = tree.getroot()

        # Find the title of the publication
        nsmap = {'dc': 'http://purl.org/dc/elements/1.1/'}
        title = root.find(".//dc:title", namespaces=nsmap).text
        xmlns = root.tag.split('}')[0][1:]

        # Find author from creator
        author = root.find(".//dc:creator", namespaces=nsmap).text


        # Define the namespaces
        namespaces = {
            'xmlns': xmlns,
            'dc': 'http://purl.org/dc/elements/1.1/'
        }


        # Iterate over annotation elements
        for annotation in root.findall(".//xmlns:annotation", namespaces=namespaces):
            # Extract UUID
            uuid_element = annotation.find(".//dc:identifier", namespaces=namespaces)
            if uuid_element is not None:
                uuid = uuid_element.text.split(":")[-1]

            # Extract text under <annotation><target>
            target_text_element = annotation.find(".//xmlns:target/xmlns:fragment/xmlns:text", namespaces=namespaces)
            if target_text_element is not None:
                target_text = target_text_element.text.strip()

            # Extract text under <annotation><content>
            content_text_element = annotation.find(".//xmlns:content/xmlns:text", namespaces=namespaces)
            if content_text_element is not None:
                content_text = content_text_element.text.strip()

            # Save data to Markdown file
            # 1. Check if the file already exists
            filename = os.path.join(folder_name, f"{uuid}.md")
            if os.path.exists(filename):
                # 1.a. Read the existing file's content
                with open(filename, 'r', encoding='utf-8') as existing_file:
                    existing_content = existing_file.read()
                
                # 1.b.Compare target text content only
                sha256_existing = hashlib.sha256(extract_content_between_heading_and_uuid(existing_content).encode()).hexdigest()
                sha256_new = hashlib.sha256(target_text.encode()).hexdigest()
                if sha256_existing != sha256_new:
                    # 1.c. Update file name appending suffix (1) 
                    filename = os.path.join(folder_name, f"{uuid} (1).md")
                    write_md_file(filename, uuid, title, author, content_text, target_text)

            else:
                filename = os.path.join(folder_name, f"{uuid}.md")
                write_md_file(filename, uuid, title, author, content_text, target_text)
     



