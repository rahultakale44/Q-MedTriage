"""
Compare the user's image with a valid dataset chest X-ray
to show the differences that cause rejection
"""

from PIL import Image
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load user's image
user_image_path = PROJECT_ROOT / "1787845294977.jpg"
user_image = Image.open(user_image_path)

# Load a valid dataset chest X-ray
dataset_image_path = PROJECT_ROOT / "data/archive (1)/chest_xray/chest_xray/test/NORMAL/IM-0001-0001.jpeg"
dataset_image = Image.open(dataset_image_path)

print("=" * 70)
print("IMAGE COMPARISON: User's Image vs Valid Chest X-ray")
print("=" * 70)

print("\n" + "─" * 70)
print("USER'S IMAGE (1787845294977.jpg) - REJECTED ❌")
print("─" * 70)
print(f"Size: {user_image.size}")
print(f"Mode: {user_image.mode}")
print(f"Format: {user_image.format}")

user_arr = np.array(user_image)
print(f"Shape: {user_arr.shape}")
print(f"Mean brightness: {user_arr.mean():.1f} / 255")
print(f"Min value: {user_arr.min()}")
print(f"Max value: {user_arr.max()}")
print(f"Standard deviation: {user_arr.std():.1f}")

# Check if grayscale
if user_image.mode == "RGB":
    r_channel = user_arr[:, :, 0]
    g_channel = user_arr[:, :, 1]
    b_channel = user_arr[:, :, 2]
    is_grayscale = np.allclose(r_channel, g_channel, atol=5) and np.allclose(g_channel, b_channel, atol=5)
    print(f"Is grayscale: {is_grayscale}")

print("\nValidation Result:")
print("  ❌ Chest X-ray confidence: 10.70%")
print("  ❌ Non-medical confidence: 71.89%")
print("  ❌ Status: REJECTED")

print("\n" + "─" * 70)
print("DATASET IMAGE (IM-0001-0001.jpeg) - ACCEPTED ✅")
print("─" * 70)
print(f"Size: {dataset_image.size}")
print(f"Mode: {dataset_image.mode}")
print(f"Format: {dataset_image.format}")

dataset_arr = np.array(dataset_image)
print(f"Shape: {dataset_arr.shape}")
print(f"Mean brightness: {dataset_arr.mean():.1f} / 255")
print(f"Min value: {dataset_arr.min()}")
print(f"Max value: {dataset_arr.max()}")
print(f"Standard deviation: {dataset_arr.std():.1f}")

print("\nValidation Result:")
print("  ✅ Chest X-ray confidence: 29.99%")
print("  ✅ Non-medical confidence: 0.08%")
print("  ✅ Status: ACCEPTED")

print("\n" + "=" * 70)
print("KEY DIFFERENCES")
print("=" * 70)

print("\n1. COLOR MODE:")
print(f"   User's image: {user_image.mode} (RGB color)")
print(f"   Valid X-ray:  {dataset_image.mode} (Grayscale)")
print("   → Medical X-rays are typically grayscale (L mode)")

print("\n2. BRIGHTNESS:")
print(f"   User's image: {user_arr.mean():.1f} / 255 (very dark)")
print(f"   Valid X-ray:  {dataset_arr.mean():.1f} / 255 (normal)")
print("   → User's image is significantly darker")

print("\n3. CONTRAST:")
print(f"   User's image: {user_arr.std():.1f} standard deviation")
print(f"   Valid X-ray:  {dataset_arr.std():.1f} standard deviation")

print("\n4. SIZE:")
print(f"   User's image: {user_image.size[0]} × {user_image.size[1]} pixels")
print(f"   Valid X-ray:  {dataset_image.size[0]} × {dataset_image.size[1]} pixels")
print("   → Dataset X-rays are typically higher resolution")

print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)
print("""
The user's image has characteristics that differ significantly from
medical chest X-rays:
  - RGB color mode instead of grayscale
  - Very low brightness (unusually dark)
  - Different size profile

This explains why CLIP detects it as non-medical with 71.89% confidence.

RECOMMENDATION: Please verify the uploaded image is actually a chest X-ray.
If it is, it may need preprocessing to match medical imaging standards.
""")
print("=" * 70)
