#!/usr/bin/env python

# pandoc templates
# https://pandoc.org/MANUAL.html#templates

# using two filters from pypi:
# https://github.com/tomduck/pandoc-xnos
# pandoc-include to transclude markdown files

# rules
# - everything in the core documents must be in markdown or pandoc markdown syntax
# - every conversion is different (pdf, html, docx) and requires its own templates, etc

# TODO
# - test math in all formats

import pypandoc
import click
import os
import pathlib

root_folder = pathlib.Path.cwd()
print(root_folder)


@click.command()
@click.option('-o', "--output_type", default=None, required=False, type=str)
def main(output_type):
    if output_type == "html":
        compile_to_html()
    elif output_type == "pdf":
        compile_to_pdf()
    elif output_type == "docx":
        compile_to_docx()
    elif output_type == "tex":
        compile_to_latex()
    elif output_type is None:
        compile_to_html()
        compile_to_pdf()
        compile_to_docx()
    else:
        raise ValueError(f"Output type {output_type} not recognized")


def compile_to_latex():
    print("compiling to tex")
    os.chdir(root_folder / "build/latex")
    pdoc_args = [
        '--template=template.latex',
        '--number-sections',
        '--filter',
        'pandoc-include',
        '--filter',
        'pandoc-xnos',
        '--bibliography=../assets/bibliography.bib',
        '--metadata',
        'link-citations=true',  # make citation links
        '--csl=../assets/nature.csl',
        "--citeproc",
    ]
    pypandoc.convert_file(source_file="thesis_pdf.md",
                          format='md',
                          to="tex",
                          outputfile="../../thesis.tex",
                          extra_args=pdoc_args)


def compile_to_pdf():
    """
        We should be able to use the latex directly, 
        but some of the pandoc filters act on markdown directly.
        Our latex doc should reflect this... but it doesn't...
    """
    compile_to_latex()
    print("compiling to pdf")
    os.chdir(root_folder)
    os.system(
        "cd build/latex/output; latexmk -pdf ../../../thesis.tex; cd ../../../; mv build/latex/output/thesis.pdf ."
    )
    os.system("mv build/latex/output/thesis.pdf .")


def compile_to_docx():
    '''
    https://stackoverflow.com/questions/14249811/markdown-to-docx-including-complex-template
    '''
    print("compiling to docx")
    pdoc_args = [
        '--reference-doc=build/docx/reference.docx',
        '--number-sections',
        '--filter',
        'pandoc-include',
        '--filter',
        'pandoc-xnos',
        '--bibliography=build/assets/bibliography.bib',
        '--metadata',
        'link-citations=true',  # make citation links
        '--csl=build/assets/nature.csl',
        "--citeproc",
    ]
    pypandoc.convert_file(source_file="build/docx/thesis_docx.md",
                          format='md',
                          to="docx",
                          outputfile="thesis.docx",
                          extra_args=pdoc_args)


def compile_to_html():
    print("compiling to html")
    pdoc_args = [
        '--toc',
        '--toc-depth=4',
        '--number-sections',
        '--filter',
        'pandoc-include',
        '--filter',
        'pandoc-xnos',
        '--bibliography=build/assets/bibliography.bib',
        '--metadata',
        'link-citations=true',  # make citation links
        '--csl=build/assets/nature.csl',
        '--mathml',  # this works in chrome and firefox
        "--css=pandoc.css",  # custom css
        "--include-in-header",  # custom header -- so I can add hypothesis, etc
        "build/html/header.html",
        "--template",
        "build/html/template.html",
        "--citeproc"
    ]
    pypandoc.convert_file(source_file="build/html/thesis.md",
                          to='html5',
                          outputfile="index.html",
                          format='md',
                          extra_args=pdoc_args)


if __name__ == '__main__':
    main()