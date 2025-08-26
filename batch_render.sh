python3 draw.py
cd renders
for f in *.gif; do
    ffmpeg -i "$f" -c:v libwebp -lossless 0 -qscale 50 -preset picture -loop 0 -an "${f%.gif}.webp"
done
cd ..
