# Generated by Django 4.2.6 on 2023-10-22 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_delete_reg'),
    ]

    operations = [
        migrations.CreateModel(
            name='child',
            fields=[
                ('reg_id', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('password', models.CharField(default='1234', max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('user_type', models.IntegerField(default=3)),
                ('status', models.BooleanField(default=False)),
                ('parent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.parent')),
            ],
        ),
    ]