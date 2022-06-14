You'll probably need:
- `invoke`, `jinja2`, and `livereload` Python libraries
- [rclone](https://rclone.org/) to sync a drive directory
- ImageMagick to verify pic size (`identify`) and convert to WEBP (`convert`)

To simply run the sync task periodically in a cron, you'll only need to install
`python3-invoke` (on Ubuntu Server)
