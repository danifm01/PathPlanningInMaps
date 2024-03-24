import bpy
import subprocess

logs = []
for scn in bpy.data.scenes:
    if scn.name == 'Base':
        continue 
    command = f'blender -b "{bpy.data.filepath}" -S "{scn.name}" -a'
    print(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logs.append(p)
    print(f'-------->>>>>>>>Rendering: {scn.name}<<<<<<<<<<---------')
