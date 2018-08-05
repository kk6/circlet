# Generated by Django 2.0.7 on 2018-07-28 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("users", "0006_auto_20180728_1059")]

    operations = [
        migrations.AlterField(
            model_name="friendship",
            name="twitter_account",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.TwitterAccount"
            ),
        ),
        migrations.AlterField(
            model_name="friendship",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
