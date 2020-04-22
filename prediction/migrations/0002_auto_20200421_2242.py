# Generated by Django 3.0.4 on 2020-04-21 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20200421_2242'),
        ('user', '0001_initial'),
        ('prediction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='cm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='user.CM', verbose_name='审核人'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='course.Course', verbose_name='课程'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='final_marks',
            field=models.FloatField(blank=True, null=True, verbose_name='结课分数'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='indicator',
            field=models.FloatField(blank=True, null=True, verbose_name='评价分数'),
        ),
    ]
