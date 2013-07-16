from django import forms
from models import Article, Comment, DPC_data

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'algorithm', 'angle_start', 'angle_end', 'angle_step', 'notes', 'upload_file')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'body')


class DPC_Form(forms.ModelForm):

    class Meta:
        model = DPC_data
        fields = ('title', 'notes', 'parameter1', 'parameter2')
