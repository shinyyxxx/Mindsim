from django.db import migrations
import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PlaceIndex",
            fields=[
                ("id", migrations.fields.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("oid", migrations.fields.CharField(max_length=64, unique=True)),
                ("name", migrations.fields.CharField(max_length=255)),
                ("location", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ("created_at", migrations.fields.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]


