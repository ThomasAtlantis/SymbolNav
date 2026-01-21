from typing import Annotated, Literal, Optional
from symbolnav import LaTeXMathExtractor
from symbolnav import SymbolExtractor
from symbolnav import Renderer
import tyro


def main(
    file: Optional[str] = None, 
    /, 
    list_symbols: Annotated[bool, tyro.conf.arg(aliases=("-l",))] = False, 
    latex_table: Annotated[bool, tyro.conf.arg(aliases=("-t",))] = False,
    ignore_errors: Annotated[bool, tyro.conf.arg(aliases=("-i",))] = False,
    sort: Annotated[bool, tyro.conf.arg(aliases=("-s",))] = False,
    latex: Optional[str] = None,
):
    symbol_extractor = SymbolExtractor()
    latex_symbols = {}

    if file is None:
        assert latex is not None, "Either [file] or --latex must be provided"

        for symbol in symbol_extractor.extract_symbol(
            latex, file="input", line=1, column=1,
            ignore_errors=ignore_errors
        ):
            latex_symbols[symbol] = (1, 1)
        for symbol in sorted(latex_symbols.keys()):
            print(Renderer.to_latex(symbol))
    else:
        latex_math_extractor = LaTeXMathExtractor()
        latex_math = list(latex_math_extractor.analyze(file=file))
        for latex_math in latex_math:
            for symbol in symbol_extractor.extract_symbol(
                latex_math.value,
                file=file,
                line=latex_math.line,
                column=latex_math.column,
                ignore_errors=ignore_errors
            ):
                if symbol is None: continue
                latex_symbols[symbol] = (latex_math, Renderer.to_latex(symbol))
        sorted_symbols = sorted(latex_symbols.keys())
        if list_symbols:
            for symbol in sorted_symbols:
                print(f"{latex_symbols[symbol][1]:.<50}: in File {file}, line {latex_symbols[symbol][0].line}, column {latex_symbols[symbol][0].column + 1}")
        if latex_table:
            print(Renderer.to_latex_table([latex_symbols[symbol][1] for symbol in sorted_symbols], num_cols=6))

def run():
    tyro.cli(main)

if __name__ == "__main__":
    run()