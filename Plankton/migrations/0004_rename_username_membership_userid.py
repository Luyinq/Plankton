# Generated by Django 4.0.4 on 2022-07-07 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Plankton', '0003_alter_membership_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='username',
            new_name='userid',
        ),
    ]
