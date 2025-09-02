python3 draw.py
cd renders
for f in *.gif; do
    ffmpeg -i "$f" -c:v libvpx-vp9 -b:v 0 -crf 30 \
        -pix_fmt yuv420p -row-mt 1 \
        -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" \
        "${f%.gif}.webm"
done
cd ..
