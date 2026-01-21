from typing import Annotated, Literal
from symbolnav import LaTeXMathExtractor
from symbolnav import SymbolExtractor
from symbolnav import Renderer
import tyro


def main(
    file: str, 
    /, 
    list_symbols: Annotated[bool, tyro.conf.arg(aliases=("-l",))] = False, 
    latex_table: Annotated[bool, tyro.conf.arg(aliases=("-t",))] = False,
    ignore_errors: Annotated[bool, tyro.conf.arg(aliases=("-i",))] = False,
    sort: Annotated[bool, tyro.conf.arg(aliases=("-s",))] = False,
):
    renderer = Renderer()
    symbol_extractor = SymbolExtractor()
    latex_math_extractor = LaTeXMathExtractor()
    latex_math = list(latex_math_extractor.analyze(file=file))

    latex_symbols = {}
    for latex_math in latex_math:
        for symbol in symbol_extractor.extract_symbol(
            latex_math.value,
            file=file,
            line=latex_math.line,
            column=latex_math.column,
            ignore_errors=ignore_errors
        ):
            if symbol is None: continue
            symbol = renderer.to_latex(symbol)
            latex_symbols[symbol] = latex_math
    
    # latex_symbols = list(latex_symbols.keys())
    # if sort:
    #     pass
    if list_symbols:
        for symbol in sorted(latex_symbols.keys()):
            print(f"{symbol:.<30}: in File {file}, line {latex_symbols[symbol].line}, column {latex_symbols[symbol].column + 1}")
    if latex_table:
        print(renderer.to_latex_table(list(latex_symbols.keys()), num_cols=6))

def run():
    tyro.cli(main)

if __name__ == "__main__":
    run()