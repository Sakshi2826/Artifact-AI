import os
import sys
import torch
import numpy as np
import rembg
from PIL import Image

# Add triposr_lib to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRIPOSR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'triposr_lib')
if TRIPOSR_PATH not in sys.path:
    sys.path.append(TRIPOSR_PATH)

try:
    from tsr.system import TSR
    from tsr.utils import remove_background, resize_foreground
except ImportError:
    print(f"Error importing TripoSR from {TRIPOSR_PATH}. Path exists: {os.path.exists(TRIPOSR_PATH)}")
    # If standard import fails, try to inject the path more aggressively
    sys.path.insert(0, TRIPOSR_PATH)
    from tsr.system import TSR
    from tsr.utils import remove_background, resize_foreground

class TripoService:
    _model = None
    _rembg_session = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            print("--- [TripoSR] Initializing Model (FORCE CPU MODE) ---", flush=True)
            # Use huggingface_hub to download if needed, but TSR.from_pretrained handles this
            cls._model = TSR.from_pretrained(
                "stabilityai/TripoSR",
                config_name="config.yaml",
                weight_name="model.ckpt",
            )
            cls._model.to("cpu")
            # Set chunk size to avoid OOM on large grids
            if hasattr(cls._model, 'renderer'):
                cls._model.renderer.set_chunk_size(131072)
            print("--- [TripoSR] Model Loaded Successfully ---", flush=True)
        return cls._model

    @classmethod
    def get_rembg(cls):
        if cls._rembg_session is None:
            print("--- [TripoSR] Initializing RemBG Session ---", flush=True)
            cls._rembg_session = rembg.new_session()
        return cls._rembg_session

    @classmethod
    def generate_3d(cls, input_image_path, output_base_path):
        """
        Converts image to 3D mesh (OBJ and GLB) using TripoSR on CPU.
        """
        model = cls.get_model()
        session = cls.get_rembg()

        print(f"--- [TripoSR] Processing Image: {input_image_path} ---", flush=True)
        # 1. Background removal and preprocessing
        image = Image.open(input_image_path)
        image = remove_background(image, session)
        image = resize_foreground(image, 0.85)
        
        # Convert to numpy and handle transparency for model input
        img_np = np.array(image).astype(np.float32) / 255.0
        if img_np.shape[2] == 4:
            img_np = img_np[:, :, :3] * img_np[:, :, 3:4] + (1 - img_np[:, :, 3:4]) * 0.5
        
        processed_image = Image.fromarray((img_np * 255.0).astype(np.uint8))

        # 2. Run TripoSR Model
        print("--- [TripoSR] Running Inference (Expect ~1-2 min on CPU) ---", flush=True)
        with torch.no_grad():
            scene_codes = model([processed_image], device="cpu")
        
        # 3. Extract Mesh
        print("--- [TripoSR] Extracting Mesh (Marching Cubes) ---", flush=True)
        # resolution=160 is better for CPU speed/stability, 256 was slightly OOM-prone
        meshes = model.extract_mesh(scene_codes, has_vertex_color=False, resolution=160)
        
        # 4. Export to files
        obj_file = output_base_path + ".obj"
        glb_file = output_base_path + ".glb"
        
        print(f"--- [TripoSR] Exporting to {obj_file} and {glb_file} ---", flush=True)
        meshes[0].export(obj_file)
        meshes[0].export(glb_file)
        
        return obj_file, glb_file
