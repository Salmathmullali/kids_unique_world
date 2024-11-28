# Generated by Django 4.2.6 on 2023-10-10 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='reg',
            fields=[
                ('reg_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('email', models.EmailField(max_length=100)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/')),
                ('user_type', models.IntegerField(default=2)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='gallery',
            fields=[
                ('file_id', models.AutoField(primary_key=True, serialize=False)),
                ('img_name', models.CharField(max_length=100)),
                ('img', models.ImageField(blank=True, null=True, upload_to='image/')),
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.reg')),
            ],
        ),
    ]
