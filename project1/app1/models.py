from django.db import models

# Create your models here.

class parent(models.Model):
    reg_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=100,default='1234')
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    user_type = models.IntegerField(default=2)
    status = models.BooleanField(default=False)

class child(models.Model):
    child_id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey('parent', on_delete=models.CASCADE, to_field='reg_id')
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    password = models.CharField(max_length=100,default='1234')
    age=models.IntegerField()
    email = models.EmailField(max_length=100)
    user_type = models.IntegerField(default=3)
    status = models.BooleanField(default=False)

class kids_video(models.Model):
    video_id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey('parent', on_delete=models.CASCADE, to_field='reg_id')
    categories = models.ForeignKey('video_category', on_delete=models.CASCADE, to_field='video_category_id')
    upload_videos = models.FileField(upload_to='video/',null= True,blank=True)
    upload_name = models.CharField(max_length=100)
    Date_time = models.DateTimeField(auto_now=True)
    Status = models.BooleanField(default=False)
class books(models.Model):
    books_id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey('parent', on_delete=models.CASCADE, to_field='reg_id')
    categories = models.ForeignKey('book_category', on_delete=models.CASCADE, to_field='book_category_id')
    upload_book = models.FileField(upload_to='book/',null= True,blank=True)
    book_image = models.FileField(upload_to='img/', null=True, blank=True)
    upload_name = models.CharField(max_length=100)
    Date_time = models.DateTimeField(auto_now=True)

class kids_game(models.Model):
    game_id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey('parent', on_delete=models.CASCADE, to_field='reg_id')
    upload_game = models.FileField(upload_to='img/', null=True, blank=True)
    upload_name = models.CharField(max_length=100)
    Date_time = models.DateTimeField(auto_now=True)
class Video(models.Model):
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/')
    view_count = models.PositiveIntegerField(default=0)

class video_category(models.Model):
    video_category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name
class book_category(models.Model):
    book_category_id=models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name