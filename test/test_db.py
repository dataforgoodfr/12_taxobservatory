import pytest
from pytest_postgresql.factories import postgresql
from pathlib import Path
from country_by_country.database import Database
from datetime import datetime


EXTRACT_TABLES = ['table_extractors', 'table_extractor_params', 'llm_models', 'llm_model_params', 'llm_extracted_data', 'documents', 'corrected_data']

@pytest.fixture()
def extract_db(postgresql):
    with postgresql.cursor() as cur:
        sql_file = Path(__file__).parents[1] / 'tax_observatory_extract.sql'
        cur.execute(sql_file.read_text())
        postgresql.commit()
    yield postgresql

@pytest.fixture()
def extract_db_cursor(extract_db):
    with extract_db.cursor() as cur:
        yield cur

@pytest.fixture()
def database_class(extract_db):
    db = Database()
    db.conn = extract_db
    return db



def test_base_tables(extract_db_cursor):
    extract_db_cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='public'
        AND table_type='BASE TABLE';
    """)
    table_list = extract_db_cursor.fetchall()
    table_list = set([table[0] for table in table_list])
    assert table_list == set(EXTRACT_TABLES)


def test_db_create_row(database_class):
    db = database_class
    now = datetime.now()
    document_params = {
        "s3_id": "document_test_id",
        "relevant_pages": [3, 4],
        "created_at": now,
        "modified_at": now
    }
    new_document_db_entry = db.create_row("documents", document_params)
    assert new_document_db_entry == [(1, 'document_test_id', [3, 4], now, now)]