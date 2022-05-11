You'll probably want:
- [rclone](https://rclone.org/) to sync a drive directory
- ImageMagick to verify pic size (`identify`) and convert to WEBP (`convert`)

# Optimizing the pics
Pics are heavy... :( Here's a shell snippet that converts your pictures to webp
and shrinks them (assuming they're larger than 768x768):

``` shell
#!/bin/sh

mkdir -p ~/.local/share/Trash

for filename in *; do
    # only iterate on things ImagaeMagick can parse, meaning: pictures. print
    # the filename without extension
    if identify -format "%t\n" "$filename" 2> /dev/null; then
        out="${filename%.*}.webp"
        convert -quality 70 -resize 768x768 "$filename" "$out"

        # in case the file we converted is already webp, there's no need to
        # delete it
        if [ "$filename" != "$out" ]; then
            mv "$filename" ~/.local/share/Trash
        fi
    fi
done
```
