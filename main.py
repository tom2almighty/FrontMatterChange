import os
import re
import yaml
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk

class FrontmatterModifier:
    def __init__(self):
        self.modifications = []
        self.folder_path = ""
        self.encoding = 'utf-8'

    def modify_frontmatter(self, frontmatter):
        for modification in self.modifications:
            action = modification['action']
            key = modification['key']
            value = modification.get('value')
            new_key = modification.get('new_key')
            subkey = modification.get('subkey')
            index = modification.get('index')

            if action == 'add':
                frontmatter[key] = value
            elif action == 'delete':
                if key in frontmatter:
                    del frontmatter[key]
            elif action == 'rename':
                if key in frontmatter:
                    frontmatter[new_key] = frontmatter.pop(key)
            elif action == 'modify':
                if key in frontmatter:
                    frontmatter[key] = value
            elif action == 'add_subkey':
                if key in frontmatter and isinstance(frontmatter[key], dict):
                    frontmatter[key][subkey] = value
            elif action == 'delete_subkey':
                if key in frontmatter and isinstance(frontmatter[key], dict) and subkey in frontmatter[key]:
                    del frontmatter[key][subkey]
            elif action == 'add_parent':
                if key in frontmatter:
                    frontmatter[new_key] = {key: frontmatter.pop(key)}
            elif action == 'delete_parent':
                if key in frontmatter and isinstance(frontmatter[key], dict):
                    for k, v in frontmatter[key].items():
                        frontmatter[k] = v
                    del frontmatter[key]
            elif action == 'add_array_member':
                if key in frontmatter and isinstance(frontmatter[key], list):
                    frontmatter[key].append(value)
            elif action == 'delete_array_member':
                if key in frontmatter and isinstance(frontmatter[key], list) and 0 <= index < len(frontmatter[key]):
                    del frontmatter[key][index]
            elif action == 'rename_array_member':
                if key in frontmatter and isinstance(frontmatter[key], list) and 0 <= index < len(frontmatter[key]):
                    frontmatter[key][index] = value

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
        self.history = []

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="选择文件夹:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.folder_entry = tk.Entry(self.master, width=50)
        self.folder_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.master, text="浏览", command=self.browse_folder).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self.master, text="编码:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.encoding_entry = tk.Entry(self.master, width=20)
        self.encoding_entry.insert(0, "utf-8")
        self.encoding_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self.master, text="修改列表:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.modifications_text = scrolledtext.ScrolledText(self.master, height=10, width=50)
        self.modifications_text.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        self.action_var = tk.StringVar()
        self.action_combobox = ttk.Combobox(self.master, textvariable=self.action_var, values=[
            "添加", "删除", "重命名", "修改", "添加子键", "删除子键", "添加上级键", "删除上级键", "添加数组成员", "删除数组成员", "重命名数组成员"
        ])
        self.action_combobox.grid(row=3, column=0, padx=5, pady=5)
        tk.Button(self.master, text="添加修改", command=self.add_modification).grid(row=3, column=1, pady=10)
        tk.Button(self.master, text="清除所有修改", command=self.clear_modifications).grid(row=3, column=2, pady=10)
        tk.Button(self.master, text="应用修改", command=self.apply_modifications).grid(row=4, column=1, pady=10)
        tk.Button(self.master, text="撤销修改", command=self.undo_modification).grid(row=4, column=2, pady=10)

        tk.Label(self.master, text="预览:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.preview_text = scrolledtext.ScrolledText(self.master, height=10, width=50)
        self.preview_text.grid(row=5, column=1, columnspan=2, padx=5, pady=5)

        self.modifications_text.bind("<KeyRelease>", self.update_preview)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_path)

    def add_modification(self):
        action = self.action_var.get()
        if not action:
            messagebox.showwarning("警告", "请选择一个操作", parent=self.master)
            return

        actions = {
            "添加": self.add_dialog,
            "删除": self.delete_dialog,
            "重命名": self.rename_dialog,
            "修改": self.modify_dialog,
            "添加子键": self.add_subkey_dialog,
            "删除子键": self.delete_subkey_dialog,
            "添加上级键": self.add_parent_dialog,
            "删除上级键": self.delete_parent_dialog,
            "添加数组成员": self.add_array_member_dialog,
            "删除数组成员": self.delete_array_member_dialog,
            "重命名数组成员": self.rename_array_member_dialog
        }

        if action in actions:
            actions[action]()

    def add_dialog(self):
        key = simpledialog.askstring("输入", "输入要添加的键:", parent=self.master)
        value = simpledialog.askstring("输入", "输入要添加的值:", parent=self.master)
        if key:
            if value is None:
                value = ""
            self.modifier.modifications.append({"action": "add", "key": key, "value": value})
            self.history.append(self.modifier.modifications.copy())
            self.update_modifications()

    def delete_dialog(self):
        key = simpledialog.askstring("输入", "输入要删除的键:", parent=self.master)
        if key:
            self.modifier.modifications.append({"action": "delete", "key": key})
            self.history.append(self.modifier.modifications.copy())
            self.update_modifications()

    def rename_dialog(self):
        key = simpledialog.askstring("输入", "输入旧键名:", parent=self.master)
        new_key = simpledialog.askstring("输入", "输入新键名:", parent=self.master)
        if key and new_key:
            self.modifier.modifications.append({"action": "rename", "key": key, "new_key": new_key})
            self.history.append(self.modifier.modifications.copy())
            self.update_modifications()

    def modify_dialog(self):
        key = simpledialog.askstring("输入", "输入要修改的键:", parent=self.master)
        new_value = simpledialog.askstring("输入", "输入新值:", parent=self.master)
        if key:
            if new_value is None:
                new_value = ""
            self.modifier.modifications.append({"action": "modify", "key": key, "value": new_value})
            self.history.append(self.modifier.modifications.copy())
            self.update_modifications()

    def add_subkey_dialog(self):
        key = simpledialog.askstring("输入", "输入要添加子键的键:", parent=self.master)
        subkey = simpledialog.askstring("输入", "输入子键:", parent=self.master)
        value = simpledialog.askstring("输入", "输入子键的值:", parent=self.master)
        if key and subkey:
            if value is None:
                value = ""
            self.modifier.modifications.append({"action": "add_subkey", "key": key, "subkey": subkey, "value": value})
            self.history.append(self.modifier.modifications.copy())
            self.update_modifications()

    def delete_subkey_dialog(self):
        key = simpledialog.askstring("输入", "输入要删除子键的键:", parent=self.master)
        subkey = simpledialog.askstring("输入", "输入要删除的子键:", parent=self.master)
        if key and subkey:
            self.modifier.modifications.append({"action": "delete_subkey", "key": key, "subkey": subkey})
            self.history.append(self.modifier.modifications.copy())
            self.update_modifications()

    def add_parent_dialog(self):
        key = simpledialog.askstring("输入", "输入要添加上级键的键:", parent=self.master)
        new_key = simpledialog.askstring("输入", "输入新的上级键:", parent=self.master)
        if key and new_key:
            self.modifier.modifications.append({"action": "add_parent", "key": key, "new_key": new_key})
            self.history.append(self.modifier.modifications.copy())
            self.update_modifications()

    def delete_parent_dialog(self):
        key = simpledialog.askstring("输入", "输入要删除的上级键:", parent=self.master)
        if key:
            self.modifier.modifications.append({"action": "delete_parent", "key": key})
            self.history.append(self.modifier.modifications.copy())
            self.update_modifications()

    def add_array_member_dialog(self):
        key = simpledialog.askstring("输入", "输入要添加成员的数组键:", parent=self.master)
        value = simpledialog.askstring("输入", "输入要添加的值:", parent=self.master)
        if key:
            if value is None:
                value = ""
            self.modifier.modifications.append({"action": "add_array_member", "key": key, "value": value})
            self.history.append(self.modifier.modifications.copy())
            self.update_modifications()

    def delete_array_member_dialog(self):
        key = simpledialog.askstring("输入", "输入要删除成员的数组键:", parent=self.master)
        index = simpledialog.askinteger("输入", "输入要删除的成员索引:", parent=self.master)
        if key and index is not None:
            self.modifier.modifications.append({"action": "delete_array_member", "key": key, "index": index})
            self.history.append(self.modifier.modifications.copy())
            self.update_modifications()

    def rename_array_member_dialog(self):
        key = simpledialog.askstring("输入", "输入要重命名成员的数组键:", parent=self.master)
        index = simpledialog.askinteger("输入", "输入要重命名的成员索引:", parent=self.master)
        value = simpledialog.askstring("输入", "输入新的值:", parent=self.master)
        if key and index is not None:
            if value is None:
                value = ""
            self.modifier.modifications.append({"action": "rename_array_member", "key": key, "index": index, "value": value})
            self.history.append(self.modifier.modifications.copy())
            self.update_modifications()

    def update_modifications(self):
        self.modifications_text.delete("1.0", tk.END)
        self.modifications_text.insert("1.0", yaml.dump(self.modifier.modifications, allow_unicode=True))
        self.update_preview()

    def apply_modifications(self):
        self.modifier.folder_path = self.folder_entry.get()
        self.modifier.encoding = self.encoding_entry.get()
        
        confirm = messagebox.askyesno("确认", "确定要应用这些修改吗?", parent=self.master)
        if not confirm:
            return

        errors, skipped = self.modifier.convert_frontmatter()

        result_message = "修改完成.\n\n"
        if errors:
            result_message += "以下文件发生错误:\n"
            result_message += "\n".join(errors) + "\n\n"
        if skipped:
            result_message += "以下文件被跳过 (没有有效的 frontmatter 块):\n"
            result_message += "\n".join(skipped)

        messagebox.showinfo("结果", result_message, parent=self.master)
        self.clear_modifications()

    def clear_modifications(self):
        self.modifier.modifications = []
        self.history = []
        self.modifications_text.delete("1.0", tk.END)
        self.update_preview()

    def undo_modification(self):
        if self.history:
            self.history.pop()
            if self.history:
                self.modifier.modifications = self.history[-1].copy()
            else:
                self.modifier.modifications = []
            self.update_modifications()

    def update_preview(self, event=None):
        try:
            modifications = yaml.safe_load(self.modifications_text.get("1.0", tk.END))
        except yaml.YAMLError:
            self.preview_text.delete("1.0", tk.END)
            self.preview_text.insert("1.0", "无效的 YAML 格式")
            return

        if not modifications:
            self.preview_text.delete("1.0", tk.END)
            self.preview_text.insert("1.0", "没有修改")
            return

        preview_text = ""
        for modification in modifications:
            action = modification['action']
            key = modification['key']
            value = modification.get('value')
            new_key = modification.get('new_key')
            subkey = modification.get('subkey')
            index = modification.get('index')

            preview_text += f"{action.capitalize()}:\n"
            preview_text += f"  键: {key}\n"
            if value is not None:
                preview_text += f"  值: {value}\n"
            if new_key is not None:
                preview_text += f"  新键: {new_key}\n"
            if subkey is not None:
                preview_text += f"  子键: {subkey}\n"
            if index is not None:
                preview_text += f"  索引: {index}\n"
            preview_text += "\n"

        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert("1.0", preview_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = FrontmatterGUI(root)
    root.mainloop()