import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("logs.db")

query = """
SELECT endpoint, COUNT(*) as visits
FROM server_logs
GROUP BY endpoint
ORDER BY visits DESC
LIMIT 10;
"""

df = pd.read_sql(query, conn)

plt.figure(figsize=(10, 6))

plt.barh(df["endpoint"], df["visits"])

plt.xlabel("Visits")
plt.ylabel("Endpoint")
plt.title("Top 10 Most Visited Endpoints")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.show()

conn.close()