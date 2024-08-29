import os
import re
import yaml

def modify_frontmatter(frontmatter, modifications):
    for action, changes in modifications.items():
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
    return frontmatter

def process_file(file_path, modifications, encoding='utf8'):
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()

        # 修正后的正则表达式匹配前置信息
        frontmatter_match = re.search(r'(?s)^---\s*\n(.*?)\s*\n---\s*', content)
        if frontmatter_match:
            frontmatter_str = frontmatter_match.group(1)
            try:
                frontmatter = yaml.safe_load(frontmatter_str)
            except yaml.YAMLError as e:
                print(f"解析 YAML 时出错: {e}，跳过文件 {file_path}")
                return "error"

            modified_frontmatter = modify_frontmatter(frontmatter, modifications)
            modified_frontmatter_str = yaml.dump(modified_frontmatter, allow_unicode=True)
            # 确保 `---` 后面有换行符与正文分开
            updated_content = f"---\n{modified_frontmatter_str}---\n{content[frontmatter_match.end():]}"

            try:
                with open(file_path, 'w', encoding=encoding) as f:
                    f.write(updated_content)
            except Exception as e:
                print(f"写入文件 {file_path} 时出错: {e}")
                return "error"
        else:
            print(f"未找到合法的 frontmatter 区块，跳过文件 {file_path}")
            return "skipped"

    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return "error"

def convert_frontmatter(folder_path, modifications, encoding='utf8'):
    errors = []
    skipped = []
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                result = process_file(file_path, modifications, encoding)
                
                if result == "error":
                    errors.append(file_path)
                elif result == "skipped":
                    skipped.append(file_path)

    if errors:
        print("\n以下文件在处理时出错:")
        for file in errors:
            print(f"- {file}")

    if skipped:
        print("\n以下文件被跳过（未找到合法的 frontmatter 区块）:")
        for file in skipped:
            print(f"- {file}")
