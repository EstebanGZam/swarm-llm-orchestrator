#!/bin/sh
# Local build for TeX installations without the Times (ptm) fonts: run ./make_fonts.sh once, then this script.
# On Overleaf or a full TeX Live, just run: pdflatex main.tex (twice).
cd "$(dirname "$0")"
[ -d fonts ] || ./make_fonts.sh
export TEXINPUTS=".:./fonts:" TFMFONTS=".:./fonts:" VFFONTS=".:./fonts:" T1FONTS=".:./fonts:" ENCFONTS=".:./fonts:" TEXFONTMAPS=".:./fonts:"
for i in 1 2; do pdflatex -interaction=nonstopmode "\\pdfmapfile{+urwlocal.map}\\input{main}" > build.log 2>&1; done
grep -E "^!|undefined|Overfull" build.log; echo "pages: $(pdfinfo main.pdf | grep Pages)"
rm -f main.aux main.out main.log
