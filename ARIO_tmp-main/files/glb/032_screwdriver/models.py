import trimesh
import json
import numpy as np












file_path = "./base.glb"
with open(file_path, 'rb') as file_obj:
    mesh = trimesh.load(file_obj, file_type='glb')
# mesh = trimesh.load(file_path, file_type='glb')
oriented_bounding_box = mesh.bounding_box_oriented
red_color = [1.0, 0.0, 0.0, 0.5]  # 红色, A=1 表示不透明


target_sphere = trimesh.creation.icosphere(subdivisions=2, radius=0.05)
target_trans_matrix_sphere = trimesh.transformations.translation_matrix([0, 0.9,0])
target_sphere.apply_transform(target_trans_matrix_sphere)
target_sphere.visual.vertex_colors = np.array([red_color] * len(target_sphere.vertices))
target_trans_list = target_trans_matrix_sphere.tolist()
# 创建一个场景
scene = trimesh.Scene(mesh)

# axis1
axis1 = trimesh.creation.axis(axis_length=1.5)
# 旋转矩阵的参数顺序是 (X, Y, Z)   to endpose axis
trans_matrix1 = trimesh.transformations.euler_matrix(0, 0,1.57)
# trans_matrix1[0,3] = 1
# trans_matrix1[1,3] = 1
# trans_matrix1[2,3] = -0.3
# 应用旋转矩阵到坐标轴
axis1.apply_transform(trans_matrix1)
scene.add_geometry(axis1)
transform_matrix_list1 = trans_matrix1.tolist()


# # 
# trans_matrix2 = trimesh.transformations.euler_matrix(-1.57, 0,1.57)
# trans_matrix2[2,3] = -0.3
# axis1.apply_transform(trans_matrix2)
# scene.add_geometry(axis1)
# # 

contact_sphere = trimesh.creation.icosphere(subdivisions=2, radius=0.2)
contact_trans_matrix_sphere = trimesh.transformations.translation_matrix([0, -0.5, 0])
contact_sphere.apply_transform(contact_trans_matrix_sphere)
contact_sphere.visual.vertex_colors = np.array([red_color] * len(contact_sphere.vertices))
contact_trans_list = contact_trans_matrix_sphere.tolist()


data = {
    'center': oriented_bounding_box.centroid.tolist(),  # 中心点
    'extents': oriented_bounding_box.extents.tolist(),   # 尺寸
    # 'grasp_pose1': transform_matrix_list1,
    'scale': 0.1,
    'contact_trans_list' : contact_trans_list,
    'target_trans_list' : contact_trans_list
}
with open('./model_data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)


# import transforms3d as t3d
# t3d.quaternions.quat2mat([0,0.707,0.707,0])
# gan_matrix = [[-1.0,0.0,0.0,0.13],
#               [0.0,0.0,1.0,0.18],
#               [0.0,1.0,0.0,0.9],
#               [0.0,0.0,0.0,1.0]]

# local_grasp_matrix = np.asarray(contact_trans_list)
# local_grasp_matrix[:3,3] *= 0.1
# global_grasp_pose_matrix1 = gan_matrix @ local_grasp_matrix

# tran2endpose_matrix1 = trimesh.transformations.euler_matrix(3.14,3.14,1.57)
# global_grasp_pose_matrix =global_grasp_pose_matrix1  @ tran2endpose_matrix1

# global_grasp_pose_matrix_q = global_grasp_pose_matrix[:3,:3]
# global_grasp_pose_matrix_p = global_grasp_pose_matrix[:3,3] 
# grasp_pose_q = t3d.quaternions.mat2quat(global_grasp_pose_matrix_q)
# pre_pose = list(global_grasp_pose_matrix_p)+list(grasp_pose_q)
# print(pre_pose[3],pre_pose[4],pre_pose[5],pre_pose[6])
# -0.707 0 0 -0.707
# 将坐标轴添加到场景
axis = trimesh.creation.axis(axis_length=1.5)
# axis.apply_transform(trimesh.transformations.euler_matrix(-1.57, 1.57, 0))
# scene.add_geometry(axis)
# scene.add_geometry(axis1)
# 可视化网格和坐标轴
scene.add_geometry(target_sphere)
scene.add_geometry(contact_sphere)
scene.show()