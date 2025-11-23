from supabase import Client
import pandas as pd
from datetime import datetime
from pathlib import Path

tables = [
    {"schema": "public", "table": "profiles"},
    {"schema": "public", "table": "history"},
    {"schema": "public", "table": "logs"},
]

class Backup:
    @staticmethod
    def create(db: Client):
        for table in tables:
            response = db.table(table["table"]).select("*").execute()
            
            if not response:
                raise RuntimeError(f"Error getting data from {table["schema"]}.{table['table']}")

            df = pd.DataFrame(response.data)

            date = datetime.now()
            date = str(date.strftime("%Y;%m;%d-%H;%M;%S"))
            save_path = Path(f'{date}-{table["schema"].upper()}{table['table']}.csv')
            save_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(save_path, index=False)