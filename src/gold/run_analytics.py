import duckdb
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SQL_DIR = PROJECT_ROOT / "sql"

con = duckdb.connect()

print("=" * 90)
print("                 RETAILPULSE BUSINESS ANALYTICS")
print("=" * 90)

sql_files = sorted(SQL_DIR.glob("*.sql"))

if not sql_files:
    raise FileNotFoundError("No SQL files found in the sql directory.")

try:
    for sql_file in sql_files:
        print("\n" + "=" * 90)
        print(sql_file.stem.replace("_", " ").upper())
        print("=" * 90)

        query = sql_file.read_text()
        results = con.execute(query)

        columns = [description[0] for description in results.description]
        rows = results.fetchall()

        print(" | ".join(columns))
        print("-" * 90)

        for row in rows:
            print(" | ".join(str(value) for value in row))

        print(f"\nTotal rows returned: {len(rows)}")

finally:
    con.close()

print("\nALL ANALYTICAL QUERIES EXECUTED SUCCESSFULLY")
