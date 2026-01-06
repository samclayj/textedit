# Attachment Manager

Script:

- attachment_manager.py

Running:

```
python3 attachment_manager.py --markdown-dir ./slipbox --attachments-dir ./attachments | fzf
```

Instructions:

- For Apple Notes - export notes as markdown. Copy attachments from the `Attachments` folder to the Obsidian attachments folder. Run the script and it will automatically rename the attachments to match the Obsidian attachment format.

Todo:

- [x] Support renaming Apple Note export attachments in the format: `![image.png](98F8D1B2-CC0E-4C0D-AED4-3A09740DA140.png)`.
- [x] Support processing multiple directories at one time.

# Book Base

Script:

- book_base.py

Todo:

- [ ] This is work in progress, figure out if it is still needed.
