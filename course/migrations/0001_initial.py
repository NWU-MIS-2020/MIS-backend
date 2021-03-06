# Generated by Django 3.0.4 on 2020-04-24 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plan', '__first__'),
        ('user', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='评价依据内容')),
                ('full_marks', models.FloatField(verbose_name='满分值')),
            ],
            options={
                'verbose_name': '历史评价依据',
                'verbose_name_plural': '历史评价依据',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='开课日期')),
                ('end_date', models.DateField(verbose_name='结课日期')),
                ('short_description', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='简介')),
                ('review_status', models.CharField(choices=[('未通过', '未通过'), ('未审核', '未审核'), ('已审核', '已审核')], default='未审核', max_length=10, verbose_name='审核状态')),
                ('review_comment', models.TextField(blank=True, default='', null=True, verbose_name='审核人评论')),
                ('cms', models.ManyToManyField(related_name='courses', to='user.CM', verbose_name='课程负责人')),
                ('offering_course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='plan.OfferingCourse', verbose_name='开设课程')),
            ],
            options={
                'verbose_name': '历史课程',
                'verbose_name_plural': '历史课程',
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_marks', models.FloatField(blank=True, null=True, verbose_name='结课分数')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='courses', to='course.Course', verbose_name='课程')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='user.Student', verbose_name='学生')),
            ],
            options={
                'verbose_name': '成绩和评价',
                'verbose_name_plural': '成绩和评价',
            },
        ),
        migrations.CreateModel(
            name='IndicatorMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_marks', models.FloatField(blank=True, default=None, null=True, verbose_name='加权平均评价分数')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indicator_marks', to='course.Grade', verbose_name='成绩和评价')),
                ('indicator_factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indicator_marks', to='plan.IndicatorFactor', verbose_name='支撑课程以及指标系数')),
            ],
            options={
                'verbose_name': '学生课程对应指标点评价值',
                'verbose_name_plural': '学生课程对应指标点评价值',
            },
        ),
        migrations.CreateModel(
            name='DetailedMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.FloatField(blank=True, default=None, null=True, verbose_name='实际分数')),
                ('basis', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='course.Basis', verbose_name='历史评级依据')),
                ('indicator_mark', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detailed_marks', to='course.IndicatorMark', verbose_name='课程在指标点中总体评价')),
            ],
            options={
                'verbose_name': '学生课程对应指标点评价值细分',
                'verbose_name_plural': '学生课程对应指标点评价值细分',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='courses', through='course.Grade', to='user.Student', verbose_name='学生'),
        ),
        migrations.AddField(
            model_name='course',
            name='teachers',
            field=models.ManyToManyField(related_name='courses', to='user.Teacher', verbose_name='负责教师'),
        ),
        migrations.AddField(
            model_name='basis',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bases', to='course.Course', verbose_name='历史课程'),
        ),
        migrations.AddField(
            model_name='basis',
            name='indicator_factor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='plan.IndicatorFactor', verbose_name='支撑课程以及指标系数'),
        ),
        migrations.AddConstraint(
            model_name='indicatormark',
            constraint=models.UniqueConstraint(fields=('indicator_factor', 'grade'), name='unique_indicator_mark'),
        ),
        migrations.AlterUniqueTogether(
            name='indicatormark',
            unique_together={('indicator_factor', 'grade')},
        ),
        migrations.AddConstraint(
            model_name='grade',
            constraint=models.UniqueConstraint(fields=('course', 'student'), name='unique_grade'),
        ),
        migrations.AlterUniqueTogether(
            name='grade',
            unique_together={('course', 'student')},
        ),
    ]
