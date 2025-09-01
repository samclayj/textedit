properties = [
    "---\n",
    "cover: ",
    "year: ",
    "title: ",
    "author: ",
    "tags: ",
    "---\n",
]

cover_pattern = r'!\[\[(.*?)\]\]'

"""
Automatically formats a markdown file for my Obsidian book base.
"""
def edit_markdown_file(file_path, new_content):
    """
    Opens a Markdown file, replaces its content, and saves the changes.

    Args:
        file_path (str): The path to the Markdown file.
        new_content (str): The new content to write to the file.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"File '{file_path}' updated successfully.")
    except IOError as e:
        print(f"An error occurred: {e}")


def has_properties(file_name):
    has_opener = False
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            if line == '---\n' and has_opener:
                return True
            else:
                has_opener = True
    return False

def init_properties(file_path):
    return



# Example usage:
complete_file = 'example.md'
todo_file = 'todo.md'


print(has_properties(complete_file))
print(has_properties(todo_file))
