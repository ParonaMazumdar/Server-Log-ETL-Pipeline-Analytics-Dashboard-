import sqlite3
import pandas as pd

conn = sqlite3.connect("logs.db")

query = """
SELECT host, COUNT(*) as requests
FROM server_logs
GROUP BY host
ORDER BY requests DESC
LIMIT 10;
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()