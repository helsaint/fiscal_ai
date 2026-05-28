import duckdb
import json
import streamlit as st

class DuckDB:
    def __init__(self, data_dictionary):
        self.duck_db_conn = duckdb.connect(':memory:')
        self.data_dictionary = data_dictionary

    def ingest_dataframe(self, df, table_name):
        table_name = table_name
        #self.duck_db_conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
        self.duck_db_conn.register(table_name, df)

    def create_data_schema_db(self):
        self.duck_db_conn.execute("""
                                  CREATE OR REPLACE TABLE DATA_SCHEMA (
                                  table_name TEXT PRIMARY KEY, description TEXT, grain TEXT, 
                                  primary_keys TEXT[], join_hints TEXT[], columns JSON
                                  );
                                  """)
        insert_data = []
        for i in self.data_dictionary:
            row = (
                i.get('table_name'),
                i.get('description'),
                i.get('grain'),
                i.get('primary_keys', []),
                i.get('join_hints', []),
                json.dumps(i.get('columns', {})) # Convert dict to JSON string
                )
            insert_data.append(row)
            
    
        self.duck_db_conn.executemany(
            "INSERT INTO DATA_SCHEMA VALUES (?, ?, ?, ?, ?, ?);",insert_data
            )
        
    def test_db(self):
        #print(self.duck_db_conn.execute("SELECT * FROM master_ministry_fiscal_intelligence LIMIT 3").fetchdf())
        print("____________________________Load DuckDB_______________________________")
        print(self.duck_db_conn.execute("SELECT table_name, description FROM DATA_SCHEMA").fetch_df())

    def execute(self, sql: str):
        """
        Wrapper to allow the class to behave like a standard DuckDB connection.
        """
        return self.duck_db_conn.execute(sql)

    def query(self, sql: str):
        """
        Returns results as a Relation or DataFrame for easier analysis.
        """
        return self.duck_db_conn.sql(sql)
    
    def executemany(self, sql: str, data_list: list):
        self.duck_db_conn.executemany(sql, data_list)
        
@st.cache_resource
def get_duckdb(data_dictionary: dict):
    return DuckDB(data_dictionary=data_dictionary)
