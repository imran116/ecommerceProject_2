# Generated by Django 5.0.2 on 2024-02-26 17:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_image', models.ImageField(upload_to='products/')),
                ('name', models.CharField(max_length=264)),
                ('preview_text', models.TextField(max_length=200, verbose_name='Preview Text')),
                ('detail_text', models.TextField(max_length=1000, verbose_name='Description')),
                ('price', models.FloatField()),
                ('old_price', models.FloatField(default=0.0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='shop_app.category')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]