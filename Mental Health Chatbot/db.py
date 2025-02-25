from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy
db = SQLAlchemy()

# db.py (Enhanced Dummy version with SQLAlchemy attribute placeholders)

# class DummyModel:
#     """A dummy base class for models."""
#     pass

# def dummy_column(*args, **kwargs):
#     return None

# def dummy_relationship(*args, **kwargs):
#     return None

# # Dummy placeholders for SQLAlchemy types and functions:
# DummyInteger = int
# DummyString = lambda length: str  # length is ignored in this dummy
# DummyText = str
# DummyDateTime = None  # Not used in the dummy
# DummyForeignKey = lambda x: None

# class DummySession:
#     def add(self, obj):
#         pass
#     def commit(self):
#         pass
#     def rollback(self):
#         pass
#     def query(self, model):
#         return self
#     def filter_by(self, **kwargs):
#         return self
#     def order_by(self, *args, **kwargs):
#         return self
#     def first(self):
#         return None
#     def all(self):
#         return []
#     def get(self, primary_key):
#         return None

# class DummyDB:
#     def __init__(self):
#         self._session = DummySession()
#         self.Model = DummyModel  # Base model for inheritance
        
#         # Dummy attributes to mimic SQLAlchemy's interface:
#         self.Column = dummy_column
#         self.Integer = DummyInteger
#         self.String = DummyString
#         self.Text = DummyText
#         self.DateTime = DummyDateTime
#         self.ForeignKey = DummyForeignKey
#         self.relationship = dummy_relationship
    
#     def init_app(self, app):
#         pass
    
#     def create_all(self):
#         pass
    
#     @property
#     def session(self):
#         return self._session

# # Instantiate a dummy 'db' so that "from db import db" works in your project
# db = DummyDB()
