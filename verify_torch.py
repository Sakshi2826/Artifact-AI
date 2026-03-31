import torch

def verify_torch():
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA version: {torch.version.cuda}")
        print(f"GPU Name: {torch.cuda.get_device_name(0)}")
        print(f"Memory allocated: {torch.cuda.memory_allocated(0) / 1024**2:.2f} MB")
    else:
        print("CUDA is not available.")

if __name__ == "__main__":
    try:
        verify_torch()
    except Exception as e:
        print(f"Error during verification: {e}")
