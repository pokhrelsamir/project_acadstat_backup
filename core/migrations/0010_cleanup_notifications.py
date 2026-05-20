# Generated manually
from django.db import migrations
from django.db.models import Q

def cleanup_notifications(apps, schema_editor):
    """Delete notifications for deleted/soft-deleted materials"""
    Notification = apps.get_model('core', 'Notification')
    CourseMaterial = apps.get_model('core', 'CourseMaterial')
    
    # Delete notifications for materials that are soft-deleted (is_active=False)
    # These are notifications that have a material FK but material is inactive
    inactive_count = Notification.objects.filter(material__is_active=False).count()
    Notification.objects.filter(material__is_active=False).delete()
    print(f"Deleted {inactive_count} notifications for soft-deleted materials")
    
    # Delete orphaned notifications: material=null but title indicates they were for materials
    # (created before material FK existed)
    orphaned_count = Notification.objects.filter(
        material__isnull=True,
        title__startswith='New Material:'
    ).count()
    Notification.objects.filter(
        material__isnull=True,
        title__startswith='New Material:'
    ).delete()
    print(f"Deleted {orphaned_count} orphaned notifications (no FK)")

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0009_notification_material'),
    ]

    operations = [
        migrations.RunPython(cleanup_notifications),
    ]
