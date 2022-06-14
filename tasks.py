import os
from datetime import datetime
from functools import partial
from pathlib import Path
from shutil import copy2, copytree, rmtree

from invoke import task

from gallery import is_pic_square, render_category, unique_filename

RCLONE_REMOTE_PATH = "Drive:/"

# chdir to project root
if __name__ == "tasks":
    os.chdir(Path(__file__).parent.absolute())

PICS_DIR = Path("./static/pics")
TRASH_DIR = Path(".trash")


@task
def sync(c):
    c.run(f'rclone --verbose sync "{RCLONE_REMOTE_PATH}" "{PICS_DIR}"')

    TRASH_DIR.mkdir(exist_ok=True)

    for pic in PICS_DIR.rglob("*.*"):
        # crash if pic is not exact square
        if not is_pic_square(pic):
            filename = pic.relative_to(PICS_DIR.parents[1])
            raise ValueError(f"PLEASE make {filename} a square!!!! I beg")

        # convert pic to webp if it isn't already
        if pic.suffix != ".webp":
            parent = pic.parent.absolute()
            c.run(f"convert {parent}/{pic.name} {parent}/{pic.stem}.webp")
            pic.rename(TRASH_DIR / pic.name)

    # rerunning the loop because some files have been renamed or trashed
    for pic in PICS_DIR.rglob("*.*"):
        pic.rename(pic.parent / f"{unique_filename(pic)}.webp")


@task
def generate(c, sass_bin="sass"):
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    out_dir = Path("out")

    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html"]),
    )

    print()
    print(datetime.now())

    # Fresh start 😎
    rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir()

    out_dir.joinpath("index.html").write_text(env.get_template("index.html").render())

    # Render makeup and tattoo galleries, stopping the process if one of the
    # pics isn't square, prompting the user to fix it manually (I'm not going
    # to let a machine randomly crop pics..............)
    for category in ["tats", "mu"]:
        for target_filename, html in render_category(
            category, env.get_template("pic.html"), env.get_template("gallery.html")
        ):
            out_dir.joinpath(target_filename).write_text(html)
        print(f"💪 Generated {category} category")

    copytree("static", "out/", dirs_exist_ok=True)
    print("💪 Copied static assets")

    copy2("static/guli.scss", "out/guli.scss")
    c.run(f"{sass_bin} out/guli.scss out/guli.css")
    print("💪 Generated CSS")


@task(sync, generate)
def publish(c):
    c.run("rsync -Aax --delete ./out/ www-data@avocadosh.xyz:/var/www/avigail/")


@task(generate)
def watch(c):
    from livereload import Server

    server = Server()

    server.watch("static/", partial(generate, c=c))
    server.watch("templates/", partial(generate, c=c))

    server.serve(root="out/")
