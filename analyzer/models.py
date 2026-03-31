from django.db import models

class ArtifactTask(models.Model):
    ruined_image = models.ImageField(upload_to='artifacts/ruined/', null=True, blank=True)
    reference_image = models.ImageField(upload_to='artifacts/reference/', null=True, blank=True)
    ruined_percentage = models.FloatField(null=True, blank=True)
    
    # Professional 500-Word Maintenance Manuals
    repair_instructions = models.TextField(null=True, blank=True)
    
    # Workflow status
    # SCANNED, SENT_TO_WORKER, REPAIRED, VALIDATED
    status = models.CharField(max_length=50, default='INITIALIZING')
    
    # Worker uploads repaired image
    repaired_image = models.ImageField(upload_to='artifacts/repaired/', null=True, blank=True)
    
    # Engineer validation
    validation_score = models.FloatField(null=True, blank=True)
    
    # Generated architectural / repair blueprint image
    blueprint_image = models.ImageField(upload_to='artifacts/blueprints/', null=True, blank=True)
    
    # TripoSR 3D Mesh
    mesh_obj = models.FileField(upload_to='artifacts/3d/', null=True, blank=True)
    mesh_glb = models.FileField(upload_to='artifacts/3d/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
