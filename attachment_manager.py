import os
import re
import uuid
import argparse

def fix_bad_attachments_in_file(markdown_file_path, dry_run=False):
    """Fixes attachments that are in a malformed format like ![[]](attachments/file.png)."""

    # This pattern finds the malformed link and captures the filename.
    bad_attachment_pattern = r'\[\]\(attachments\/(.*?)\)'
    replacements = []

    try:
        with open(markdown_file_path, 'r+', encoding='utf-8') as f:
            content = f.read()

            for match in re.finditer(bad_attachment_pattern, content):
                original_link = match.group(0)
                file_name = match.group(1)
                new_link = f'![[{file_name}]]'
                replacements.append((original_link, new_link))

            if replacements:
                if dry_run:
                    print(f'[DRY RUN] In {markdown_file_path}, would fix {len(replacements)} bad links:')
                    for old, new in replacements:
                        print(f'  - Replace "{old}"')
                        print(f'    with    "{new}"')
                else:
                    # Apply all replacements to the content
                    new_content = content
                    for old, new in replacements:
                        new_content = new_content.replace(old, new)

                    f.seek(0)
                    f.write(new_content)
                    f.truncate()
                    print(f'Fixed {len(replacements)} bad attachment links in {markdown_file_path}')

    except Exception as e:
        print(f'Error fixing bad attachments in {markdown_file_path}: {e}')


def rename_attachments_in_file(markdown_file_path, attachments_dir, dry_run=False):
    """Renames attachments found in a single markdown file."""
    attachment_pattern = r'!\[\[(?:attachments\/)?(.*?)\]\]'
    markdown_file_name = os.path.splitext(os.path.basename(markdown_file_path))[0]

    try:
        with open(markdown_file_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            original_content = content
            new_content = content

            changes_made = False
            for match in re.finditer(attachment_pattern, content):
                attachment_name = match.group(1)
                original_link = match.group(0)

                old_attachment_path = os.path.join(attachments_dir, attachment_name)

                # Don't update attachments that have already been updated.
                if attachment_name.startswith(markdown_file_name):
                    continue

                if os.path.exists(old_attachment_path):
                    file_ext = os.path.splitext(attachment_name)[1]
                    new_uuid = "DRY-RUN-UUID" if dry_run else uuid.uuid4()
                    new_file_name = f'{markdown_file_name} - {new_uuid}{file_ext}'
                    new_attachment_path = os.path.join(attachments_dir, new_file_name)

                    if dry_run:
                        print(f"[DRY RUN] Would rename: {old_attachment_path} -> {new_attachment_path}")
                    else:
                        os.rename(old_attachment_path, new_attachment_path)

                    new_content = new_content.replace(original_link, f'![[{new_file_name}]]\n\n')
                    # Also handle any properties.
                    new_content = new_content.replace(attachment_name, new_file_name)
                    changes_made = True

            if changes_made:
                if dry_run:
                     print(f"[DRY RUN] Would update links in: {markdown_file_path}")
                else:
                    if new_content != original_content:
                        f.seek(0)
                        f.write(new_content)
                        f.truncate()
                        print(f"Updated attachments in {markdown_file_path}")
            else:
                print(f"No changes made to {markdown_file_path}")

    except Exception as e:
        print(f"Error processing {markdown_file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Rename attachments in markdown files.")
    parser.add_argument("--markdown-dir", required=True, help="Directory containing markdown files.")
    parser.add_argument("--attachments-dir", required=True, help="Directory containing attachment files.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the renaming process without making changes.")
    args = parser.parse_args()

    # Resolve to absolute paths for robustness
    markdown_dir = os.path.abspath(args.markdown_dir)
    attachments_dir = os.path.abspath(args.attachments_dir)

    if not os.path.isdir(markdown_dir):
        print(f"Error: Markdown directory not found at {markdown_dir}")
        return

    if not os.path.isdir(attachments_dir):
        print(f"Error: Attachments directory not found at {attachments_dir}")
        return

    for filename in os.listdir(markdown_dir):
        if filename.endswith(".md"):
            markdown_file_path = os.path.join(markdown_dir, filename)
            fix_bad_attachments_in_file(markdown_file_path, args.dry_run)
            rename_attachments_in_file(markdown_file_path, attachments_dir, args.dry_run)

if __name__ == "__main__":
    main()
