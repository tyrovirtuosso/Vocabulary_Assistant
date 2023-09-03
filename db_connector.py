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

import bcrypt
from email_validator import validate_email, EmailNotValidError


load_dotenv()


class AWS_POSTGRE:
    def __init__(self):
        connected = False
        while not connected:
            try:
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
                Email VARCHAR(255) UNIQUE NOT NULL,
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
                BoxNumber INT DEFAULT 1,           
                SuccessfulCompletions INT DEFAULT 0,
                NextReviewDate DATE DEFAULT current_date,
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
        
    def create_user(self, userid, email, password, maxlearningwords):
        # Generate a random salt
        salt = bcrypt.gensalt()
        
        # Hash the plain text password with the salt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        try:
            # Validate the email address
            valid = validate_email(email)
            
            # Get the validated email address
            validated_email = valid.email
            
        except EmailNotValidError as e:
            print(f"Invalid email address: {e}")
        
        try:
            # Insert the user into the Users table
            self.cursor.execute(
                "INSERT INTO Users (Username, Email, Password, MaxLearningWords) VALUES (%s, %s, %s, %s)",
                (userid, validated_email, hashed_password.decode('utf-8'), maxlearningwords)
            )
            
            self.conn.commit()
            
            print(f"User {userid} added successfully")
        except Error as e: 
            self.conn.rollback()
    
    def user_login(self, userid, email, password):
        self.cursor.execute("SELECT Password FROM Users WHERE Username = %s and Email = %s", (userid, email))
        result = self.cursor.fetchone()
        
        if result:
            stored_hashed_password = result[0].encode('utf-8')  # Get the stored hashed password from the query result

            # Verify the provided password by hashing it with the stored salt and comparing to the stored hash
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
                print("Login successful")
            else:
                print("Login failed: Incorrect password")
        else:
            print("Login failed: Username not found")