# Generated by Django 4.2.2 on 2023-07-03 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_data_height1_alter_data_height2'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='final_image',
            field=models.ImageField(default=0, upload_to=''),
            preserve_default=False,
        ),
    ]
