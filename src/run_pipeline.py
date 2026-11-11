import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Pipeline stages in execution order
PIPELINE_STAGES = [
    {
        "name": "Bronze Ingestion",
        "script": "src/ingestion/bronze_ingestion.py"
    },
    {
        "name": "Silver Transformation",
        "script": "src/transformation/create_silver.py"
    },
    {
        "name": "Silver Relationship Validation",
        "script": "src/validation/check_silver_relationships.py"
    },
    {
        "name": "Gold Transformation",
        "script": "src/gold/create_gold.py"
    },
    {
        "name": "Business Analytics",
        "script": "src/gold/run_analytics.py"
    }
]


def run_pipeline():

    start_time = datetime.now()

    print("=" * 65)
    print("           RETAILPULSE MASTER DATA PIPELINE")
    print("=" * 65)

    print("Started:", start_time.strftime("%Y-%m-%d %H:%M:%S"))

    for index, stage in enumerate(PIPELINE_STAGES, start=1):

        script_path = PROJECT_ROOT / stage["script"]

        print("\n" + "=" * 65)
        print(f"STAGE {index}: {stage['name']}")
        print("=" * 65)

        # Check whether the script exists
        if not script_path.exists():
            print(f"ERROR: Script not found: {script_path}")
            sys.exit(1)

        try:
            subprocess.run(
                [sys.executable, str(script_path)],
                cwd=PROJECT_ROOT,
                check=True
            )

            print(f"\n{stage['name']}: SUCCESS")

        except subprocess.CalledProcessError as error:
            print(f"\n{stage['name']}: FAILED")
            print("Exit code:", error.returncode)
            print("Pipeline stopped.")
            sys.exit(error.returncode)

    end_time = datetime.now()
    duration = end_time - start_time

    print("\n" + "=" * 65)
    print("       RETAILPULSE PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 65)

    print("Started:", start_time.strftime("%H:%M:%S"))
    print("Finished:", end_time.strftime("%H:%M:%S"))
    print("Duration:", duration)


if __name__ == "__main__":
    run_pipeline()
