import peewee as pw
from gallery.db import db
from .base_model import Base
from peewee import ManyToManyField

__all__ = [
    "Region",
    "Tribe",
    "Artist",
    "Artifact",
    "ArtifactType",
    "Image",
    "Exhibition",
    "User",
    "Comment",
    "ArtifactArtistThrough",
    "UserRoleThrough",
    "ExhibitionArtifactThrough"
]

class Region(Base):
    id = pw.AutoField()
    name = pw.TextField(unique=True)
    created_datetime = pw.DateTimeField()
    modified_datetime = pw.DateTimeField()

class Tribe(Base):
    id = pw.AutoField()
    name = pw.TextField(unique=True)
    region = pw.ForeignKeyField(Region, backref="tribes")
    created_datetime = pw.DateTimeField()
    modified_datetime = pw.DateTimeField()

class Artist(Base):
    id = pw.AutoField()
    name = pw.TextField()
    region = pw.ForeignKeyField(Region, backref='artists')
    tribe = pw.ForeignKeyField(Tribe, backref='artists')
    created_datetime = pw.DateTimeField()
    modified_datetime = pw.DateTimeField()

class ArtifactType(Base):
    id = pw.AutoField()
    name = pw.TextField(unique=True)
    description = pw.TextField(null=True)
    created_datetime = pw.DateTimeField()
    modified_datetime = pw.DateTimeField()

    class Meta: # your lsp is gaslighting you this is fine
        table_name = 'artifact_type'

class Artifact(Base):
    id = pw.AutoField()
    title = pw.TextField(unique=True)
    description = pw.TextField(null=True)
    date_authored = pw.DateField(null=True) # authored specified to not confuse with a possible create_date for db objects
    display_location = pw.TextField(null=True)
    artifact_type = pw.ForeignKeyField(ArtifactType, backref='artifacts', null=True)
    created_datetime = pw.DateTimeField()
    modified_datetime = pw.DateTimeField()
    artists = ManyToManyField(Artist, backref='artifacts')  # Place ManyToManyField here

class Image(Base):
    id = pw.AutoField()
    url = pw.TextField(unique=True)  # URL to the image file
    height = pw.IntegerField(null=True)  # Height of the image in pixels
    width = pw.IntegerField(null=True)  # Width of the image in pixels
    rights = pw.TextField(null=True)  # Rights information for the image
    artifact = pw.ForeignKeyField(Artifact, backref='images', null=True)  # Optional link to an artifact
    created_datetime = pw.DateTimeField()
    modified_datetime = pw.DateTimeField()

class Exhibition(Base):
    id = pw.AutoField()
    name = pw.TextField(unique=True)
    description = pw.TextField(null=True)
    start_date = pw.DateField()
    end_date = pw.DateField()
    location = pw.TextField()
    artifacts = ManyToManyField(Artifact, backref='exhibitions')  # Add ManyToManyField here

class Role(Base):
    id = pw.AutoField()
    name = pw.TextField(unique=True)  
    description = pw.TextField(null=True) 
    created_datetime = pw.DateTimeField()
    modified_datetime = pw.DateTimeField()

class User(Base):
    id = pw.AutoField()
    first_name = pw.TextField()
    last_name = pw.TextField() 
    username = pw.TextField(unique=True)
    email = pw.TextField(unique=True)  
    password_hash = pw.TextField()  
    created_datetime = pw.DateTimeField()
    modified_datetime = pw.DateTimeField()
    roles = ManyToManyField(Role, backref='users')

class Comment(Base):
    id = pw.AutoField()
    content = pw.TextField()
    author = pw.ForeignKeyField(User, backref='comments')  # Link to the user who made the comment
    artifact = pw.ForeignKeyField(Artifact, backref='comments')  # Optional link to an artifact
    parent_comment = pw.ForeignKeyField('self', backref='comments', null=True)  # Self-referential foreign key for replies
    created_datetime = pw.DateTimeField()
    modified_datetime = pw.DateTimeField()

    @property
    def is_top_level(self): # because i can't get generated properties to work with peewee 
        return self.parent_comment is None

# After all model definitions, initialize the M2M tables
ArtifactArtistThrough = Artifact.artists.get_through_model()
UserRoleThrough = User.roles.get_through_model()
ExhibitionArtifactThrough = Exhibition.artifacts.get_through_model()
