# System and Environment
import os
import time
from dotenv import load_dotenv
from typing import Optional
import json

# Database
import psycopg2
from psycopg2 import Error

# Error Handling
import traceback

# Data Manipulation
import pandas as pd

import bcrypt
from email_validator import validate_email, EmailNotValidError
from categories import category_subcategory_dict
from words import words


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
                CategoryName VARCHAR(255) UNIQUE NOT NULL
            );
        """
        
        create_words_table = """
            CREATE TABLE IF NOT EXISTS Words (
                WordID serial PRIMARY KEY,
                WordName VARCHAR(255) UNIQUE NOT NULL,
                CategoryID INT REFERENCES Categories(CategoryID),     
                BoxNumber INT DEFAULT 1,           
                SuccessfulCompletions INT DEFAULT 0,
                NextReviewDate DATE DEFAULT current_date,
                UserID INT REFERENCES Users(UserID)
            );
        """
        
        
        create_tables = [
            create_users_table,
            create_categories_table,
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
        self.cursor.execute("SELECT UserID, Password FROM Users WHERE Username = %s and Email = %s", (userid, email))
        result = self.cursor.fetchone()
        
        if result:
            stored_user_id = result[0] 
            stored_hashed_password = result[1].encode('utf-8')  
            
            # Verify the provided password by hashing it with the stored salt and comparing to the stored hash
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
                print("Login successful")
                return stored_user_id 
            else:
                print("Login failed: Incorrect password")
                return None
        else:
            print("Login failed: Username not found")
            return None
    
    def insert_category(self, category_name):
        def category_exists(category_name):
            self.cursor.execute("SELECT CategoryName FROM Categories WHERE CategoryName = %s", (category_name,))
            return self.cursor.fetchone() is not None

        try:
            # Iterate through the dictionary
            if not category_exists(category_name):
                                
                # Insert the category into the Categories table
                self.cursor.execute("INSERT INTO Categories (CategoryName) VALUES (%s) RETURNING CategoryID", (category_name,))
                category_id = self.cursor.fetchone()[0]  # Get the inserted CategoryID
                
                # Commit the transaction
                self.conn.commit()

        except Exception as e:
            self.conn.rollback()  # Rollback in case of an error
            print(f"Error: {e}")
            
    def insert_words(self, ai, user_id):
        def word_exists(word_name):
            self.cursor.execute("SELECT WordName FROM Words WHERE WordName = %s", (word_name,))
            return self.cursor.fetchone() is not None   
        
        def extract_category(word):
            category = ai.get_category(word)
            return category
        
        def get_category_id(category):
            self.cursor.execute("SELECT CategoryID FROM Categories WHERE CategoryName = %s", (category,))
            category_id = self.cursor.fetchone()
            if category_id:
                return category_id[0]
        
        try:
            corrected_words = ai.spelling_corrector(words)
            
            for word in corrected_words:                                                
                # Check if the word already exists
                if not word_exists(word):                                        
                    category = extract_category(word)
                    self.insert_category(category)
                    category_id = get_category_id(category)
                    self.cursor.execute(
                        "INSERT INTO Words (WordName, CategoryID, UserID) VALUES (%s, %s, %s)",
                        (word, category_id, user_id)  # Replace subcategory_id and user_id with appropriate values
                    )                    
                    print(f"Inserted word {word} of category {category}")

            # Commit the transaction
            self.conn.commit()
            print("Words inserted successfully")

        except Exception as e:
            self.conn.rollback()  # Rollback in case of an error
            print(f"Error: {e}")