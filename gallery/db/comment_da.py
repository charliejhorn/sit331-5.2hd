from playhouse.shortcuts import model_to_dict, dict_to_model
from gallery.models import Comment, Artifact, User
from peewee import DoesNotExist, IntegrityError
from gallery.utils import NotFoundException, DuplicateException
import datetime

class CommentDataAccess:
    def get_all_comments(self):
        """Get all comments"""
        return [model_to_dict(comment) for comment in Comment.select()]

    def add_new_comment(self, comment):
        """Create a new comment"""
        current_time = datetime.datetime.now()
        comment['created_datetime'] = current_time
        comment['modified_datetime'] = current_time
        
        comment = dict_to_model(Comment, comment)
        comment.save()
        return model_to_dict(comment)

    def get_comment_by_id(self, id):
        """Get a single comment by its ID"""
        try:
            comment = Comment.get_by_id(id)
            return model_to_dict(comment)
        except DoesNotExist:
            raise NotFoundException("comment", id)

    def update_comment_by_id(self, id, updated_data):
        """Update a comment by its ID"""
        try:
            comment = Comment.get_by_id(id)
            updated_data['modified_datetime'] = datetime.datetime.now()
            
            for key, value in updated_data.items():
                if hasattr(comment, key):
                    setattr(comment, key, value)
            comment.save()
            return model_to_dict(comment)
        except DoesNotExist:
            raise NotFoundException("comment", id)

    def delete_comment_by_id(self, id):
        """Delete a comment by its ID"""
        try:
            comment = Comment.get_by_id(id)
            comment.delete_instance()
        except DoesNotExist:
            raise NotFoundException("comment", id)

    def get_comments_by_artifact(self, artifact_id):
        """Get all comments for a specific artifact"""
        comments = Comment.select().where(Comment.artifact == artifact_id)
        return [model_to_dict(c) for c in comments]

    def get_comments_by_user(self, user_id):
        """Get all comments by a specific user"""
        comments = Comment.select().where(Comment.author == user_id)
        return [model_to_dict(c) for c in comments]

    def get_comments_by_artifact_and_user(self, artifact_id, user_id):
        """Get all comments for a specific artifact by a specific user"""
        comments = Comment.select().where(
            (Comment.artifact == artifact_id) & 
            (Comment.author == user_id)
        )
        return [model_to_dict(c) for c in comments]

    def get_comments_by_date_range(self, start_date, end_date):
        """Get all comments posted within a date range"""
        comments = Comment.select().where(
            (Comment.date_posted >= start_date) & 
            (Comment.date_posted <= end_date)
        )
        return [model_to_dict(c) for c in comments]

    def get_comments_by_parent_comment(self, parent_comment_id):
        """Get all replies to a specific parent comment"""
        comments = Comment.select().where(Comment.parent_comment == parent_comment_id)
        return [model_to_dict(c) for c in comments]

