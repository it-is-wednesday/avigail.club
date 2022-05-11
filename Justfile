sync:
    rclone --verbose sync "Nextcloud:/אביגיל" ./static/pics

watch:
    @# https://github.com/k-bx/par
    par "python -m http.server --directory out 18361" \
        "watchexec python generate.py -w generate.py -w templates -w static --restart"

publish: sync
    rsync -Aax --delete ./out/ www-data@avocadosh.xyz:/var/www/avigail/
