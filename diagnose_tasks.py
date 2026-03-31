import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from analyzer.models import ArtifactTask
from analyzer.views import subtask_master_vision_v21_direct

def diagnose():
    tasks = ArtifactTask.objects.all().order_by('-created_at')
    print(f"Total Tasks: {tasks.count()}")
    
    missing_manuals = tasks.filter(repair_instructions__isnull=True) | tasks.filter(repair_instructions='')
    print(f"Tasks missing manuals: {missing_manuals.count()}")
    
    for task in missing_manuals:
        print(f"\n--- Diagnosing Task ID: {task.id} ---")
        print(f"Status: {task.status}")
        print(f"Ruined Image: {task.ruined_image.name if task.ruined_image else 'None'}")
        
        if task.ruined_image:
            print(f"Attempting manual generation for Task ID: {task.id}...")
            try:
                result = subtask_master_vision_v21_direct(task.id)
                if result:
                    print(f"RE-RUN SUCCESS for Task {task.id}")
                    # Double check if saved
                    task.refresh_from_db()
                    if task.repair_instructions:
                        print("Manual successfully generated and saved.")
                    else:
                        print("Result returned but repair_instructions field is still empty!")
                else:
                    print(f"RE-RUN FAILED for Task {task.id} (Empty result returned)")
            except Exception as e:
                print(f"EXCEPTION during re-run: {e}")
        else:
            print(f"Task {task.id} has no image, cannot generate manual.")

if __name__ == "__main__":
    diagnose()
