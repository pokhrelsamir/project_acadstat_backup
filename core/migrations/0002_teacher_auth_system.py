# Generated migration for teacher authentication system

from django.db import migrations, models
import django.db.models.deletion


def create_users_for_teachers(apps, schema_editor):
    """Create User accounts for existing Teacher records"""
    Teacher = apps.get_model('core', 'Teacher')
    User = apps.get_model('auth', 'User')
    
    for teacher in Teacher.objects.all():
        username = f"{teacher.first_name.lower()}.{teacher.last_name.lower()}"
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=teacher.email if getattr(teacher, 'email', None) else f"{username}@example.com",
            password='temp123',
            first_name=teacher.first_name,
            last_name=teacher.last_name
        )
        teacher.user = user
        teacher.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        # Step 1: Add user field as nullable initially
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='teacher_profile',
                to='auth.user',
                blank=True
            ),
        ),

        # Step 2: Create users for existing teachers
        migrations.RunPython(create_users_for_teachers, migrations.RunPython.noop),

        # Step 3: Make user field required (NOT NULL)
        migrations.AlterField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='teacher_profile',
                to='auth.user'
            ),
        ),

        # Step 4: Add is_active field
        migrations.AddField(
            model_name='teacher',
            name='is_active',
            field=models.BooleanField(default=True),
        ),

        # Step 5: Add subjects ManyToManyField
        migrations.AddField(
            model_name='teacher',
            name='subjects',
            field=models.ManyToManyField(
                blank=True,
                related_name='teachers',
                to='core.Subject'
            ),
        ),

        # Step 6: Remove old single subject field (if it exists)
        migrations.RemoveField(
            model_name='teacher',
            name='subject',
        ),

        # Step 7: Add teachers ManyToManyField to Student
        migrations.AddField(
            model_name='student',
            name='teachers',
            field=models.ManyToManyField(
                blank=True,
                related_name='students',
                to='core.Teacher'
            ),
        ),

        # Step 8: Remove old single teacher field (if it exists)
        migrations.RemoveField(
            model_name='student',
            name='teacher',
        ),

        # Step 9: Create CourseMaterial model
        migrations.CreateModel(
            name='CourseMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='course_materials/')),
                ('file_url', models.URLField(blank=True, help_text='External link to material', null=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='core.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_materials', to='core.teacher')),
            ],
            options={
                'ordering': ['-upload_date'],
            },
        ),
    ]
