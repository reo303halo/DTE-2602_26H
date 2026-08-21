# Writing Scientific Reports in CS/Engineering — LaTeX Project

A self-contained LaTeX project for teaching bachelor students how to
write scientific reports in computer science / engineering. The
compiled PDF is both **teaching material** (it explains report
structure, style, figures/tables, citations, and common mistakes) and a
**reusable template** (every technique it teaches is demonstrated in
its own source code).

## Project layout

```
.
├── main.tex                 # Master file: preamble + document skeleton
├── references.bib           # Bibliography (biblatex/biber)
├── Makefile                 # `make` to build, `make clean` to tidy up
├── sections/
│   ├── 01_introduction.tex
│   ├── 02_structure.tex           # IMRaD structure, abstract, intro vs. background
│   ├── 03_writing_style.tex       # tense, voice, precision, consistency
│   ├── 04_figures_tables.tex      # pgfplots figure + booktabs table examples
│   ├── 05_algorithms_code.tex     # algorithm2e pseudocode + listings + equations
│   ├── 06_citations.tex           # biblatex usage, when/how to cite
│   ├── 07_latex_tips.tex          # practical LaTeX workflow tips
│   ├── 08_common_mistakes.tex     # recurring issues seen in grading
│   └── 09_checklist.tex           # pre-submission checklist
└── images/                  # drop your own figures here (includes UiT logos that is used in the document)
```

## How to compile

Requires a TeX Live / MiKTeX install with `bibtex` (for the
bibliography) and the packages used in `main.tex` (all standard, in
`texlive-full` or MiKTeX's default set — no `biber` binary needed,
see the tip in Section 6 of the guide if you'd rather use
`biblatex`/`biber`).

VSCode and other tools make work simply by running the main file,
otherwise:

```bash
make            # builds main.pdf via latexmk (runs pdflatex + bibtex as needed)
make clean      # removes all auxiliary/build files
```

Or manually:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Using this as a student template

Students can:
1. Copy the whole folder as the starting point for their own report.
2. Delete the explanatory prose in each `sections/*.tex` file but keep
   the section headings and the worked examples (figure, table,
   algorithm, listing, equation, citation) as a scaffold.
3. Replace `references.bib` with their own sources.

## Customising

- Update the title/author on the `\title`/`\author` lines in
  `main.tex`.
- Citation style is IEEE numeric by default
  (`style=ieee` in the `biblatex` package options in `main.tex`);
  swap to `style=numeric`, `style=authoryear`, or an ACM style file if
  your course uses a different convention.
- `siunitx` is mentioned in the LaTeX-tips section but not loaded by
  default, to keep the dependency list minimal — add it if your
  students will report many measurements with units.
