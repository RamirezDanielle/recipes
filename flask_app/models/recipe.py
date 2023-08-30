from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash

DB = 'Recipes'
class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under30 = data['under30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
       
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(DB).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def save(cls, data):
        query = """
                INSERT INTO recipes(name,description, instructions, date_made, under30, user_id)
                VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under30)s, %(user_id)s);
                """
        return connectToMySQL(DB).query_db(query,data)

    @classmethod
    def get_one(cls,data):
        query = """
                SELECT * FROM recipes WHERE id = %(id)s;
                """
        results = connectToMySQL(DB).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def update(cls,data):
        query = """
                UPDATE recipes SET
                name=%(name)s,description=%(description)s,
                instructions=%(instructions)s,date_made=%(date_made)s,
                under30=%(under30)s, updated_at=NOW() WHERE id = %(id)s;
                """
        results = connectToMySQL(DB).query_db(query,data)
        return results

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query,data)
    
    @classmethod
    def get_all_users_recipes(cls):
        query = """SELECT * FROM recipes
                   JOIN users
                   ON recipes.user_id = users.id
                """
        results = connectToMySQL(DB).query_db(query)
        print(results)
        recipes = []
        for row in results:
            recipe = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name':row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            recipe.user = User(user_data)
            recipes.append(recipe)
        return recipes
    
    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters", "recipe")
        if len(data['instructions']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters", "recipe")
        if len(data['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters", "recipe")
            is_valid = False
        if data['date_made'] == "":
            is_valid = False
            flash("Please enter a date", "recipe")
        return is_valid
        
        