#!/bin/sh
# Builds paper/fonts/: a Times clone (URW Nimbus Roman) for TeX installations without the ptm fonts.
# Not needed on Overleaf or a full TeX Live. Needs the urw-base35 fonts and t1utils (t1disasm, t1asm).
set -e
cd "$(dirname "$0")"
U=${URW_DIR:-/usr/share/fonts/type1/urw-base35}
mkdir -p fonts && cd fonts
cp "$(kpsewhich ec.enc)" ec.enc
: > urwlocal.map
for pair in NimbusRoman-Regular:urwptmr NimbusRoman-Italic:urwptmri NimbusRoman-Bold:urwptmb NimbusRoman-BoldItalic:urwptmbi; do
  f=${pair%%:*}; t=${pair##*:}
  t1disasm "$U/$f.t1" > "$f.raw" && t1asm -b "$f.raw" "$f.pfb" && rm "$f.raw"          # normalised PFB for pdfTeX
  afm2tfm "$U/$f.afm" -T ec.enc -v "$t" "$t-raw.tfm" > /dev/null 2>&1 || true                        # virtual font keeps TeX ligatures
  vptovf "$t.vpl" "$t.vf" "$t.tfm" > /dev/null 2>&1 || true
  echo "$t-raw $f \" ECEncoding ReEncodeFont \" <ec.enc <$f.pfb" >> urwlocal.map
done
afm2tfm "$U/NimbusRoman-Regular.afm" -T ec.enc -V urwptmrc urwptmrc-raw.tfm > /dev/null 2>&1 || true        # small caps
vptovf urwptmrc.vpl urwptmrc.vf urwptmrc.tfm > /dev/null 2>&1 || true
echo "urwptmrc-raw NimbusRoman-Regular \" ECEncoding ReEncodeFont \" <ec.enc <NimbusRoman-Regular.pfb" >> urwlocal.map
rm -f ./*.vpl
cat > t1ptm.fd <<'FD'
\ProvidesFile{t1ptm.fd}[2026/10/07 local URW Nimbus Roman as ptm]
\DeclareFontFamily{T1}{ptm}{}
\DeclareFontShape{T1}{ptm}{m}{n}{<-> urwptmr}{}
\DeclareFontShape{T1}{ptm}{m}{it}{<-> urwptmri}{}
\DeclareFontShape{T1}{ptm}{m}{sc}{<-> urwptmrc}{}
\DeclareFontShape{T1}{ptm}{m}{sl}{<->ssub * ptm/m/it}{}
\DeclareFontShape{T1}{ptm}{b}{n}{<-> urwptmb}{}
\DeclareFontShape{T1}{ptm}{b}{it}{<-> urwptmbi}{}
\DeclareFontShape{T1}{ptm}{b}{sc}{<->ssub * ptm/m/sc}{}
\DeclareFontShape{T1}{ptm}{b}{sl}{<->ssub * ptm/b/it}{}
\DeclareFontShape{T1}{ptm}{bx}{n}{<->ssub * ptm/b/n}{}
\DeclareFontShape{T1}{ptm}{bx}{it}{<->ssub * ptm/b/it}{}
\DeclareFontShape{T1}{ptm}{bx}{sc}{<->ssub * ptm/m/sc}{}
\DeclareFontShape{T1}{ptm}{bx}{sl}{<->ssub * ptm/b/it}{}
FD
echo "fonts/ ready"
