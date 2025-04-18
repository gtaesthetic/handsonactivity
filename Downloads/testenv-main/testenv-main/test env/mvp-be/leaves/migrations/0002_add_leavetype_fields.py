from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('leaves', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavetype',
            name='max_days_allowed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='leavetype',
            name='requires_documentation',
            field=models.BooleanField(default=False),
        ),
    ] 