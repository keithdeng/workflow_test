from django import forms
from models import Article, Comment

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'parameter1', 'save_to', 'notes')#, 'thumbnail')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'body')
