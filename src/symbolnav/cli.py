from symbolnav.latex_math_extractor.extractor import LaTeXMathExtractor
from symbolnav.symbol_extractor.extractor import SymbolExtractor
from symbolnav.renderer import Renderer
import time
import tyro


def main(file: str, /, list_symbols: bool = False, latex_table: bool = False):
    renderer = Renderer()
    symbol_extractor = SymbolExtractor()
    latex_math_extractor = LaTeXMathExtractor()
    time_start = time.time()
    file = "reference/main.tex"
    latex_math = list(latex_math_extractor.analyze(file=file))
    print(f"Elapsed time: {time.time() - time_start}")

    latex_symbols = {}
    for latex_math in latex_math:
        for symbol in symbol_extractor.extract_symbol(
            latex_math.value,
            file=file,
            source_line=latex_math.line,
            source_column=latex_math.column
        ):
            if symbol is None: continue
            symbol = renderer.to_latex(symbol)
            latex_symbols[symbol] = latex_math
    if list_symbols:
        for symbol in sorted(latex_symbols.keys()):
            print(f"{symbol:.<30}: in File {file}, line {latex_symbols[symbol].line}, column {latex_symbols[symbol].column + 1}")
    if latex_table:
        print(renderer.to_latex_table(list(latex_symbols.keys()), num_cols=6))

def run():
    tyro.cli(main)

if __name__ == "__main__":
    run()