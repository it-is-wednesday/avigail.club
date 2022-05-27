import os
from pathlib import Path

from invoke import Config, task
from livereload import Server

from generate import main as generate_html

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
    generate_html()


@task(sync, generate)
def publish(c):
    c.run("rsync -Aax --delete ./out/ www-data@avocadosh.xyz:/var/www/avigail/")


@task(generate)
def watch(c):
    server = Server()

    server.watch("static/", generate_html)
    server.watch("templates/", generate_html)

    server.serve(root="out/")
