# Generated by Django 4.2.1 on 2023-05-31 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ChapterSotry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("chapter", models.IntegerField()),
                ("name", models.CharField(max_length=100)),
                ("content", models.TextField()),
                ("image", models.ImageField(upload_to="")),
            ],
            options={
                "db_table": "StoryChapter",
            },
        ),
        migrations.CreateModel(
            name="TypeStory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("typename", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="LongStory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("image", models.ImageField(upload_to="")),
                ("type", models.CharField(max_length=100)),
                (
                    "author_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.authorstory",
                    ),
                ),
            ],
            options={
                "db_table": "LongStory",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.authorstory",
                    ),
                ),
                (
                    "storyid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.chaptersotry",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="chaptersotry",
            name="story_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.longstory"
            ),
        ),
    ]
