import os
import re
import yaml
import tkinter as tk
from tkinter import filedialog, messagebox

class FrontmatterModifier:
    def __init__(self):
        self.modifications = {}
        self.folder_path = ""
        self.encoding = 'utf-8'

    def modify_frontmatter(self, frontmatter):
        for action, changes in self.modifications.items():
            if action == 'add':
                frontmatter.update(changes)
            elif action == 'delete':
                for key in changes:
                    frontmatter.pop(key, None)
            elif action == 'nest':
                for old_key, new_structure in changes.items():
                    if old_key in frontmatter:
                        new_key = new_structure.get('new_key', old_key)
                        subkey = new_structure['subkey']
                        frontmatter[new_key] = {subkey: frontmatter.pop(old_key)}
                        frontmatter[new_key].update(new_structure.get('additional', {}))
            elif action == 'unnest':
                for nested_key, structure in changes.items():
                    if nested_key in frontmatter and isinstance(frontmatter[nested_key], dict):
                        subkey = structure.get('subkey', next(iter(frontmatter[nested_key])))
                        new_key = structure.get('new_key', nested_key)
                        if subkey in frontmatter[nested_key]:
                            frontmatter[new_key] = frontmatter[nested_key].get(subkey, '')
                            if new_key != nested_key:
                                frontmatter.pop(nested_key)
            elif action == 'rename':
                for old_key, new_key in changes.items():
                    if old_key in frontmatter:
                        frontmatter[new_key] = frontmatter.pop(old_key)
            elif action == 'modify':
                for key, new_value in changes.items():
                    if key in frontmatter:
                        frontmatter[key] = new_value
            elif action == 'append':
                for key, value in changes.items():
                    if key in frontmatter and isinstance(frontmatter[key], list):
                        frontmatter[key].append(value)
                    elif key in frontmatter:
                        frontmatter[key] = [frontmatter[key], value]
                    else:
                        frontmatter[key] = [value]
            elif action == 'prepend':
                for key, value in changes.items():
                    if key in frontmatter and isinstance(frontmatter[key], list):
                        frontmatter[key].insert(0, value)
                    elif key in frontmatter:
                        frontmatter[key] = [value, frontmatter[key]]
                    else:
                        frontmatter[key] = [value]
        return frontmatter

    def process_file(self, file_path):
        try:
            with open(file_path, 'r', encoding=self.encoding) as f:
                content = f.read()

            frontmatter_match = re.search(r'(?s)^---\s*\n(.*?)\n---\s*\n', content)
            if frontmatter_match:
                frontmatter_str = frontmatter_match.group(1)
                try:
                    frontmatter = yaml.safe_load(frontmatter_str)
                except yaml.YAMLError as e:
                    print(f"Error parsing YAML: {e}, skipping file {file_path}")
                    return "error"

                modified_frontmatter = self.modify_frontmatter(frontmatter)
                modified_frontmatter_str = yaml.dump(modified_frontmatter, allow_unicode=True)
                updated_content = f"---\n{modified_frontmatter_str}---\n{content[frontmatter_match.end():]}"

                try:
                    with open(file_path, 'w', encoding=self.encoding) as f:
                        f.write(updated_content)
                except Exception as e:
                    print(f"Error writing to file {file_path}: {e}")
                    return "error"
            else:
                print(f"No valid frontmatter block found, skipping file {file_path}")
                return "skipped"

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return "error"

    def convert_frontmatter(self):
        errors = []
        skipped = []
        
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    result = self.process_file(file_path)
                    
                    if result == "error":
                        errors.append(file_path)
                    elif result == "skipped":
                        skipped.append(file_path)

        return errors, skipped

class FrontmatterGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Frontmatter Modifier")
        self.modifier = FrontmatterModifier()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Select folder:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.folder_entry = tk.Entry(self.master, width=50)
        self.folder_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.master, text="Browse", command=self.browse_folder).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self.master, text="Encoding:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.encoding_entry = tk.Entry(self.master, width=20)
        self.encoding_entry.insert(0, "utf-8")
        self.encoding_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self.master, text="Modifications:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.modifications_text = tk.Text(self.master, height=10, width=50)
        self.modifications_text.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        tk.Button(self.master, text="Apply Modifications", command=self.apply_modifications).grid(row=3, column=1, pady=10)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_path)

    def apply_modifications(self):
        self.modifier.folder_path = self.folder_entry.get()
        self.modifier.encoding = self.encoding_entry.get()
        
        try:
            self.modifier.modifications = yaml.safe_load(self.modifications_text.get("1.0", tk.END))
        except yaml.YAMLError as e:
            messagebox.showerror("Error", f"Invalid YAML format in modifications: {e}")
            return

        errors, skipped = self.modifier.convert_frontmatter()

        result_message = "Modification completed.\n\n"
        if errors:
            result_message += "Errors occurred in the following files:\n"
            result_message += "\n".join(errors) + "\n\n"
        if skipped:
            result_message += "The following files were skipped (no valid frontmatter block found):\n"
            result_message += "\n".join(skipped)

        messagebox.showinfo("Results", result_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = FrontmatterGUI(root)
    root.mainloop()