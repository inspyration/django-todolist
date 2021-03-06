# Generated by Django 2.1.5 on 2019-01-11 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.CharField(choices=[('⇈', '⇈ Very high'), ('↑', '↑ High'), ('⇅', '⇅ Regular'), ('↓', '↓ Low'), ('⇊', '⇊ Very low')], db_index=True, default='3', max_length=1, verbose_name='priority')),
                ('status', models.CharField(choices=[('A', 'Fuzzy'), ('B', 'Draft'), ('C', 'Planned'), ('D', 'In progress'), ('E', 'Archived'), ('V', 'Dropped (Archived)'), ('W', 'Dropped (In progress)'), ('X', 'Dropped (Planned)'), ('Y', 'Dropped (Draft)'), ('Z', 'Dropped (Fuzzy)')], db_index=True, default='A', max_length=1, verbose_name='status')),
                ('deadline', models.DateField(blank=True, db_index=True, null=True, verbose_name='deadline')),
                ('label', models.CharField(db_index=True, max_length=48, verbose_name='label')),
                ('name', models.CharField(db_index=True, max_length=128, verbose_name='name')),
                ('description', models.TextField(db_index=True, verbose_name='description')),
                ('planned_on', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='planned on')),
                ('estimate', models.PositiveSmallIntegerField(db_index=True, verbose_name='estimate')),
                ('estimate_unit', models.CharField(blank=True, choices=[('w', 'week'), ('d', 'day'), ('h', 'hour'), ('m', 'minute')], db_index=True, max_length=1, verbose_name='estimate unit')),
                ('duration', models.PositiveSmallIntegerField(db_index=True, verbose_name='duration')),
                ('duration_unit', models.CharField(blank=True, choices=[('w', 'week'), ('d', 'day'), ('h', 'hour'), ('m', 'minute')], db_index=True, max_length=1, verbose_name='duration unit')),
                ('slug', models.SlugField(max_length=32, unique=True)),
            ],
            options={
                'verbose_name': 'action',
                'verbose_name_plural': 'actions',
                'ordering': ('-planned_on', '-deadline', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('action_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='action.Action')),
                ('location', models.CharField(blank=True, db_index=True, max_length=64, verbose_name='duration unit')),
                ('departure_time', models.TimeField(blank=True, db_index=True, verbose_name='time')),
                ('send_reminder', models.BooleanField(db_index=True, default=False, verbose_name='Do you want a reminder to be sent ?')),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('action.action',),
        ),
        migrations.CreateModel(
            name='RecurrentAction',
            fields=[
                ('action_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='action.Action')),
                ('frequency', models.CharField(choices=[('d', 'daily'), ('w', 'weekly'), ('m', 'monthly'), ('y', 'yearly')], db_index=True, max_length=1, verbose_name='frequency')),
                ('active', models.BooleanField(db_index=True, verbose_name='active')),
                ('until', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='until')),
                ('count', models.PositiveSmallIntegerField(verbose_name='count')),
            ],
            options={
                'verbose_name': 'recurrent action',
                'verbose_name_plural': 'recurrent actions',
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('action.action',),
        ),
        migrations.AddField(
            model_name='action',
            name='dependency_set',
            field=models.ManyToManyField(blank=True, null=True, related_name='_action_dependency_set_+', to='action.Action', verbose_name='dependencies'),
        ),
        migrations.AddField(
            model_name='action',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_action.action_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='action',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='action_set', to='project.Project', verbose_name='project'),
        ),
        migrations.AlterIndexTogether(
            name='action',
            index_together={('project', 'name'), ('project', 'label'), ('planned_on', 'deadline', 'name')},
        ),
    ]
