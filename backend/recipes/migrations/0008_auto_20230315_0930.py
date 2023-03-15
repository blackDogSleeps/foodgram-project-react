# Generated by Django 2.2.16 on 2023-03-15 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20230315_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.Recipe'),
        ),
    ]
