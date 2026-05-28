from dataclasses import dataclass
import duckdb

@dataclass
class QueryDB:
    conn: duckdb.DuckDBPyConnection

    async def query_db(self, query_string: str):
        result = self.conn.execute(query_string).fetch_df()
        return result
