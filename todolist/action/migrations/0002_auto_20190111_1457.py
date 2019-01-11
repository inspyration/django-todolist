# Generated by Django 2.1.5 on 2019-01-11 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='dependency_set',
            field=models.ManyToManyField(blank=True, related_name='_action_dependency_set_+', to='action.Action', verbose_name='dependencies'),
        ),
        migrations.AlterField(
            model_name='action',
            name='priority',
            field=models.CharField(choices=[('⇈', '⇈ Very high'), ('↑', '↑ High'), ('⇅', '⇅ Regular'), ('↓', '↓ Low'), ('⇊', '⇊ Very low')], db_index=True, default='⇅', max_length=1, verbose_name='priority'),
        ),
    ]