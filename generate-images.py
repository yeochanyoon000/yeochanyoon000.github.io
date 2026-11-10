# from pathlib import Path
# import json

# ROOT = Path(__file__).resolve().parent
# FOLDERS = {
#     "home": ROOT / "assets" / "images" / "home",
#     "work": ROOT / "assets" / "images" / "work",
# }
# IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}

# image_list = {}

# for section, folder in FOLDERS.items():
#     folder.mkdir(parents=True, exist_ok=True)
#     images = sorted(
#         (
#             path.relative_to(ROOT).as_posix()
#             for path in folder.iterdir()
#             if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
#         ),
#         key=str.lower,
#     )
#     image_list[section] = images

# output = ROOT / "images.json"
# output.write_text(json.dumps(image_list, indent=2, ensure_ascii=False), encoding="utf-8")
# print(f"Updated {output.name}")
# print(f"Homepage images: {len(image_list['home'])}")
# print(f"Work images: {len(image_list['work'])}")

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent

FOLDERS = {
    "home": ROOT / "assets" / "images" / "home",
    "work": ROOT / "assets" / "images" / "work",
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}
OUTPUT = ROOT / "images.json"


def get_image_paths(folder):
    """Return all image paths currently present in a folder."""
    folder.mkdir(parents=True, exist_ok=True)
    return {
        path.relative_to(ROOT).as_posix()
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    }


def load_existing():
    """Load the current image order, if images.json already exists."""
    if not OUTPUT.exists():
        return {}

    try:
        data = json.loads(OUTPUT.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        print("Warning: images.json could not be read; starting with folder order.")
        return {}


existing = load_existing()
image_list = {}

for section, folder in FOLDERS.items():
    current_paths = get_image_paths(folder)

    # Keep the previous order for files that still exist.
    previous_order = existing.get(section, [])
    if not isinstance(previous_order, list):
        previous_order = []

    ordered = []
    seen = set()

    for item in previous_order:
        if isinstance(item, str) and item in current_paths and item not in seen:
            ordered.append(item)
            seen.add(item)

    # Add only newly discovered images at the end, in alphabetical order.
    new_images = sorted(current_paths - seen, key=str.lower)
    ordered.extend(new_images)

    image_list[section] = ordered

OUTPUT.write_text(
    json.dumps(image_list, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print(f"Updated {OUTPUT.name}")
print(f"Homepage images: {len(image_list['home'])}")
print(f"Work images: {len(image_list['work'])}")
print("Existing order preserved; new images appended.")

