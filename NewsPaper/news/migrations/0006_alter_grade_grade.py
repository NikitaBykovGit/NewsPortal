# Generated by Django 5.0 on 2024-01-22 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_grade_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='grade',
            field=models.CharField(choices=[('Like', 1), ('Dislike', -1)], default='Like', max_length=7),
        ),
    ]
