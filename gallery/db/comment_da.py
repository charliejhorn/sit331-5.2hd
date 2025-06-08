from playhouse.shortcuts import model_to_dict, dict_to_model
from gallery.models import Comment, Artifact, User

class CommentDataAccess:
    def get_all_comments(self):
        return [model_to_dict(comment) for comment in Comment.select()]

    def add_comment(self, comment):
        comment = Comment.create(**comment)
        return model_to_dict(comment)

    def delete_comment(self, id):
        Comment.delete_by_id(id)
        
        pass

    def get_comment(self, id):
        return model_to_dict(Comment.get_by_id(id))

    def update_comment(self, comment):
        Comment.update(comment).where(Comment.id == int(comment["id"]))

