sync:
    rclone --verbose copy "Nextcloud:/אביגיל" ./static/pics

watch:
    par "python -m http.server --directory out 18361" \
        "watchexec python generate.py -w generate.py -w templates -w static --restart"
