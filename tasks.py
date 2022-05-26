import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from multiprocessing import Process
from pathlib import Path

from invoke import Config, task
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from generate import main as generate_html


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


@task
def watch(c):
    def http():
        # there's no way other way to change the serving directory xd
        os.chdir("./out/")
        server_address = ("", 18361)
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
        httpd.serve_forever()

    def watch_proc_func():
        class Handler(FileSystemEventHandler):
            def on_modified(self, event: FileSystemEvent):
                if event.is_directory:
                    return
                generate(c)

        observer = Observer()
        observer.schedule(Handler(), "templates", recursive=True)
        observer.schedule(Handler(), "static", recursive=True)
        observer.start()
        observer.join()

    http_proc = Process(target=http)
    http_proc.start()

    watch_proc = Process(target=watch_proc_func)
    watch_proc.start()

    http_proc.join()
    watch_proc.join()
