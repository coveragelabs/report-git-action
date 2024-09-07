import markdown
import re

severity_colors_map = {
    "critical": "BrickRed",
    "high": "RedOrange",
    "medium": "Dandelion",
    "low": "ForestGreen",
    "informational": "RoyalBlue"
}

def extract_header_content(md_file):
    pattern = r"---\s*(.*?)\s*---"
    
    match = re.search(pattern, md_file, re.DOTALL)
    
    if match:
        header = match.group(1)
        
        header_dict = {}
        for line in header.splitlines():
            if line.strip(): 
                key, value = line.split(":", 1) 
                header_dict[key.strip()] = value.strip()
        
        return header_dict
    else:
        return None

def escape_latex_special_chars(text):
    return text.replace('#', '\\#')

def extract_section_content(md_file, section_title):
    pattern = rf"##\s*{re.escape(section_title)}\s*(.*?)(##|$)"

    match = re.search(pattern, md_file, re.DOTALL)

    if match:
        return match.group(1).strip()
    else:
        return None

def transform_links_to_latex(context):
    pattern = r"\[(.*?)\]\((.*?)\)"

    latex_links = re.sub(pattern, r"\\href{\2}{\\textcolor{cyan}{\1}}", context)

    latex_links = escape_latex_special_chars(latex_links)
    
    items = "\n    \\item ".join(latex_links.splitlines())
    
    return f"\\begin{{itemize}}\n    \\item {items}\n\\end{{itemize}}"

def generate_latex_content(template_file, header, description, poc, context, recommendation):
    latex_content = template_file

    transformed_context = transform_links_to_latex(context)

    placeholders = {
        "<id>": header.get('id'),
        "<title>": header.get('title'),
        "<severity>": header.get('severity').upper(),
        "<severity-color>": severity_colors_map.get(header.get('severity').lower()),
        "<category>": header.get('category'),
        "<description>": description,
        "<proof-of-concept>": poc,
        "<context>": transformed_context,
        "<recommendations>": recommendation
    }
    
    for placeholder, value in placeholders.items():
        latex_content = latex_content.replace(placeholder, value)
    
    return latex_content

def main():
    # Read the markdown file
    with open("issue.md") as f:
        md_file = f.read()

    # Parse the markdown file content
    header = extract_header_content(md_file)
    description = extract_section_content(md_file, "Description")
    poc = extract_section_content(md_file, "Proof of Concept")
    context = extract_section_content(md_file, "Context")
    recommendation = extract_section_content(md_file, "Recommendation")

    # Read the latex template
    with open("issue-latex-template.txt", "r") as f:
        template_file = f.read()
    
    # Populate the templace with the content extracted from the markdown
    content = generate_latex_content(template_file, header, description, poc, context, recommendation)

    print(content)

    # Write the populated template to a new tex file
    with open("issue.tex", "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()