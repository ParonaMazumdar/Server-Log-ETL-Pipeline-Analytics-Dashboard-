import re
import pandas as pd
from sqlalchemy import create_engine

# Read log file
with open("data/NASA_access_log_Jul95", "r", encoding="latin-1") as file:
    lines = file.readlines()

# Regex pattern
pattern = r'(\S+) - - \[(.*?)\] "(.*?)" (\d{3}) (\S+)'

parsed_data = []

for line in lines:
    match = re.match(pattern, line)
    if match:
        parsed_data.append(match.groups())

# DataFrame
df = pd.DataFrame(
    parsed_data,
    columns=["host", "timestamp", "request", "status_code", "bytes"]
)

# Split request
request_parts = df["request"].str.split(" ", n=2, expand=True)

df["method"] = request_parts[0]
df["endpoint"] = request_parts[1]
df["protocol"] = request_parts[2]

df.drop(columns=["request"], inplace=True)

# Clean data
df["status_code"] = df["status_code"].astype(int)

df["bytes"] = pd.to_numeric(
    df["bytes"],
    errors="coerce"
).fillna(0).astype(int)

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    format="%d/%b/%Y:%H:%M:%S %z"
)

# Create database connection
engine = create_engine("sqlite:///logs.db")

# Load into SQL
df.to_sql(
    "server_logs",
    engine,
    if_exists="replace",
    index=False
)

print("Data loaded successfully into SQLite!")