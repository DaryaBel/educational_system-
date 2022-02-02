# Generated by Django 3.2 on 2022-02-02 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logo', verbose_name='Логотип')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
            },
        ),
        migrations.CreateModel(
            name='Olympiad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('percent_to_win', models.PositiveIntegerField(verbose_name='Необходимое количество % для победы')),
                ('time_to_pass', models.DurationField(blank=True, null=True, verbose_name='Ограничение времени для решения')),
                ('date_result', models.DateField(blank=True, null=True, verbose_name='Дата оглашения результатов')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='Дата окончания приема ответов')),
                ('is_draft', models.BooleanField(default=False, verbose_name='Черновик')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companyOlympiad', to='olympiads.company', verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Олимпиада',
                'verbose_name_plural': 'Олимпиады',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.TextField(verbose_name='Текст задания')),
                ('max_score', models.PositiveIntegerField(verbose_name='Максимальное количество баллов')),
                ('order', models.IntegerField(default=0, unique=True, verbose_name='Номер задания')),
                ('olympiad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='olympiadTask', to='olympiads.olympiad', verbose_name='Олимпиада')),
            ],
            options={
                'verbose_name': 'Задание',
                'verbose_name_plural': 'Задания',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(blank=True, null=True, verbose_name='Балл')),
                ('certificate', models.FileField(blank=True, null=True, upload_to='certificates/', verbose_name='Сертификат')),
                ('is_draft', models.BooleanField(default=False, verbose_name='Черновик')),
                ('olympiad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='olympiadResult', to='olympiads.olympiad', verbose_name='Олимпиада')),
            ],
            options={
                'verbose_name': 'Результат',
                'verbose_name_plural': 'Результаты',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(verbose_name='Ответ на задание')),
                ('score', models.PositiveIntegerField(blank=True, null=True, verbose_name='Выставленное количество баллов')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taskAnswer', to='olympiads.task', verbose_name='Задание')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
    ]
