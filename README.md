# Convert Standard Notes JSON export to Markdown files

Alert! Custom edge-case code ahead!

This was written to turn a single export file from Standard Notes into individual Markdown files, while preserving the titles (including emojis) and last modified times.

A typical (unencrypted) Standard Notes export is a zip that contains a directory, `Items/`, with your notes as individual `txt` files. It also contains a `Standard Notes Backup and Import File.txt`, which is JSON-formatted.

This Python program conforms to the particular form of that JSON-formatted export. It creates individual Markdown files for each note. If you have the `Items/` directory, you shouldn't need to do this (just rename each note with a `.md` extension instead) unless you're _really_ serious about those emojis.

***That said,*** if you're looking for a Python example of iterating through JSON, building a new dictionary from another dictionary, opening and writing files, setting arbitrary modification times on a new file, adding type annotations to a `for` loop, checking for the existence of command-line arguments, or timing how long it takes for your program to run... it's all in here.

## Using this in a larger project

This program was written to a professional standard, but just for fun. It has not been considered in a production environment. Use it with wild abandon on your own machine with a known input file; don't rely on it in a production application without stringent input sanitization (and you might lose those emojis).
