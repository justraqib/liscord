# Generated by Django 4.1 on 2022-08-30 17:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app', '0004_channel_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServerMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='server',
            name='created_by',
        ),
        migrations.AddField(
            model_name='server',
            name='members',
            field=models.ManyToManyField(related_name='servers_joined', through='app.ServerMembers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='servermembers',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.server'),
        ),
        migrations.AddField(
            model_name='servermembers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='servermembers',
            unique_together={('server', 'user')},
        ),
    ]
