# Generated by Django 5.2.1 on 2025-05-30 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0005_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=200, null=True, unique=True),
        ),
    ]
