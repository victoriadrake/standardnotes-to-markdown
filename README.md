# Convert Standard Notes JSON export to Markdown files

This was written to turn a single export file from Standard Notes into individual Markdown files, while preserving the titles (including emojis), tags, and last modified times.

A typical (unencrypted) Standard Notes export is a zip that contains a directory, `Items/`, with your notes as individual `txt` files. It also contains a `Standard Notes Backup and Import File.txt`, which is JSON-formatted.

This Python program conforms to the particular form of that JSON-formatted export. It creates individual Markdown files for each note.

## Usage

`python convert.py [JSON input filename] [output dirname]`

## Using this in a larger project

This program was written to a professional standard, but just for fun. It has not been considered in a production environment. Use it with wild abandon on your own machine with a known input file.
