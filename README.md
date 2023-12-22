# rm2do
# Requirements
- Remarkable Cloud
- Google API Access (specifically Google Tasks)
  - A Google Task list called "Remarkable"
- Python 3.12 (maybe? haven't tried any other versions)

# Running
`py -m venv venv`

`pip install -r requirements.txt`

`main.py run`

_You can also do `main.py pull` or `main.py push` to only run one action_

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
- Task creation through OCR
  - Though from what I see these days, handwriting OCR is _tricky_ to say the least
- Ability to run as a service (watching for changes instead of manually running)
- Somehow get around having to use Remarkable Cloud
  - It's slow, I don't like it
  - RM2 also has an interesting quirk where deleting a file will not reflect on the device until refreshed... but adding a file does. So you get duplicates until you refresh
  - You also ahve to close the file for it to sync and refresh, a slow process
    - This one is harder to get around since it's fundementally how `xochitl` works, but still... food for thought
