bl_info = {
    "name": "Blengen",
    "author": "Pandartb3d",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Generate",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}

import bpy
from random import uniform
from random import random



class MyVoxel(bpy.types.Operator):
    """This is my simple operator"""
    bl_idname = "scene.myvoxel"
    bl_label = "Voxel"
    
    def execute(self, context):
        
        bpy.ops.transform.translate(value=(20, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(-20, -0, -0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

        
        bpy.context.object.data.remesh_voxel_size = 0.2
        bpy.ops.object.voxel_remesh()
        bpy.ops.sculpt.sculptmode_toggle()

  
        
        return {"FINISHED"}


class MyOperator(bpy.types.Operator):
    """This is my simple operator"""
    bl_idname = "scene.myoperator"
    bl_label = "Delete All & New Gen"
    
    def execute(self, context):
        context = bpy.context
        scene = context.scene
        #Delete Scene
        for c in scene.collection.children:
            scene.collection.children.unlink(c)
            #Collection and Mirror Axis

        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="model")

        mat_list = []
        number = 0

        for x in range(0, 3):
            
            for y in range(-2, 3):   
                
                for z in range(-2,3):
                    
                    if random() >= 0.8:
                        
                        if random() >=0.5:
                            bpy.ops.mesh.primitive_cube_add(enter_editmode=False, location=(0, 0, 0))
                            
                        else:
                            bpy.ops.mesh.primitive_uv_sphere_add(segments=15, ring_count=15, radius=1, enter_editmode=False, location=(0, 0, 0))       
                        mat = bpy.data.materials.new("test")
                        mat.use_nodes = True
                        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (random(), random(), random(), 1)
                        ob = bpy.context.active_object
                        ob.data.materials.append(mat)
                        mat_list.append(mat)
                        
                        

                        bpy.ops.transform.translate(value=(x, y, z), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

                        bpy.ops.transform.resize(value=(uniform(0.5,5), uniform(0.5,5), uniform(0.5,5)), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

                        bpy.ops.transform.rotate(value=uniform(3.14,-3.14), orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.ops.transform.rotate(value=uniform(3.14,-3.14), orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                        bpy.ops.transform.rotate(value=uniform(3.14,-3.14), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

                        number += 1


        ob = bpy.context.active_object

        for i in range(0,number):
            

            ob.data.materials.append(mat)
            ob.data.materials[i] = mat_list[i]
            

        bpy.ops.object.mode_set(mode = 'OBJECT')  
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.make_single_user(object=True, obdata=True)
        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.booltool_auto_union()
        bpy.ops.object.transform_apply(location = True, scale = True, rotation = True)

        #bpy.ops.object.material_slot_remove_unused()

        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.context.object.modifiers["Mirror"].mirror_object = bpy.data.objects["Empty"]
        bpy.context.object.modifiers["Mirror"].use_axis[0] = True
        bpy.context.object.modifiers["Mirror"].use_axis[1] = False
        bpy.context.object.modifiers["Mirror"].use_axis[2] = False

        bpy.context.object.modifiers["Mirror"].use_bisect_axis[0] = True
            
        bpy.context.object.modifiers["Mirror"].merge_threshold = 0.25

        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")

        bpy.context.object.data.use_auto_smooth = True
        bpy.ops.object.shade_smooth()



        bpy.ops.object.move_to_collection(collection_index=1)

        my_areas = bpy.context.workspace.screens[0].areas
        my_shading = 'MATERIAL'
        
        for area in my_areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = my_shading
        
        
        return {"FINISHED"}








class panel(bpy.types.Panel):
    bl_idname = "panel.panel3"
    bl_label = "Blengen"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blengen"
 
    def draw(self, context):
        
        
        layout = self.layout
        obj = context.object
        row = layout.row()
        row.label(text="IMPORTANT:")
        row = layout.row()
        row.label(text="ENABLE 'BOOL TOOL' ADDON")
        
        
        
        row = layout.row()
        row.label(text="Quick Gen")
        
        row = layout.row()
        row.operator("scene.myoperator", icon='CURSOR')
        row = layout.row()
        
        row = layout.row()
        row.label(text="Quick Voxel (only Blender 2.81)")
        
        row = layout.row()
        row.operator("scene.myvoxel", icon='MOD_REMESH')
        
 
 
def register() :
    bpy.utils.register_class(panel) 
    bpy.utils.register_class(MyOperator)
    bpy.utils.register_class(MyVoxel)

 
def unregister() :
    bpy.utils.unregister_class(panel)  
    bpy.utils.unregister_class(MyOperator)
    bpy.utils.register_class(MyVoxel)
 
if __name__ == "__main__" :
    register()
