import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from analyzer.models import ArtifactTask
tasks = ArtifactTask.objects.all().order_by('id')
print(f"Total Tasks: {tasks.count()}")
for t in tasks:
    print(f"Task {t.id}: Manual={'YES' if t.repair_instructions else 'NO'}, Status={t.status}")
