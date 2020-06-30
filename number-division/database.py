import psycopg2
import psycopg2.pool


pool = psycopg2.pool.ThreadedConnectionPool(1, 20,
                                          dbname='practise',
                                          user='simo09',
                                          host='localhost',
                                          password='practise')


class DB:
    def __enter__(self):
        self.conn = pool.getconn()
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        pool.putconn(self.conn)
