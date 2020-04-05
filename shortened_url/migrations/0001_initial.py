# Generated by Django 2.2.12 on 2020-04-03 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShortenedURL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subpart', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Subpart')),
                ('long_url', models.URLField(verbose_name='Long URL')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Shortened URL',
                'verbose_name_plural': 'Shortened URLs',
                'ordering': ['-created_at'],
            },
        ),
    ]