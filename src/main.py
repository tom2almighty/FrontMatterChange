from modify import modify_frontmatter, process_file, convert_frontmatter

def main():
    folder_path = r".\test"
    modifications = {
        'add': {'author': 'John Doe'},
        'delete': ['outdated_field'],
        'nest': {
            'featured_image': {'new_key': 'cover', 'subkey': 'image', 'additional': {'alt': ''}},
        },
        'unnest': {
            'link': {'subkey': 'bio', 'new_key': 'link'},
        },
        'rename': {'abbrlink': 'slug'},
        'modify': {'title': 'New Title'},
    }
    convert_frontmatter(folder_path, modifications)

if __name__ == "__main__":
    main()
