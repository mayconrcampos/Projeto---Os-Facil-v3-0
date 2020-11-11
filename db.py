import sqlite3


class Db:
    def conecta_db(self):
        self.conn = sqlite3.connect("dbase.db")
        self.cursor = self.conn.cursor()
    
    def desconecta_db(self):
        self.conn.close()
    
    def cria_db(self):
        self.conecta_db()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            nome TEXT,
            contato TEXT
            );
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            descricao TEXT,
            codigo TEXT,
            valor REAL
            );
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS os (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            os TEXT,
            data TEXT,
            entrada REAL,
            total REAL,
            status TEXT
            );
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS cp (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            os TEXT,
            valor_uni REAL,
            descricao TEXT,
            qtde INTEGER,
            sub_total REAL
            );
        """)


        self.conn.commit()
        self.desconecta_db()




