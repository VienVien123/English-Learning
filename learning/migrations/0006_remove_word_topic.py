# Generated by Django 5.1.7 on 2025-03-29 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("learning", "0005_alter_topic_options_remove_topic_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="word",
            name="topic",
        ),
    ]
