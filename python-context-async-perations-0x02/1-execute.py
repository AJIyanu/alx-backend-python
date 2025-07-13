import mysql.connector

class ExecuteQuery:
    def __init__(self, config, query, params=None):
        self.config = config
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor()

        try:
            self.cursor.execute(self.query, self.params)
            if self.query.strip().lower().startswith("select"):
                self.result = self.cursor.fetchall()
            else:
                self.connection.commit()
                self.result = self.cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            raise e

        return self.result

    def __exit__(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()


config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}

with ExecuteQuery(config, "SELECT * FROM users WHERE age > ?", (25,)) as result:
    for row in result:
        print(row)