# Computer Vision Pipeline

`backend/app/services/vision.py` defines the inspection contract and deterministic demonstration behavior. Production deployment should inject a versioned YOLOv8 model, retain image hashes and inference metadata, and write reviewed labels back to the quality dataset. Install the `vision` optional dependency group to enable OpenCV, Ultralytics, and PyTorch.
