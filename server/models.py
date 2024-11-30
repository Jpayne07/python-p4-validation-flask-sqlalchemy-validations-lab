from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Authors need a name")
        existing_author = Author.query.filter_by(name=name).first()
        if existing_author:
            raise ValueError(f"An author with the name '{name}' already exists.")
        return name
    
    @validates('phone_number')
    def validate_phone(self, key, phone_number):
        if len(phone_number) !=10:
            raise ValueError(f"Phone number must be exactly 10 characters.")
        print(type(phone_number))
        if not isinstance(int(phone_number), int):
            raise ValueError(f"Phone number must be integer.")
        return phone_number
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    

    # Add validators  
    @validates('content')
    def validate_content(self, key, content):
        if len(content)< 250:
            raise ValueError("Content must be at least 250 characters long")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary)> 250:
            raise ValueError("summary must be no more than 250 characters long")
        
    @validates('category')
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError("Category must be Fiction or Non-Fiction.")
        return category

    @validates('title')
    def validate_title(self, key, title):
        clickbaits = ["Won't Believe", "Secret", "Top", "Guess"]
        # Check if any clickbait word is in the title
        if not title:
            raise ValueError("Post must have title") 
        if any(clickbait in title for clickbait in clickbaits):
            return title
        else:
            raise ValueError("Post title must have clickbait")
                  


        
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
