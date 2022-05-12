from datetime import datetime
from pathlib import Path
from shutil import copy2, copytree, rmtree
from subprocess import run
from typing import Iterator, List, Tuple

from jinja2 import Environment, FileSystemLoader, select_autoescape

HTML = str

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html"]),
)

out_dir = Path("out")

pics_dir = Path("static/pics")


def is_pic_square(pic: Path) -> bool:
    """Returns True if pic's width is equal to its height"""
    # I could use the `file` command as well but the output of `identify` is
    # formattable and I feel like `file`'s interface isn't consistent
    proc = run(["identify", "-format", "%[fx:w]x%[fx:h]", pic], capture_output=True)
    width, height = proc.stdout.decode().split("x")
    return width == height


def render(template_name, title, **kwargs):
    rendered = env.get_template(template_name).render(**kwargs)
    out_dir.joinpath(f"{title}.html").write_text(rendered)


def render_category(category_title: str) -> Iterator[Tuple[str, HTML]]:
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
        yield f"{pic.stem}.html", env.get_template("pic.html").render(**args)

    yield (
        f"{category_title}.html",
        env.get_template("gallery.html").render(pics=gallery_pics),
    )


if __name__ == "__main__":
    print()
    print(datetime.now())

    # Fresh start 😎
    rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir()

    render("index.html", "index")

    # Render makeup and tattoo galleries, stopping the process if one of the
    # pics isn't square, prompting the user to fix it manually (I'm not going
    # to let a machine randomly crop pics..............)
    for category in ["tats", "mu"]:
        for target_filename, html in render_category(category):
            out_dir.joinpath(target_filename).write_text(html)
    print("💪 Generated pages")

    copytree("static", "out/", dirs_exist_ok=True)
    print("💪 Copied static assets")

    copy2("static/guli.scss", "out/guli.scss")
    run(["sass", "out/guli.scss", "out/guli.css"])
    print("💪 Generated CSS")
