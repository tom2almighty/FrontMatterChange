# Frontmatter Modifier

Frontmatter Modifier 是一个用于批量修改 Markdown 文件中 frontmatter 的工具。它支持添加、删除、重命名、修改 frontmatter 字段，以及嵌套和解嵌套键值对，适用于不同博客框架、主题间内容的迁移。

## 功能特性

- 添加新的键值对
- 删除键值对
- 重命名某个键名
- 修改某个键值
- 为某个键添加和删除子键值对
- 为某个键删除子键值对
- 为某个键值对添加上一级键
- 删除某个包含子键值对的上一级键
- 为某个数组类型的键值添加、删除、重命名成员

## 安装

1. 克隆仓库到本地：
   ```bash
   git clone https://github.com/tom2almighty/frontmatter-modifier.git
   cd frontmatter-modifier
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

1. 运行脚本：
   ```bash
   python main.py
   ```

2. 在弹出的 GUI 界面中选择要处理的文件夹，设置编码，并添加修改操作。

3. 点击“应用修改”按钮，确认后将应用所有修改到指定文件夹中的 `Markdown` 文件。

## 界面说明

- **选择文件夹**：点击“浏览”按钮选择要处理的文件夹。
- **编码**：设置文件编码，默认为 `utf-8`。
- **修改列表**：显示当前的修改操作列表。
- **添加修改**：通过下拉框选择要执行的操作，并填写相应的键和值。
- **清除所有修改**：清除当前的所有修改操作。
- **应用修改**：应用所有修改到指定文件夹中的 `Markdown` 文件。
- **撤销修改**：撤销上一步的修改操作。
- **预览**：实时预览当前的修改操作。

## 示例

以下是一些常见的修改操作示例：

- 添加新的键值对：
  ```yaml
  action: add
  key: title
  value: New Title
  ```

- 删除键值对：
  ```yaml
  action: delete
  key: title
  ```

- 重命名某个键名：
  ```yaml
  action: rename
  key: old_key
  new_key: new_key
  ```

- 修改某个键值：
  ```yaml
  action: modify
  key: title
  value: Modified Title
  ```

- 为某个键添加子键值对：
  ```yaml
  action: add_subkey
  key: author
  subkey: name
  value: John Doe
  ```

- 为某个键删除子键值对：
  ```yaml
  action: delete_subkey
  key: author
  subkey: name
  ```

- 为某个键值对添加上一级键：
  ```yaml
  action: add_parent
  key: title
  new_key: metadata
  ```

- 删除某个包含子键值对的上一级键：
  ```yaml
  action: delete_parent
  key: metadata
  ```

- 为某个数组类型的键值添加成员：
  ```yaml
  action: add_array_member
  key: tags
  value: new_tag
  ```

- 为某个数组类型的键值删除成员：
  ```yaml
  action: delete_array_member
  key: tags
  index: 0
  ```

- 为某个数组类型的键值重命名成员：
  ```yaml
  action: rename_array_member
  key: tags
  index: 0
  value: updated_tag
  ```

## 贡献

欢迎贡献代码、报告问题或提出建议。请在 GitHub 仓库中提交 Issue 或 Pull Request。

