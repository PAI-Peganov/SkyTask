#!/usr/bin/env python3
"""
Simple3DEditor
Author
    Peganov Artyom (Пеганов Артём) artyompeganov428@gmail.com
Starting App
    For start App run simple_3d_editor.py

Take Help
    py simple_3d_editor --help
Features
    "Save" button to save scene as pkl file
    "Load" button to load scene from pkl file
    In "Editing" tab you can choose an object and edit it in near field
    In "Adding" tab you can choose option to add new object to your scene
There are any primitive objects available like:
    Points, Segments, Planes, 2D and 3D Figures (by different ways)
When you want to create new Object, you need to give it a name and
    if for build Object(1) you need any other Object(2) you need
    previously add this Object(2) to scene by creating and
    write its name to Object(1) adding window.
Point:
    x, y, z
Segment:
    2 points
Plane (3 ways):
1) 3 points
2) point, segment
3) point, plane

And other

To add contur you need plane to add it to this plane to border it
Of course you can rotate and zoom scene by scroll bars
"""
import sys
import subprocess


def main():
    args = sys.argv[1:]

    if "--help" in args:
        print(__doc__)
        return

    subprocess.run(["python", "src/qt_app.py"])


if __name__ == "__main__":
    main()
