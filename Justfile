sync:
    rclone --verbose sync "Nextcloud:/אביגיל" ./static/pics

generate:
    python generate.py

watch:
    @# https://github.com/k-bx/par
    par "python -m http.server --directory out 18361" \
        "watchexec -w generate.py -w templates -w static --restart python generate.py"

publish: sync generate
    rsync -Aax --delete ./out/ www-data@avocadosh.xyz:/var/www/avigail/
