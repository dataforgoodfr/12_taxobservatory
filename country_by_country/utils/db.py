import psycopg2
import logging
from pypika import Query, Table, Criterion
from pypika.queries import QueryBuilder
from typing import Any


class Database:
    def __init__(self, db_host=None, db_port=None, db_user=None, db_password=None, db_name=None) -> None:
        if not (db_host and db_port and db_user and db_password and db_name):
            logging.warning("No database connection information provided, results won't be persisted")
            self.conn = None
        else:
            self.conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                database=db_name,
            )

    def _query(self, query: str | QueryBuilder, autocommit:bool = True) -> list[tuple[Any, ...]]:
        """
        Executes the query and returns the result. 
        If autocommit is True, changes are committed to the database.
        Returns a list of tuples, each tuple representing a row.
        """
        if isinstance(query, QueryBuilder):
            query = str(query)
        if self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query)
                if autocommit:
                    self.conn.commit()
                return cur.fetchall()
        else:
            raise Exception("This instance holds no database connection")

    def get_or_create_v1(self, table_name: str, column: str, value: Any) -> list[tuple[Any, ...]]:
        """
        In table_name, returns the row where column == value if it exists, 
        otherwise creates it.
        Creation only works if table requires only this single column / value to create a row.
        """
        get_query = Query.from_(table_name).select("*").where(column == value)
        queried_value = self._query(get_query, autocommit=False)
        if len(queried_value) == 0:
            insert_query = Query.into(table_name).columns(column).insert(value)
            new_row = self._query(insert_query)
            return new_row
        if len(queried_value) >= 1:
            return queried_value
        
    def get_or_create_v2(self, table_name: str, insert_dict: dict[str, Any]) -> list[tuple[Any, ...]]:
        """
        Get all entries in table_name where all the key-value pairs in insert_dict match. 
        Create a new row if no such row exists.
        """
        table = Table(table_name)
        get_query = Query.from_(table).select("*")
        get_query = get_query.where(
            Criterion.all([
                getattr(table, key) == value for key, value in insert_dict.items()
            ])
        )
        queried_value = self._query(get_query, autocommit=False)
        if len(queried_value) == 0:
            insert_query = Query.into(table).columns(*[insert_dict.keys()]).insert(*[insert_dict.values()])
            new_row = self._query(insert_query)
            return new_row
        if len(queried_value) >= 1:
            return queried_value
            


# def save_to_db(db: Database) -> None:
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             config = kwargs.get("config") 
#             result = func(*args, **kwargs)
#             extractor = db.get_or_create_v1("table_extractors", "name", config["table_extraction"]["type"])
#             extractor_params =
#             db._write(result)
#             return result
#         return wrapper
#     return decorator
    

if __name__ == "__main__":
    import pandas as pd
    import io
    df = pd.DataFrame({
        "a": [1, 2, 3],
        "b": [4, 5, 6]
    })
    buffer = io.BytesIO()
    df.to_pickle(buffer)
    df_bytes = buffer.getvalue()
    db = Database("localhost", 5400, 'postgres', 'postgres', 'extract_db')
    llm_extr_data = {
        'document_id': '1234',
        'table_extractor_id': '1',
        "table_extractor_params_id": '1',
        "llm_model_id": 1,
        "llm_model_params_id": 56,
        "data": df_bytes
    }
    db.get_or_create_v2('llm_extracted_data', llm_extr_data)
