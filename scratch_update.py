import os
import re

index_path = r'c:\Users\brian\Desktop\網頁程式設計\project\static\templates\index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace `{{ url_for('to_do') }}` with `{{ url_for('goal', goal_id=X) }}`
# However, there are exactly 17 of them in the `squares` section.
# Let's find the section.
start_idx = content.find('<section class="squares" id="17goals">')
end_idx = content.find('</section>', start_idx)
section_content = content[start_idx:end_idx]

# Replace inside this section
new_section_content = section_content
for i in range(1, 18):
    # we replace only the first occurrence 17 times
    new_section_content = new_section_content.replace(
        "{{ url_for('to_do') }}", 
        f"{{{{ url_for('goal', goal_id={i}) }}}}", 
        1
    )

new_content = content[:start_idx] + new_section_content + content[end_idx:]

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated index.html successfully.")
