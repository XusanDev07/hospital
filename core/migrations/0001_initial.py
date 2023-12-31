# Generated by Django 4.2.4 on 2023-08-21 16:48

import core.models.auth
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDoctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=125, verbose_name='Ismi')),
                ('surname', models.CharField(max_length=125, verbose_name='Familyasi')),
                ('phone', models.CharField(max_length=125, unique=True, verbose_name='Telefon raqami')),
                ('img', models.ImageField(null=True, upload_to='docs', verbose_name='Rasm')),
                ('info', models.TextField(null=True, verbose_name="Shifokor haqida ma'lumot")),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='Elektron pochtasi')),
                ('gender', models.BooleanField(default=True, verbose_name='Jinsi')),
                ('user_type', models.SmallIntegerField(choices=[(1, 'Owner'), (2, 'Adminastirator'), (3, 'Doktor'), (4, 'Mijozlar')], default=4, verbose_name='Foydalanuvchi statusi')),
                ('new', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'Doktor',
                'verbose_name_plural': '1. Doktorlar',
            },
            managers=[
                ('objects', core.models.auth.CusManeger()),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=123)),
            ],
            options={
                'verbose_name': 'Lavozim',
                'verbose_name_plural': '6. Lavozimlar',
            },
        ),
        migrations.CreateModel(
            name='Professions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=123)),
            ],
            options={
                'verbose_name': 'Kasb',
                'verbose_name_plural': '5. Kasblar',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=123)),
                ('info', models.TextField()),
                ('icon', models.ImageField(upload_to='service')),
            ],
            options={
                'verbose_name': 'Servis',
                'verbose_name_plural': '2. Servislar',
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(default='50 000 UZS', max_length=123)),
                ('pr', models.IntegerField(blank=True, editable=False, null=True)),
                ('doc', models.ForeignKey(limit_choices_to={'user_type': 3}, on_delete=django.db.models.deletion.CASCADE, related_name='service_prices', to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.service')),
            ],
            options={
                'verbose_name': 'Narx',
                'verbose_name_plural': '3. Narxlar ',
            },
        ),
        migrations.CreateModel(
            name='DocTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('free', models.BooleanField(default=True)),
                ('doc', models.ForeignKey(limit_choices_to={'user_type': 3}, on_delete=django.db.models.deletion.CASCADE, related_name='doc_time', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Vaqt',
                'verbose_name_plural': '4. Vaqt sarrhisobi',
            },
        ),
        migrations.AddField(
            model_name='userdoctor',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='position', to='core.position'),
        ),
        migrations.AddField(
            model_name='userdoctor',
            name='prof',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profession', to='core.professions'),
        ),
        migrations.AddField(
            model_name='userdoctor',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
