import os
import psycopg2
from linesman_postgres.postgres import PostgresBackend
from linesman.tests import (create_mock_session, get_temporary_filename,
                            SPECIFIC_DATE_EPOCH)
from linesman.tests.backends import TestBackend


class TestBackendPostgres(TestBackend):

    def setUp(self):
        # This must be configurable
        self.db = 'linesman-test'
        self.user = 'linesman-test'
        self.password = 'linesman-test'
        self.backend = PostgresBackend(db=self.db,
                                       user=self.user,
                                       password=self.password)

    def tearDown(self):
        conn = self.conn = psycopg2.connect(dbname=self.db, user=self.user,
                                            password=self.password)
        query = 'DROP TABLE sessions;'
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()

    def test_setup(self):
        """ Test that setup() creates a new table with the correct columns. """
        expected_columns = [
            (u"uuid",       u"",        1),
            (u"timestamp",  u"FLOAT",    0),
            (u"session",    u"PICKLE",   0)
        ]
