from django import forms
from .models import parent,child,books,kids_video,kids_game,book_category,video_category

class loginform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,max_length=15, min_length=5)
    class Meta():
        model = parent
        fields = ('email','password',)


class parent_regform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=15, min_length=5)
    class Meta():
        model=parent
        fields=('firstname','lastname','address','phone','email')
class editform(forms.ModelForm):
    class Meta():
        model = parent
        fields = ('firstname','lastname','address',)
class childform(forms.ModelForm):
    class Meta():
        model=child
        fields=('firstname','lastname','age','email','password',)
class videoform(forms.ModelForm):
    class Meta():
        model = kids_video
        fields =('upload_videos','upload_name','categories')
class bookform(forms.ModelForm):
    class Meta():
        model = books
        fields = ('upload_book','upload_name','categories')

class child_editform(forms.ModelForm):
    class Meta():
        model = child
        fields = ('firstname','lastname','age','password','email')

class gameform(forms.ModelForm):
    class Meta():
        model = kids_game
        fields = ('upload_game','upload_name')
class video_editform(forms.ModelForm):
    class Meta():
        model = kids_video
        fields = ('upload_videos','upload_name','categories')
class videocategoryform(forms.ModelForm):
    class Meta():
        model = video_category
        fields = ('category_name',)
class bookcategoryform(forms.ModelForm):
    class Meta():
        model = book_category
        fields = ('category_name',)
class video_editcategoryform(forms.ModelForm):
    class Meta():
        model = video_category
        fields = ('category_name',)
class book_editcategoryform(forms.ModelForm):
    class Meta():
        model = book_category
        fields = ('category_name',)




