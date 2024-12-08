# Generated by Django 5.1.3 on 2024-11-23 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_rename_warnings_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='link',
            field=models.URLField(blank=True, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='importance',
            field=models.CharField(choices=[('Срочно', 'Срочно'), ('Внимание', 'Внимание'), ('Рассмотреть', 'Рассмотреть')], default='Внимание', max_length=150, verbose_name='Важность'),
        ),
    ]
