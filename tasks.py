import os
from datetime import datetime
from functools import partial
from pathlib import Path
from shutil import copy2, copytree, rmtree
from typing import Iterator, List, Tuple

from invoke import Config, task
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

from gallery import render_category

# chdir to project root
os.chdir(Path(__file__).parent.absolute())


@task
def optimize_pics(c):
    for f in Path("./static/pics/").rglob("*.*"):
        if f.suffix != ".webp":
            with c.cd(f.parent):
                c.run(f"convert {f.name} {f.stem}.webp")
            f.rename(Path(f"~/.local/share/Trash/{f.name}").expanduser())


@task
def sync(c):
    c.run('rclone --verbose sync "Nextcloud:/אביגיל" ./static/pics')


@task
def generate(c):
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
    c.run("sass out/guli.scss out/guli.css")
    print("💪 Generated CSS")


@task(sync, generate)
def publish(c):
    c.run("rsync -Aax --delete ./out/ www-data@avocadosh.xyz:/var/www/avigail/")


@task(generate)
def watch(c):
    server = Server()

    server.watch("static/", partial(generate, c=c))
    server.watch("templates/", partial(generate, c=c))

    server.serve(root="out/")
