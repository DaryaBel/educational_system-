# Generated by Django 3.2 on 2022-03-26 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_remove_organization_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='kind',
            field=models.CharField(choices=[('UNIVERSITY', 'Высшее учебное заведение'), ('COMPANY', 'Компания')], default='UNIVERSITY', max_length=12, verbose_name='Вид организации'),
            preserve_default=False,
        ),
    ]
