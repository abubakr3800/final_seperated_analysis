import os
import json
import argparse
import pyvista as pv

# -------------------------------
# INTERACTIVE VIEWER
# -------------------------------
def show_fixtures(json_file):
    """Open interactive 3D scene with glowing fixtures"""
    if not os.path.exists(json_file):
        raise FileNotFoundError(f"JSON file not found: {json_file}")

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    plotter = pv.Plotter()
    plotter.show_grid()
    plotter.add_axes()

    for room in data.get("rooms", []):
        for p in room.get("layout", []):
            x, y, z = p["x_m"], p["y_m"], p["z_m"]
            sphere = pv.Sphere(radius=0.15, center=(x, y, z))
            plotter.add_mesh(sphere, color="yellow", opacity=1.0, emissive=True)

    print("✓ Viewer ready — use mouse to rotate/zoom")
    plotter.show()


# -------------------------------
# BLENDER EXPORT
# -------------------------------
def export_to_blender(json_file, out_file="scene_blender.py"):
    """Export fixtures to Blender Python script"""
    if not os.path.exists(json_file):
        raise FileNotFoundError(f"JSON file not found: {json_file}")

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines = [
        "import bpy",
        "from mathutils import Vector",
        "# Clear existing objects",
        "bpy.ops.object.select_all(action='SELECT')",
        "bpy.ops.object.delete(use_global=False)"
    ]

    for room in data.get("rooms", []):
        for p in room.get("layout", []):
            x, y, z = p["x_m"], p["y_m"], p["z_m"]
            lines.append(f"""
light_data = bpy.data.lights.new(name="Light", type='POINT')
light_data.energy = 1000  # Adjust lumens for brightness
light_obj = bpy.data.objects.new(name="Light", object_data=light_data)
light_obj.location = Vector(({x}, {y}, {z}))
bpy.context.collection.objects.link(light_obj)
""")

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✓ Blender export ready: run inside Blender with `blender --python {out_file}`")


# -------------------------------
# RADIANCE EXPORT
# -------------------------------
def export_to_radiance(json_file, out_file="scene.rad"):
    """Export fixtures to Radiance .rad file"""
    if not os.path.exists(json_file):
        raise FileNotFoundError(f"JSON file not found: {json_file}")

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines = []
    for room in data.get("rooms", []):
        for i, p in enumerate(room.get("layout", [])):
            x, y, z = p["x_m"], p["y_m"], p["z_m"]
            lines.append(f"""
void light fixture{i}
0
0
3 1000 1000 1000

fixture{i} sphere s{i}
0
0
4 {x} {y} {z} 0.15
""")

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✓ Radiance export saved: {out_file}")


# -------------------------------
# MAIN CLI
# -------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lighting Fixtures Visualizer & Exporter")
    parser.add_argument("json_file", help="Extracted JSON file from report")
    parser.add_argument("--viewer", action="store_true", help="Open interactive 3D viewer")
    parser.add_argument("--export", choices=["blender", "radiance"], help="Export format")

    args = parser.parse_args()

    if args.viewer:
        show_fixtures(args.json_file)
    elif args.export == "blender":
        export_to_blender(args.json_file)
    elif args.export == "radiance":
        export_to_radiance(args.json_file)
    else:
        print("No action selected. Use --viewer or --export blender|radiance")
