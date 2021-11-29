from sqlalchemy import create_engine
import pandas as pd

# Path to sqlite, THIS MAY NOT MATCH YOUR PATH
database_path = "../Resources/Census_Data.sqlite"

# Create an engine that can talk to the database
engine = create_engine(f"sqlite:///{database_path}")
conn = engine.connect()
