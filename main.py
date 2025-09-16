from pathlib import Path

import click
import langs # Needed for Language to function

from language import Language
from fileParser import FileParser

@click.command()
@click.option(
    "--input-dir", "-i",
    type=click.Path(exists=True, dir_okay=True, path_type=Path),
    required=True,
    help="Project Directory"
)
@click.option(
    "--output-dir", "-o",
    type=click.Path(exists=False, dir_okay=True, path_type=Path),
    required=True,
    help="Output Directory"
)
@click.option(
    "--languages", "-l",
    type=click.Choice(list(Language.all_languages().keys()), case_sensitive=False),
    required=True,
    multiple=True,
    help="Programming languages to parse"
)
def main(input_dir: Path, output_dir: Path, languages: list[str]) -> None:
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

if __name__ == "__main__":
    main()
