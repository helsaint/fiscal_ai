import json

def sql_creator(sql_json: dict):

    query_parts = {
            "select": [],
            "from": "",
            "where": [],
            "group_by": [],
            "limit": ""
            }
    
    sql_query = assemble(query_parts, sql_json)
    return sql_query
    
def build_select(query_parts, relevant_tables, joins_column):
    if(joins_column is None):
        for col in relevant_tables[0]['columns']:
            query_parts["select"].append(f"{relevant_tables[0]['table_name']}.{col['name']}")
        return
    for table in relevant_tables:
        for col in table['columns']:
            query_parts["select"].append(f"{table['table_name']}.{col['name']}")       

def build_from_and_join(query_parts, relevant_tables, joins_column):
    base_table = relevant_tables[0]['table_name']
    from_clause = base_table
        
    if (joins_column is not(None)) and (len(relevant_tables) > 1):
        base_col = joins_column[0]['column']
        for i in range(1, len(relevant_tables)):
            target_table = relevant_tables[i]['table_name']
            target_col = joins_column[i]['column']
            from_clause += f" INNER JOIN {target_table} ON {base_table}.{base_col} = {target_table}.{target_col}"
    query_parts["from"] = from_clause


def build_where(query_parts, filters):
    if filters is None:
        return
    
    for f in filters:
        val = f"'{f['value']}'" if isinstance(f['value'], str) else f['value']
        query_parts["where"].append(f"{f['table_name']}.{f['column']} {f['operator']} {val}")

def assemble(query_parts, sql_json) -> str:
        build_from_and_join(query_parts, 
                        sql_json['relevant_tables'],
                        sql_json['joins_column'])
        build_select(query_parts, sql_json['relevant_tables'], sql_json['joins_column'])
        build_where(query_parts, sql_json['filter_schema'])

        sql = f"SELECT {', '.join(query_parts['select'])}"
        sql += f" FROM {query_parts['from']}"
        
        if query_parts["where"]:
            sql += f" WHERE {' AND '.join(query_parts['where'])}"
            
        # DuckDB/SQL Standard: If we have SUMs and raw columns, we need GROUP BY
        # This is a simplified logic to auto-detect group by needs
        non_agg = [c for c in query_parts["select"] if "SUM(" not in c]
        has_agg = any("SUM(" in c for c in query_parts["select"])
        if has_agg and non_agg:
            sql += f" GROUP BY {', '.join(non_agg)}"

        return sql + ";"
        