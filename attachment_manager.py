import os
import re
import uuid
import argparse

attachment_pattern = r'!\[\[(.*?)\]\]'

def rename_attachments_in_file(markdown_file_path, attachments_dir, dry_run=False):
    """Renames attachments found in a single markdown file."""
    markdown_file_name = os.path.splitext(os.path.basename(markdown_file_path))[0]

    try:
        with open(markdown_file_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            original_content = content

            attachments = re.findall(attachment_pattern, content)

            changes_made = False
            for attachment_name in attachments:
                old_attachment_path = os.path.join(attachments_dir, attachment_name)

                if os.path.exists(old_attachment_path):
                    file_ext = os.path.splitext(attachment_name)[1]
                    # In a dry run, we generate a placeholder UUID for consistent output
                    new_uuid = "DRY-RUN-UUID" if dry_run else uuid.uuid4()
                    new_file_name = f"{markdown_file_name} - {new_uuid}{file_ext}"
                    new_attachment_path = os.path.join(attachments_dir, new_file_name)

                    if dry_run:
                        print(f"[DRY RUN] Would rename: {old_attachment_path} -> {new_attachment_path}")
                    else:
                        os.rename(old_attachment_path, new_attachment_path)

                    # Update the link in the markdown file content
                    content = content.replace(f"![[{attachment_name}]]", f"![[{new_file_name}]]")
                    changes_made = True

            if changes_made:
                if dry_run:
                     print(f"[DRY RUN] Would update links in: {markdown_file_path}")
                else:
                    if content != original_content:
                        f.seek(0)
                        f.write(content)
                        f.truncate()
                        print(f"Updated attachments in {markdown_file_path}")

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
            rename_attachments_in_file(markdown_file_path, attachments_dir, args.dry_run)

if __name__ == "__main__":
    main()
