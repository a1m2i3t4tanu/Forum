# Generated by Django 2.1.5 on 2019-09-27 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Email', models.EmailField(max_length=200)),
                ('Body', models.TextField()),
                ('Created', models.DateTimeField(auto_now_add=True)),
                ('Active', models.BooleanField(default=True)),
                ('Parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='forum.Comment')),
            ],
            options={
                'ordering': ('-Created',),
            },
        ),
        migrations.AddField(
            model_name='post',
            name='p_file',
            field=models.FileField(blank=True, null=True, upload_to='file_pics'),
        ),
        migrations.AddField(
            model_name='post',
            name='p_image',
            field=models.ImageField(blank=True, null=True, upload_to='quest_pics'),
        ),
        migrations.AddField(
            model_name='comment',
            name='Post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='forum.Post'),
        ),
    ]
