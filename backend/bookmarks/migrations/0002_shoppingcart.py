# Generated by Django 2.2.16 on 2023-03-18 10:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0008_auto_20230315_0930'),
        ('bookmarks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_cart', to='recipes.Recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
