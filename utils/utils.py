import os

def scan_recurse(base_dir):
    try:
        for entry in os.scandir(base_dir):
            if entry.is_file():
                yield entry
            else:
                yield from scan_recurse(entry.path)
    except Exception as e:
        return str(e)