from datetime import datetime
from pathlib import Path
from shutil import copy2, copytree
from subprocess import run

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html"]),
)

out_dir = Path("out")
out_dir.mkdir(exist_ok=True)

pics_dir = Path("static/pics")


def is_pic_square(pic: Path) -> bool:
    """Returns True if pic's width is equal to its height"""
    # I could use the `file` command as well but the output of `identify` is
    # formattable and I feel like `file`'s interface isn't consistent
    proc = run(["identify", "-format", "%[fx:w]x%[fx:h]", pic], capture_output=True)
    width, height = proc.stdout.decode().split("x")
    return width == height


def pics_in_dir(d: Path):
    """
    Iterate over files in given directory, return a tuple of the filename and a
    link to use as a src attribute for <img>
    """
    for p in d.iterdir():
        yield p.name, f"/{p.relative_to(pics_dir.parent)}"


def render(template_name, title, **kwargs):
    rendered = env.get_template(template_name).render(**kwargs)
    out_dir.joinpath(f"{title}.html").write_text(rendered)


print()
print(datetime.now())


if __name__ == "__main__":
    render("index.html", "index")

    # Render makeup and tattoo galleries, stopping the process if one of the
    # pics isn't square, prompting the user to fix it manually (I'm not going
    # to let a machine randomly crop pics..............)
    for category in ["tats", "mu"]:
        directory = pics_dir / category
        for pic in directory.iterdir():
            if not is_pic_square(pic):
                filename = pic.relative_to(directory.parent)
                raise ValueError(f"PLEASE make {filename} a square!!!! I beg")
        render("gallery.html", category, pics=pics_in_dir(directory))
    print("💪 Generated pages")

    copytree("static", "out/", dirs_exist_ok=True)
    print("💪 Copied static assets")

    copy2("static/guli.scss", "out/guli.scss")
    run(["sass", "out/guli.scss", "out/guli.css"])
    print("💪 Generated CSS")
