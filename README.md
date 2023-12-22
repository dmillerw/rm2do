# rm2do
# Requirements
- Remarkable Cloud
- Google API Access (specifically Google Tasks)

# Running
`main.py run`

It _should_ walk you through the initial setup (pairing with Remarkable Cloud and getting Google tokens)

**NOTE**: This will also **attempt** to download the appropriate `rmapi` binary for your OS (it uses it to interact w/ the Cloud API because I don't really want to re-implement right now)

If that doesn't work it, download manually and throw it in `bin/rmapi[.exe]`

---

Run for the first time (after completing all the authentication steps)

It will pull all tasks from a Google Task list called "Remarkable" and put them into a PDF. Internally it also stores a reference to the Task ID and the coordinates of the cooresponding checkbox. This is then pushed to Cloud

When pulling, it will pull the file back down from Cloud and read through all the pen marks, looking for any that intersect the defined checkboxes. Any tasks that do are marked as complete.

The PDF is then re-generated using the latest list of tasks, and the cycle repeats

# Todo

_In no particular order_

- **BETTER LOGGING** _oh dear god, better logging_
- Better error handling (_see above_)
- File comparison (don't download unchanged files from Remarkable)
- Task comparison (don't regenerate if nothing has changed)
- Better documentation/comments

## Features

- Prettier PDF
- Markup on tasks (saving some of the surrounding drawing and attaching to the generated PDF)
- Actions? Highlight to make a priority, strike through to complete
- Other todo backends
