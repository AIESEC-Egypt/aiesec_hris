# Generated by Django 2.0.1 on 2018-01-10 21:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('university', models.CharField(max_length=128)),
                ('faculty', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=128)),
                ('date_of_birth', models.DateField()),
                ('interested_ixp', models.CharField(max_length=128)),
                ('ixp', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Timeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_contacted', models.BooleanField(default=False)),
                ('date_contacted', models.DateTimeField(default=False)),
                ('status_onhold', models.BooleanField(default=False)),
                ('date_onhold', models.DateTimeField(default=False)),
                ('status_accepted', models.BooleanField(default=False)),
                ('date_accepted', models.DateTimeField(default=False)),
                ('status_rejected', models.BooleanField(default=False)),
                ('date_rejected', models.DateTimeField(default=False)),
                ('status_inducted', models.BooleanField(default=False)),
                ('date_inducted', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='applicant',
            name='timeline',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='recruitment.Timeline'),
        ),
    ]
