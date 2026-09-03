"""
Inspect the user's uploaded image to understand why it's being rejected
"""

from PIL import Image
from pathlib import Path

# Load the image
image_path = Path(__file__).resolve().parents[2] / "1787845294977.jpg"

if image_path.exists():
    image = Image.open(image_path)
    
    print("=" * 70)
    print("USER IMAGE ANALYSIS")
    print("=" * 70)
    print(f"Path: {image_path}")
    print(f"Size: {image.size}")
    print(f"Mode: {image.mode}")
    print(f"Format: {image.format}")
    
    # Get image info
    print(f"\nImage Info:")
    print(f"  Width: {image.width}px")
    print(f"  Height: {image.height}px")
    print(f"  Aspect Ratio: {image.width/image.height:.2f}")
    
    # Check if it's grayscale-like
    if image.mode == "RGB":
        # Sample pixels to check if it's actually grayscale
        import numpy as np
        arr = np.array(image)
        
        # Check if R=G=B (grayscale stored as RGB)
        r_channel = arr[:, :, 0]
        g_channel = arr[:, :, 1]
        b_channel = arr[:, :, 2]
        
        is_grayscale = np.allclose(r_channel, g_channel) and np.allclose(g_channel, b_channel)
        print(f"  Is Grayscale: {is_grayscale}")
        
        # Get some statistics
        print(f"  Mean brightness: {arr.mean():.1f}")
        print(f"  Min value: {arr.min()}")
        print(f"  Max value: {arr.max()}")
    
    print("\nImage successfully loaded. The validator reports:")
    print("  - Chest X-ray confidence: 10.70%")
    print("  - Unsupported: 71.89%")
    print("  - This suggests the image may not be a medical chest X-ray")
    
    # Save a thumbnail for reference
    thumbnail_path = image_path.parent / "user_image_thumbnail.jpg"
    thumbnail = image.copy()
    thumbnail.thumbnail((400, 400))
    thumbnail.save(thumbnail_path)
    print(f"\nThumbnail saved to: {thumbnail_path}")
    
else:
    print(f"Image not found at {image_path}")
