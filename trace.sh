#!/bin/bash
# Stone Story RPG font tracing program by link2_thepast


#use 'rename s/_\\ *' to strip _ from a_.png, b_.png, etc. if you want

spc_dir=./special-glyphs
png_dir=./glyphs
bmp_dir=./bitmaps
svg_dir=./vectors

rm -r $bmp_dir
rm -r $svg_dir

mkdir $bmp_dir
mkdir $svg_dir

echo "Tracing glyphs..."
for file in $spc_dir/* $png_dir/*
do
  name=$(basename -- "$file" .png)
  echo "Tracing glyph $name"

  #assume block glyphs are already cropped, since cropdetect won't work
  if [ "$name" = "full-block" ] || [ "$name" = "upper-half" ] || [ "$name" = "lower-half" ]; then
    ffmpeg -nostdin -y -loglevel quiet -i $file $bmp_dir/$name.bmp
  else
    cropvalue=$(ffmpeg -loop 1 -i $file -frames:v 5 -vf cropdetect=24:2:1 -f null - 2>&1 | awk '/crop/ {print $NF}' | tail -1)
    #ffmpeg -nostdin -y -loglevel quiet -i $file -vf $cropvalue $bmp_dir/$name.bmp
    #ffmpeg -nostdin -y -loglevel quiet -i $file -vf "$cropvalue, scale=22:40:flags=neighbor" $bmp_dir/$name.bmp
    ffmpeg -nostdin -y -loglevel quiet -i $file -vf "$cropvalue, pad=22:40:(ow-iw)/2:(oh-ih)/2:white" $bmp_dir/$name.bmp
  fi

  autotrace -background-color=FFFFFF -filter-iterations=0 -corner-threshold=180 -corner-always-threshold=180 -line-reversion-threshold=1000.0 -line-threshold=2 -output-format=svg -output-file=$svg_dir/$name.svg -input-format=bmp $bmp_dir/$name.bmp
done

echo "Generating font with FontForge..."
fontforge -script fontforge_generate_ssrpg.py
echo "Done processing glyphs!"
