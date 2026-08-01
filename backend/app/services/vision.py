from app.schemas import InspectionCreate


def inspect_product(request: InspectionCreate) -> dict:
    """Demonstration inference contract; production deployments can inject a YOLO detector here."""
    has_demo_defect = request.product_code.lower().endswith("defect")
    return {
        "product_code": request.product_code,
        "image_url": request.image_url,
        "result": "fail" if has_demo_defect else "pass",
        "defect_type": "surface_scratch" if has_demo_defect else None,
        "confidence": 0.94 if has_demo_defect else 0.99,
        "bounding_boxes": (
            [{"x": 0.23, "y": 0.41, "width": 0.18, "height": 0.12}] if has_demo_defect else []
        ),
    }
