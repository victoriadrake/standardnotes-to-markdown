import json
import os
import sys
import time as counter
from datetime import datetime


def readJSON(infile):
    with open(infile, "r") as f:
        data = f.read()
    return json.loads(data)


def writeMarkdown(processed, outfile):
    with open(outfile, "w+") as f:
        f.write(processed)


def setModTime(path, mod_time):
    # Convert to epoch (seconds)
    # Remove the 'Z' at end of ISO input: https://bugs.python.org/issue35829
    mtime = datetime.fromisoformat(mod_time[:-1])
    return os.utime(path, times=(datetime.now().timestamp(), mtime.timestamp()))


def main():
    if len(sys.argv) <= 2:
        print(
            "Missing arguments.\nUsage: python convert.py [JSON input filename] [output dirname]\nExample: python convert.py export.json notes\n"
        )
        sys.exit(1)

    infile = sys.argv[1]
    dirname = sys.argv[2]

    # Open the file
    try:
        raw_dict = readJSON(infile)
    except json.decoder.JSONDecodeError:
        print("Input file must be JSON format.")
        sys.exit(1)

    # Create directory for notes
    try:
        os.mkdir(dirname)
    except FileExistsError:
        print(
            f"A directory called {dirname} already exists. Stopping to avoid accidental overwriting.\nPlease provide a different directory name."
        )
        sys.exit(1)

    # Initialize stats
    count = 0
    start = counter.time()
    print("Starting the tedious work for you...")

    # Standard Notes export has a top-level "items" key
    items = raw_dict["items"]

    notes_list = []
    # Loop through the exported items. Not all of these are your notes.
    items: list
    obj: dict
    for obj in items:
        # Get just the notes in the notes_list of dicts
        if obj["content_type"] == "Note":
            # We only want these keys in the new dicts
            fields = ["uuid", "created_at", "updated_at", "content"]
            note: dict = {key: value for key, value in obj.items() if key in fields}
            notes_list.append(note)

    # Tag notes
    tags_list = []
    for obj in items:
        if obj["content_type"] == "Tag":
            fields = ["content"]
            tag: dict = {key: value for key, value in obj.items() if key in fields}
            tags_list.append(tag)
    
    # Loop the notes list
    note: dict
    notes_list: list
    for note in notes_list:
        tag_text = "\n" # Reset for each note
        # Optionally, update this to add a bit of the uuid to mitigate duplicate filenames
        if note["content"]["title"] == "":
            # If no title exists, use the creation date
            filename = f'{note["created_at"][:10]}.md'
        else:
            name = (
                f'{note["content"]["title"]}_{note["created_at"][:10]}'.replace("/", "or")
                .replace(" ", "_")
                .replace(".", "")
                .replace(":", "")
                .replace("'", "")
                .replace("?", "")
                .replace('"', "")
            )
            filename = f'{name}.md'

        # Loop the tags list
        tag: dict
        tags_list: list
        for tag in tags_list:
            if str(note["uuid"]) in str(tag["content"]["references"]):
                tag_text = tag_text + f'#{tag["content"]["title"]} '
        # Create a new .md file
        outpath = os.path.join(dirname, filename)
        # The str method renders newlines
        content = str(note["content"]["text"])
        processed = f'{content}\n{tag_text}'
        writeMarkdown(processed, outpath)
        # Preserve the note's last modified time
        setModTime(outpath, note["updated_at"])
        count += 1


    end = counter.time()
    time = end - start
    print(f"Created {count} notes in {time} seconds. You're welcome.")


if __name__ == "__main__":
    main()
