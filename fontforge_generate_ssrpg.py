# -*- coding: utf-8 -*-
#Stone Story RPG font tracing program by link2_thepast
import fontforge
import psMat
import tempfile
import shutil
import os

from contextlib import contextmanager

#parameters
font_name = "StoneStoryRPG"

font_file = 'ssrpg.ttf'
proj_file = 'ssrpg.sfd'

bmp_dir = './bitmaps'
svg_dir = './vectors'

back_lyr = "Back"
fore_lyr = "Fore"

t_scale = 25
t_dx = 0
t_dy = -19200
t_width = 550
t_height = 820

#unicode codepoints for special characters
spc_dict = {
  "backslash"     : 92,
  "colon"         : 58,
  "double-quote"  : 34,
  "greater-than"  : 62,
  "less-than"     : 60,
  "percent"       : 37,
  "period"        : 46,
  "pipe"          : 124,
  "question-mark" : 63,
  "slash"         : 47,
  "space"         : 32,
  "star"          : 42,
  "full-block"    : 9608,
  "lower-half"    : 9604,
  "upper-half"    : 9600
}

#helper function for parsing unicode codepoint
def get_codepoint(str):
  pt = spc_dict.get(str)

  if pt is not None:
    return pt
  return ord( str[0] )

#context manager to sanitize unicode filenames
@contextmanager
def tmp_symlink(fname):
  target = tempfile.mktemp(suffix=os.path.splitext(fname)[1])
  fname = os.path.normpath(os.path.abspath(fname))

  try:
    os.symlink(fname, target)
    yield target
  finally:
    if os.path.exists(target):
      os.remove(target)

#create font object
ssrpg = fontforge.font()

ssrpg.encoding = "UnicodeBMP"
ssrpg.fontname = font_name
ssrpg.fullname = font_name
ssrpg.familyname = font_name

for glyph_svg in os.listdir(svg_dir):
  #parse glyph file paths from filesystem
  glyph_basename = os.path.basename(glyph_svg)
  glyph_name = os.path.splitext(glyph_basename)[0]

  glyph_svg = os.path.join(svg_dir, glyph_svg)
  glyph_bmp = os.path.join(bmp_dir, glyph_name + '.bmp')

  #get glyph name as single unicode char
  glyph_name = unicode(glyph_name, 'utf-8')

  glyph_ord = get_codepoint(glyph_name)

  #add glyph to font
  print("Processing glyph %s (codepoint 0x%04x)" % (unichr(glyph_ord), glyph_ord) )
  glyph = ssrpg.createChar(glyph_ord)

  #import glyph points
  if glyph_name != 'space':
    glyph.activeLayer = fore_lyr
    with tmp_symlink(glyph_svg) as glyph_svg_no_unicode:
      glyph.importOutlines(glyph_svg_no_unicode)

  #transform points to fit
  scale = psMat.scale(t_scale)
  glyph.transform(scale)

  translate = psMat.translate(t_dx, t_dy)
  glyph.transform(translate)

  #misc cleanup
  glyph.width = t_width
  glyph.vwidth = t_height
  glyph.correctDirection()
  glyph.simplify()

  #import bitmap for reference image
  glyph.activeLayer = back_lyr
  with tmp_symlink(glyph_bmp) as glyph_bmp_no_unicode:
    glyph.importOutlines(glyph_bmp_no_unicode)

#fix font em size and integral alignment
ssrpg.em = 1024

#save FontForge project and generate font
ssrpg.save(proj_file)
#ssrpg.generate(font_file)
