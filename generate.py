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
    render("gallery.html", "tats", pics=pics_in_dir(pics_dir / "tats"))
    render("gallery.html", "mu", pics=pics_in_dir(pics_dir / "mu"))
    print("💪 Generated pages")

    copytree("static", "out/", dirs_exist_ok=True)
    print("💪 Copied static assets")

    copy2("static/guli.scss", "out/guli.scss")
    run(["sass", "out/guli.scss", "out/guli.css"])
    print("💪 Generated CSS")
