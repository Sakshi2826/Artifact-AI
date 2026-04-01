import os
import torch
import numpy as np
import rembg
from PIL import Image

# ✅ FIXED IMPORTS (RELATIVE - WORKS ON RENDER)
from .triposr_lib.tsr.system import TSR
from .triposr_lib.tsr.utils import remove_background, resize_foreground


class TripoService:
    _model = None
    _rembg_session = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            print("--- [TripoSR] Initializing Model (FORCE CPU MODE) ---", flush=True)

            cls._model = TSR.from_pretrained(
                "stabilityai/TripoSR",
                config_name="config.yaml",
                weight_name="model.ckpt",
            )

            cls._model.to("cpu")

            # Prevent memory issues on Render
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

        # 1. Background removal
        image = Image.open(input_image_path).convert("RGBA")
        image = remove_background(image, session)
        image = resize_foreground(image, 0.85)

        # Convert to numpy
        img_np = np.array(image).astype(np.float32) / 255.0

        if img_np.shape[2] == 4:
            img_np = img_np[:, :, :3] * img_np[:, :, 3:4] + (1 - img_np[:, :, 3:4]) * 0.5

        processed_image = Image.fromarray((img_np * 255.0).astype(np.uint8))

        # 2. Run model
        print("--- [TripoSR] Running Inference (CPU: ~1-2 min) ---", flush=True)

        with torch.no_grad():
            scene_codes = model([processed_image], device="cpu")

        # 3. Extract mesh
        print("--- [TripoSR] Extracting Mesh ---", flush=True)

        meshes = model.extract_mesh(
            scene_codes,
            has_vertex_color=False,
            resolution=160  # safer for low memory
        )

        # 4. Export files
        obj_file = output_base_path + ".obj"
        glb_file = output_base_path + ".glb"

        print(f"--- [TripoSR] Exporting to {obj_file} and {glb_file} ---", flush=True)

        meshes[0].export(obj_file)
        meshes[0].export(glb_file)

        return obj_file, glb_file