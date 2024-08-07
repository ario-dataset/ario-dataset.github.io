import trimesh
import json
import numpy as np












file_path = "./base.glb"
with open(file_path, 'rb') as file_obj:
    mesh = trimesh.load(file_obj, file_type='glb')
# mesh = trimesh.load(file_path, file_type='glb')
oriented_bounding_box = mesh.bounding_box_oriented
scene = trimesh.Scene(mesh)

target_pose = [0, 0.815, 0.75]
target_sphere = trimesh.creation.icosphere(subdivisions=2, radius=0.15)
target_trans_matrix_sphere = trimesh.transformations.translation_matrix(target_pose)
target_sphere.apply_transform(target_trans_matrix_sphere)
red_color = [1.0, 0.0, 0.0, 0.5]  # 红色, A=1 表示不透明
target_sphere.visual.vertex_colors = np.array([red_color] * len(target_sphere.vertices))
target_trans_list = target_trans_matrix_sphere.tolist()


contact_pose = [0, 0, -0.25]
contact_sphere = trimesh.creation.icosphere(subdivisions=2, radius=0.15)
contact_trans_matrix_sphere = trimesh.transformations.translation_matrix(contact_pose)
contact_sphere.apply_transform(contact_trans_matrix_sphere)
red_color = [1.0, 0.0, 0.0, 0.5]  # 红色, A=1 表示不透明
contact_sphere.visual.vertex_colors = np.array([red_color] * len(contact_sphere.vertices))




# axis1
axis1 = trimesh.creation.axis(axis_length=1.5)
trans_matrix = trimesh.transformations.euler_matrix(-1.57, 0,1.57)
# trans_matrix1[0,3] = 1
# trans_matrix1[1,3] = 1
trans_matrix[2,3] = -0.25
axis1.apply_transform(trans_matrix)
transform_matrix_list = trans_matrix.tolist()


data = {
    'center': oriented_bounding_box.centroid.tolist(),  # 中心点
    'extents': oriented_bounding_box.extents.tolist(),   # 尺寸
    'scale': 0.1,
    'contact_pose' : contact_pose,
    'target_pose' : target_pose,
    'trans_matrix' : transform_matrix_list
}
with open('./model_data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
    
# 将坐标轴添加到场景
axis = trimesh.creation.axis(axis_length=1.5)
# scene.add_geometry(axis)
scene.add_geometry(axis1)
scene.add_geometry(target_sphere)
scene.add_geometry(contact_sphere)
scene.show()