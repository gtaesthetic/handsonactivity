# filepath: c:\Users\Manuel\Documents\GitHub\mvp-be\leaves\migrations\0002_populate_leavetypes.py
from django.db import migrations

def populate_leave_types(apps, schema_editor):
    LeaveType = apps.get_model("leaves", "LeaveType")
    leave_types = [
        ("Annual Leave", "Annual leave entitlement", 20, False),
        ("Sick Leave", "Sick leave entitlement", 14, True),
        ("Hospitalisation Leave", "Medical leave for hospitalization", 60, True),
        ("NS Service Leave", "For National Service obligations", 14, False),
        ("Paternity Leave", "Leave for new fathers", 14, True),
        ("Maternity Leave", "Leave for new mothers", 90, True),
        ("Childcare Leave", "Leave for childcare responsibilities", 6, False),
        ("No Pay Leave", "Unpaid leave", 0, False),
        ("Study Leave", "For educational purposes", 10, False),
        ("Exam Leave", "For examination purposes", 5, False),
        ("Compassionate Leave", "For family emergencies", 7, False),
        ("Sabbatical Leave", "Extended leave", 180, False),
    ]
    for name, description, max_days, requires_doc in leave_types:
        LeaveType.objects.create(
            name=name,
            description=description,
            max_days_allowed=max_days,
            requires_documentation=requires_doc,
        )

class Migration(migrations.Migration):
    dependencies = [
        ("leaves", "0002_add_leavetype_fields"),
    ]

    operations = [
        migrations.RunPython(populate_leave_types),
    ]