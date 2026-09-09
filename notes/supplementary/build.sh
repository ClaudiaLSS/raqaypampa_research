#!/usr/bin/env bash
# Assemble the per-section files into one supplementary document.
# Section order is the file order below; keep it in sync with the S-numbers.
#
#   ./build.sh                        -> supplementary_material.pdf
#   ./build.sh out.docx               -> Word (format inferred from extension)
#
# PDF output needs a LaTeX engine, which is NOT installed on this machine.
# Either install one (texlive-xetex) and add --pdf-engine=xelatex below,
# or build .docx and export to PDF from Word.
set -euo pipefail
cd "$(dirname "$0")"

FILES=(
  s0_front.md
  s1_qualitative_methodology.md
  s2_profiles_and_parameters.md
  s3_parameter_derivation.md
  s4_truth_files.md
  s5_survey_instruments.md
)

OUT="${1:-supplementary_material.pdf}"
pandoc "${FILES[@]}" --toc -o "$OUT"
echo "wrote $OUT"
