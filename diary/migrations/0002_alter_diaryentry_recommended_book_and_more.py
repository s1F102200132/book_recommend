# Generated by Django 4.2.16 on 2024-10-26 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('diary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diaryentry',
            name='recommended_book',
            field=models.CharField(default='Not Available', max_length=100),
        ),
        migrations.AlterField(
            model_name='diaryentry',
            name='sentiment',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='diaryentry',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
