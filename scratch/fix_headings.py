import re

def fix_numbered_headings(content):
    lines = content.splitlines()
    fixed_lines = []
    
    for line in lines:
        # Match headings like #### Title 5.1.4 RestOfTitle
        match = re.match(r'^(#{1,6})\s+(.*?)(\d+\.\d+\.\d+)\s+(.*)', line)
        if match:
            level = match.group(1)
            prefix = match.group(2).strip()
            number = match.group(3).strip()
            suffix = match.group(4).strip()
            
            new_line = f"{level} {number} {prefix} {suffix}"
            fixed_lines.append(new_line)
        else:
            fixed_lines.append(line)
            
    return "\n".join(fixed_lines)

if __name__ == "__main__":
    file_path = "/Users/flyngcoq/AI_Project/40_Projects/Work/Safe_AI/인공지능_AI_보안_안내서-2.md"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = fix_numbered_headings(content)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Numbered headings fixed.")
