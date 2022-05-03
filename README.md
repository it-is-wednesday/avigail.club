Files are synced using [rclone](https://rclone.org/). Run `rclone config` with
your favorite drive (e.g. [Nextcloud](https://rclone.org/webdav/) or [Google
Drive](https://rclone.org/drive/)), then:

```shell
rclone --verbose sync "remotename:/remotepath" ./static/pics
```

In this case:  
`remotename` = Nextcloud  
`remotepath` = אביגיל
