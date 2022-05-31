from pathlib import Path
from subprocess import run
from typing import Iterator, List, Tuple

from jinja2 import Template

HTML = str

pics_dir = Path("static/pics")


def is_pic_square(pic: Path) -> bool:
    """Returns True if pic's width is equal to its height"""
    # I could use the `file` command as well but the output of `identify` is
    # formattable and I feel like `file`'s interface isn't consistent
    proc = run(["identify", "-format", "%[fx:w]x%[fx:h]", pic], capture_output=True)
    width, height = proc.stdout.decode().split("x")
    return width == height


def render_category(
    category_title: str, pic_template: Template, gallery_template: Template
) -> Iterator[Tuple[str, HTML]]:
    """
    Iterates over the category's pic directory, rendering the category's
    gallery HTML and every picture's individual page's HTML as well.

    Returns an iterator of filenames and HTML strings. The HTML should be
    written into a file at the filename.

    Raises ValueError on processing pictures that aren't square (width != height)
    """
    directory = pics_dir / category_title
    pics_in_dir = list(directory.iterdir())
    gallery_pics: List[Tuple[str, str]] = []

    for i, pic in enumerate(pics_in_dir):
        if not is_pic_square(pic):
            filename = pic.relative_to(directory.parent)
            raise ValueError(f"PLEASE make {filename} a square!!!! I beg")

        link = pic.relative_to(pics_dir.parent)

        gallery_pics.append((pic.stem, f"/{link}"))

        args = {
            "src": link,
            "back": f"/{category_title}.html",
            "next": (
                f"{pics_in_dir[i + 1].stem}.html" if i < len(pics_in_dir) - 1 else None
            ),
            "prev": f"{pics_in_dir[i - 1].stem}.html" if i > 0 else None,
        }
        yield f"{pic.stem}.html", pic_template.render(**args)

    yield (
        f"{category_title}.html",
        gallery_template.render(pics=gallery_pics),
    )
