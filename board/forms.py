from django import forms
from board.models import Post, Comment

from django.contrib.auth import get_user_model

User = get_user_model()

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': '제목은 3자 이상 입력해주세요.'})
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'placeholder': '내용은 10자 이상 입력해주세요.'})

    class Meta:
        model = Post
        fields = ('title', 'text',)




class SignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}))
    password = forms.RegexField(regex=r'^(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9]|.*[0-9]).{8,24}$', widget=forms.PasswordInput(attrs={'class': 'form-control',}))
    password_confirm = forms.RegexField(regex=r'^(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9]|.*[0-9]).{8,24}$', widget=forms.PasswordInput(attrs={'class': 'form-control',}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('아이디가 이미 사용중입니다.')
        return username

    def clean_password_confirm(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['password_confirm']
        if password1 != password2:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        return password2

    def signup(self):
        if self.is_valid():
            return User.objects.create_user(
                username = self.cleaned_data['username'],
                password = self.cleaned_data['password_confirm'],
            )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
