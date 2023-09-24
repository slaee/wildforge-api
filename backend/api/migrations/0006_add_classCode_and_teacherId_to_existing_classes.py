from django.db import migrations, models
import random
import string

def assign_teacher_and_generate_class_code(apps, schema_editor):
    Class = apps.get_model('wildforge_api', 'Class')
    User = apps.get_model('wildforge_api', 'User')

    for class_instance in Class.objects.filter(teacherId=None):
        teacher = User.objects.order_by('?').first() # Get a random teacher
        
        # Generate a random alphanumeric class_code
        class_code_length = 8
        characters = string.ascii_letters + string.digits
        class_code = ''.join(random.choice(characters) for _ in range(class_code_length))

        class_instance.teacherId = teacher
        class_instance.class_code = class_code
        class_instance.save()

class Migration(migrations.Migration):

    dependencies = [
        ('wildforge_api', '0005_remove_user_role_user_is_staff_user_is_superuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='teacherId',
            field=models.ForeignKey(to='wildforge_api.User', on_delete=models.CASCADE, null=True),
        ),
        migrations.AddField(
            model_name='class',
            name='class_code',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.RunPython(assign_teacher_and_generate_class_code),
    ]
