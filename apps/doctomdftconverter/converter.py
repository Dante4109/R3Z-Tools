import os
import mammoth
import html2text
from datetime import datetime

# TO-DO Add root folder path using OS 

input_dir = "exported_docs/Characters"
output_dir = "markdown_output"

input_root = "exported_docs"
output_root = "markdown_output"

os.makedirs(output_dir, exist_ok=True)

converter = html2text.HTML2Text()
converter.ignore_links = False

def process_all_files():
  for root, _, files in os.walk(input_root):
    for file in files:
        if file.lower().endswith(".docx"):
            input_path = os.path.join(root, file)

            # Preserve relative path structure
            relative_path = os.path.relpath(root, input_root)
            output_dir = os.path.join(output_root, relative_path)
            os.makedirs(output_dir, exist_ok=True)

            # Read .docx and convert to HTML
            with open(input_path, "rb") as docx_file:
                result = mammoth.convert_to_html(docx_file)
                html = result.value
            markdown_content = converter.handle(html)

            # Extract metadata
            title = os.path.splitext(file)[0]
            mod_time = os.path.getmtime(input_path)
            date_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')

            # YAML front matter
            metadata = f"""---\ntitle: "{title}"\ndate: {date_str}\nsource_file: "{file}"\n---\n\n"""

            output_filename = title + ".md"
            output_path = os.path.join(output_dir, output_filename)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(metadata + markdown_content)

            print(f"✅ Converted: {input_path} -> {output_path}")

def process_files_folder():

  for filename in os.listdir(input_dir):
      if filename.lower().endswith(".docx"):
          input_path = os.path.join(input_dir, filename)

          with open(input_path, "rb") as docx_file:
              result = mammoth.convert_to_html(docx_file)
              html = result.value

          markdown = converter.handle(html)

          output_filename = os.path.splitext(filename)[0] + ".md"
          output_path = os.path.join(output_dir, output_filename)

          with open(output_path, "w", encoding="utf-8") as f:
              f.write(markdown)

          print(f"✅ Converted: {filename} -> {output_filename}")

if __name__ == '__main__':
    folder_path = "input"
    target_language = "en"  # Change to your desired target language
    process_all_files()