# Generated by Django 5.0 on 2024-01-21 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_grade'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grade',
            old_name='boolean',
            new_name='grade',
        ),
    ]
