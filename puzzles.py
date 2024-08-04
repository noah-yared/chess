import pandas as pd
import zstandard as zstd

df = pd.read_csv("./data/lichess_db_puzzle.csv.zst", compression="zstd")

print(df["FEN"][100000:100010].sort_values(), sep="\n")