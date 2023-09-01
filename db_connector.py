# System and Environment
import os
import time
from dotenv import load_dotenv
from typing import Optional

# Database
import psycopg2
from psycopg2 import Error

# Error Handling
import traceback

# Data Manipulation
import pandas as pd

load_dotenv()


class AWS_POSTGRE:
    def __init__(self):
        connected = False
        while not connected:
            try:
                print(os.environ.get('AWS_POSTGRE_HOST'))
                self.conn = psycopg2.connect(
                    host=os.environ.get('AWS_POSTGRE_HOST'),
                    user=os.environ.get('AWS_POSTGRE_USERNAME'),
                    password=os.environ.get('AWS_POSTGRE_PASSWORD'),
                    port=os.environ.get('AWS_POSTGRE_PORT'),
                    database=os.environ.get('AWS_POSTGRE_DATABASE')
                )
                self.cursor = self.conn.cursor()
                self.create_tables()
                connected = True
            except Error as e:
                print("Error, cannot connect to aws db:", e)
                traceback.print_exc()
                print("trying again after 5 seconds")
                time.sleep(5)

    def create_tables(self):
        create_users_table = """
            CREATE TABLE IF NOT EXISTS Users (
                UserID serial PRIMARY KEY,
                Username VARCHAR(255) NOT NULL,
                Password VARCHAR(255) NOT NULL,
                MaxLearningWords INT -- Add more columns as needed
            );
        """

        create_categories_table = """
            CREATE TABLE IF NOT EXISTS Categories (
                CategoryID serial PRIMARY KEY,
                CategoryName VARCHAR(255) NOT NULL
            );
        """

        create_subcategories_table = """
            CREATE TABLE IF NOT EXISTS Subcategories (
                SubcategoryID serial PRIMARY KEY,
                SubcategoryName VARCHAR(255) NOT NULL,
                CategoryID INT REFERENCES Categories(CategoryID)
            );
        """
        
        create_words_table = """
            CREATE TABLE IF NOT EXISTS Words (
                WordID serial PRIMARY KEY,
                WordName VARCHAR(255) NOT NULL,
                SubcategoryID INT REFERENCES Subcategories(SubcategoryID),
                LearningStatus VARCHAR(255) NOT NULL,
                UserID INT REFERENCES Users(UserID)
            );
        """
        
        
        create_tables = [
            create_users_table,
            create_categories_table,
            create_subcategories_table,
            create_words_table
            ]
        
        for query in create_tables:
            self.cursor.execute(query)
        self.conn.commit()
        
    