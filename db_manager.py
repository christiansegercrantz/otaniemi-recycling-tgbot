import sqlite3

from sqlite3 import Error
import os



class dbManager:
    class __dbManager:
        def __init__(self, db_file_path):
            self.path = db_file_path
        def __str__(self):
            return "Connection:"+ self.conn + "Path: " + self.path

        def create_connection(self):
            # create a database connection to a SQLite database
            self.conn = None
            try:
                self.conn = sqlite3.connect(self.path)
                #print("SQlite version: {}".format(sqlite3.version))
            except Error as e:
                print(e)


        def close_connection(self):
            if self.conn:
                self.conn.close
            self.conn = None

        def create_table(self, create_table_sql):
            """ create a table from the create_table_sql statement
            :param conn: Connection object
            :param create_table_sql: a CREATE TABLE statement
            :return:
            """
            try:
                self.create_connection()
                c = self.conn.cursor()
                c.execute(create_table_sql)
            except Error as e:
                print(e)
            finally:
                self.close_connection()

        def initiate_tables(self):
            #define tables
            sql_create_items_table = """ CREATE TABLE IF NOT EXISTS items_for_sale (
                                        id integer PRIMARY KEY,
                                        status text,
                                        seller_id text NOT NULL,
                                        channel_message_id text,
                                        posted_date text,
                                        name text,
                                        description text,
                                        price text,
                                        picture_message_ids text
                                        ); """
        
            sql_create_queue_table = """CREATE TABLE IF NOT EXISTS queue (
                                        id integer PRIMARY KEY,
                                        queue_ids text NOT NULL,
                                        item_id integer NOT NULL,
                                        FOREIGN KEY (item_id) REFERENCES items_for_sale (id)
                                        );"""
        
            sql_create_pictures_table = """CREATE TABLE IF NOT EXISTS pictures (
                                        id integer PRIMARY KEY,
                                        picture_id text NOT NULL,
                                        caption_id text,
                                        item_id integer NOT NULL,
                                        FOREIGN KEY (item_id) REFERENCES items_for_sale (id)
                                        );"""
            self.create_connection()
            # create tables
            if self.conn is not None:
                # create items table
                self.create_table(sql_create_items_table)
                # create queue table
                self.create_table(sql_create_queue_table)
                # create pictures table
                self.create_table(sql_create_pictures_table)
            else:
                print("Error! cannot create the database connection.")
            self.close_connection()

        def create_item_for_sale(self, item):
            """
            Create a new item into the items_for_sale table
            :param conn:
            :param item:
            :return: item id
            """
            sql = ''' INSERT INTO items_for_sale(seller_id,status,channel_message_id,posted_date,name,description,price,picture_message_ids)
                        VALUES(?,?,?,?,?,?,?,?) '''
            self.create_connection()
            cur = self.conn.cursor()
            cur.execute(sql, item)
            self.conn.commit()

            self.close_connection()
            return cur.lastrowid
            

        def create_queuer(self, queuer):
            """
            Create a new queuer
            :param conn:
            :param queuer:
            :return: id of querer (database id)
            """

            sql = ''' INSERT INTO queue(queue_ids, item_id)
                    VALUES(?,?) '''
            self.create_connection()
            cur = self.conn.cursor()
            cur.execute(sql, queuer)
            self.conn.commit()

            self.close_connection()
            return cur.lastrowid

        def create_picture(self, picture):
            """
            Create a new queuer
            :param conn:
            :param queuer:
            :return: id of picture (database id)
            """

            sql = ''' INSERT INTO tasks(picture_id, caption_id)
                        VALUES(?,?) '''
            self.create_connection()
            cur = self.conn.cursor()
            cur.execute(sql, picture)
            self.conn.commit()

            self.close_connection()
            return cur.lastrowid
        
        def set_item_for_sale_name(self, name):
            """
            update name of a item
            :param name:
            :return: item id
            """
            sql = ''' UPDATE items_for_sale
                    SET name = ? ,
                    SET status = ?
                    WHERE id = ?'''
            self.create_connection()
            cur = self.conn.cursor()
            cur.execute(sql, name)
            self.conn.commit()

    instance = None
    def __init__(self, arg):
        if not dbManager.instance:
            dbManager.instance = dbManager.__dbManager(arg)
        else:
            dbManager.instance.val = arg
    def __getattr__(self, name):
        return getattr(self.instance, name)