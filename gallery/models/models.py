import peewee as pw
from gallery.db import db
from .base_model import Base

# class Base(pw.Model):
#     class Meta:
#         database = db  # This model uses the "database.db" database.

# example model
# class Person(Model):
#     name = pw.CharField()
#     birthday = pw.DateField()

#     class Meta:
#         database = db # This model uses the "people.db" database.


__all__ = [
    "Base",
    "Region",
    "Tribe",
    "Artist",
    "Artifact",
    "ArtifactType",
    "ArtistArtifactJoin",
    "Image",
    "Exhibition",
    "ExhibitionArtifactJoin",
    "User",
    "Comment",
]

class Region(Base):
    id = pw.AutoField()
    name = pw.TextField()

class Tribe(Base):
    id = pw.AutoField()
    name = pw.TextField()
    region = pw.ForeignKeyField(Region, backref="tribes")

class Artist(Base):
    id = pw.AutoField()
    name = pw.TextField()
    region = pw.ForeignKeyField(Region, backref='artists')
    tribe = pw.ForeignKeyField(Tribe, backref='artists')

class ArtifactType(Base):
    id = pw.AutoField()
    name = pw.TextField()
    description = pw.TextField(null=True)

    class Meta(Base.Meta): # Your lsp is gaslighting you this is fine
        table_name = 'artifact_type'

class Artifact(Base):
    id = pw.AutoField()
    title = pw.TextField()
    description = pw.TextField(null=True)
    date_authored = pw.DateField(null=True) # authored specified to not confuse with a possible create_date for db objects
    display_location = pw.TextField(null=True)
    artifact_type = pw.ForeignKeyField(ArtifactType, backref='artifacts', null=True)

class ArtistArtifactJoin(Base):
    artist = pw.ForeignKeyField(Artist, backref='artist_artifacts')
    artifact = pw.ForeignKeyField(Artifact, backref='artifact_artists')

    class Meta(Base.Meta):
        table_name = 'artist_artifact_join'
        indexes = (
            (('artist', 'artifact'), True),  # Unique constraint on artist and artifact
        )
        primary_key = pw.CompositeKey('artist', 'artifact')

class Image(Base):
    id = pw.AutoField()
    url = pw.TextField()  # URL to the image file
    height = pw.IntegerField(null=True)  # Height of the image in pixels
    width = pw.IntegerField(null=True)  # Width of the image in pixels
    rights = pw.TextField(null=True)  # Rights information for the image
    artifact = pw.ForeignKeyField(Artifact, backref='images', null=True)  # Optional link to an artifact

class Exhibition(Base):
    id = pw.AutoField()
    name = pw.TextField()
    description = pw.TextField(null=True)
    start_date = pw.DateField()
    end_date = pw.DateField()
    location = pw.TextField()

class ExhibitionArtifactJoin(Base):
    exhibition = pw.ForeignKeyField(Exhibition, backref='exhibition_artifacts')
    artifact = pw.ForeignKeyField(Artifact, backref='artifact_exhibitions')

    class Meta(Base.Meta):
        table_name = 'exhibition_artifact_join'
        indexes = (
            (('exhibition', 'artifact'), True),  # Unique constraint on exhibition and artifact
        )
        primary_key = pw.CompositeKey('exhibition', 'artifact')

class Role(Base):
    id = pw.AutoField()
    name = pw.TextField(unique=True)  
    description = pw.TextField(null=True) 

class User(Base):
    id = pw.AutoField()
    first_name = pw.TextField()
    last_name = pw.TextField() 
    username = pw.TextField(unique=True)
    email = pw.TextField(unique=True)  
    password_hash = pw.TextField()  
    membership_type = pw.TextField()

class UserRoleJoin(Base):
    user = pw.ForeignKeyField(User, backref='user_roles')
    role = pw.ForeignKeyField(Role, backref='role_users')

    class Meta(Base.Meta):
        table_name = 'user_role_join'
        indexes = (
            (('user', 'role'), True),  # Unique constraint on user and role
        )
        primary_key = pw.CompositeKey('user', 'role')

class Comment(Base):
    id = pw.AutoField()
    content = pw.TextField()
    author = pw.ForeignKeyField(User, backref='comments')  # Link to the user who made the comment
    artifact = pw.ForeignKeyField(Artifact, backref='comments')  # Optional link to an artifact
    date_posted = pw.DateTimeField(constraints=[pw.SQL('DEFAULT CURRENT_TIMESTAMP')])  # Automatically set to current timestamp
    parent_comment = pw.ForeignKeyField('self', backref='comments', null=True)  # Self-referential foreign key for replies

    @property
    def is_top_level(self): # because i can't get generated properties to work with peewee 
        return self.parent_comment is None
