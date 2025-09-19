from pathlib import Path

import click
import typer
from typing import Annotated

from docgen.fileParser import FileParser
from docgen.language import Language
from docgen.DocMatcher.topLevel import print_all

app = typer.Typer(rich_markup_mode="rich", add_completion=False)

@app.command()
def main(
    input_dir: Annotated[Path, typer.Argument(help="Input directory")],
    languages: Annotated[
        list[str],
        typer.Argument(
            help="List of languages to include in the generated documentation",
            click_type=click.Choice(Language.all_languages().keys()),
        ),
    ],
    output_dir: Annotated[Path, typer.Option(..., "--output-dir", "-o", help="Output directory")] = "out",
) -> None:
    fp = FileParser()

    allowed_extensions = [
        langauge.FILE_EXTENSION
        for name, langauge in Language.all_languages().items()
        if name in languages
    ]

    for path in Path(input_dir).rglob("*"):  # recursive glob
        if path.is_file():
            if path.suffix not in allowed_extensions:
                continue
            language = Language.get_language_for_file(path)

            if language:
                fp.parse_file(path, language)
            else:
                print("NOT SUPPORTED")
        elif path.is_dir():
            print("Dir:", path)
    print_all()


if __name__ == "__main__":
    app()
