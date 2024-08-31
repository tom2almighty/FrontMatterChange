# Frontmatter 修改工具

## 项目简介
这是一个用于批量修改 `Markdown` 文件中 `frontmatter` 的工具。它支持添加、删除、嵌套、解嵌套、重命名以及修改 `frontmatter` 字段，可以用于不同博客框架、主题间内容的迁移。

## 功能特点
- **添加字段**: 向 `frontmatter` 中添加新的字段。
- **删除字段**: 从 `frontmatter` 中删除指定字段。
- **嵌套字段**: 将字段嵌套到子键中。
- **解嵌套字段**: 将子键中的字段解嵌套。
- **重命名字段**: 修改 `frontmatter` 字段的名称。
- **修改字段值**: 修改现有字段的值。
- **添加新字段值**： 给字段添加新的值。

## 安装与使用
**安装依赖**

下载后安装依赖：
```python
pip install -r requirements.txt
```
**使用**
 双击 `main.py` 运行，选择文件夹后以 `YAML` 格式添加需要的修改。

## 字段说明

| 参数      | 功能       | 说明                                                         |
| --------- | ---------- | ------------------------------------------------------------ |
| `add`     | 添加字段   | `'add': {'author': 'John Doe'}` 将在 `frontmatter` 中添加一个名为 `author` 的字段，值为 `John Doe`。 |
| `delete`  | 删除字段   | `'delete': ['outdated_field']` 将删除名为 `outdated_field` 的字段。 |
| `nest`    | 嵌套字段   | 将现有字段嵌套到新的字段下。例如，`'nest': {'featured_image': {'new_key': 'cover', 'subkey': 'image', 'additional': {'alt': ''}}}` 会将 `featured_image` 字段嵌套到 `cover` 字段下，并且 `cover` 字段下会包含 `image` 子字段，`image`的值为原始 `featured_image` 的值，同时附加一个 `alt` 子字段。 |
| `unnest`  | 解嵌套字段 | 将嵌套的字段提升为顶级字段或移动到另一个键下。例如，`'unnest': {'link': {'subkey': 'bio', 'new_key': 'link'}}` 会将 `link` 字段下的 `bio` 子字段提升为顶级 `link` 字段，或移动至新的键下，值保持不变。 |
| `raname`  | 重命名字段 | `'rename': {'abbrlink': 'slug'}` 将 `abbrlink` 字段重命名为 `slug`。` |
| `modify`  | 修改字段值 | 直接修改现有字段的值。例如，`'modify': {'title': 'New Title'}` 将 `title` 字段的值修改为 `New Title`。 |
| `append`  | 添加字段值 | 将值添加到列表末尾，如果字段不存在则创建新列表。             |
| `prepend` | 添加字段值 | 将值添加到列表开头，如果字段不存在则创建新列表。             |

下面是一个例子：

```yaml
add:
  author: John Doe
delete:
  - outdated_field
nest:
  featured_image:  # 需要嵌套的字段
    new_key: cover # 嵌套到此字段下
    subkey: image  # 此字段使用 `featured_image` 的原始值
    additional:
      alt: '' # 额外的子字段
unnest:
  link: # 需要解嵌套的字段
    subkey: bio # 新顶级字段使用此字段的值
    new_key: link # 新顶级字段的名称
rename:
  abbrlink: slug
modify:
  title: New Title
append:
  tags: new_tag
prepend:
  categories: main_category
```