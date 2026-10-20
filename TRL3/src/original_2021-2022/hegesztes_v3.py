import open3d as o3d # 0.12 version
import numpy as np  # 1.15 version
import copy
import time
import matplotlib as mpl # 3.3 version
import matplotlib.pyplot as plt
from matplotlib import cm
# import pandas as pd
# import seaborn as sns


def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])


def convert2pc(cloud):
    temp = o3d.geometry.PointCloud()
    for point in cloud:
        temp.points.append(point.reshape(3, 1))
    return temp


def convert2pc2(cloud, normal):
    temp = o3d.geometry.PointCloud()
    for point in cloud:
        temp.points.append(point.reshape(3, 1))
    for norm in normal:
        temp.normals.append(norm.reshape(3, 1))
    return temp


class MplColorHelper:

    def __init__(self, cmap_name, start_val, stop_val):
        self.cmap_name = cmap_name
        # self.cmap = plt.get_cmap(cmap_name)
        self.cmap = my_cmap
        self.norm = mpl.colors.Normalize(vmin=start_val, vmax=stop_val)
        self.scalarMap = cm.ScalarMappable(norm=self.norm, cmap=self.cmap)

    def get_rgb(self, val):
        return self.scalarMap.to_rgba(val)


# 1. lépés: olvassuk be a mesheket
template_mesh = o3d.io.read_triangle_mesh("09vas.ply")
object_mesh = o3d.io.read_triangle_mesh("10grey.ply")
template_mesh.compute_vertex_normals()
object_mesh.compute_vertex_normals()

o3d.visualization.draw_geometries([template_mesh, object_mesh])

# 2. lépés: mintavételezzük a mesheket, hogy egyforma sűrűségű részeket kapjunk

# template_cloud = template_mesh.sample_points_poisson_disk(number_of_points=50, init_factor=4)
# object_cloud = object_mesh.sample_points_poisson_disk(number_of_points=50, init_factor=4) # lassubb

template_cloud = template_mesh.sample_points_uniformly(number_of_points=250000)  # kevésbé szép de gyors
object_cloud = object_mesh.sample_points_uniformly(number_of_points=250000)
o3d.visualization.draw_geometries([object_cloud])

print(len(np.asarray(object_cloud.points)))

print(object_cloud)

# 3. lépés: feature-alapú regisztráció: feature kiszámítása

template_pcr = np.mean(template_cloud.compute_nearest_neighbor_distance())
object_pcr = np.mean(object_cloud.compute_nearest_neighbor_distance())
pcr = (template_pcr + object_pcr) / 2

template_cloud_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
    template_cloud,
    o3d.geometry.KDTreeSearchParamHybrid(radius=pcr * 10, max_nn=1000))

object_cloud_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
    object_cloud,
    o3d.geometry.KDTreeSearchParamHybrid(radius=pcr * 10, max_nn=1000))

# 3. lépés: feature-alapú regisztráció: regisztráció

distance_threshold = pcr * 10

result = o3d.pipelines.registration.registration_fast_based_on_feature_matching(
    template_cloud, object_cloud, template_cloud_fpfh, object_cloud_fpfh,
    o3d.pipelines.registration.FastGlobalRegistrationOption(
        maximum_correspondence_distance=distance_threshold,
        iteration_number=500,
        maximum_tuple_count=2500))

print(result)
draw_registration_result(template_cloud, object_cloud, result.transformation)

# 4. lépés: iteartív regisztráció

icp_distance_threshold = pcr * 10

icp_result = o3d.pipelines.registration.registration_icp(
    template_cloud, object_cloud, icp_distance_threshold, result.transformation,
    o3d.pipelines.registration.TransformationEstimationPointToPlane(),
    o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=2000))

print(icp_result)
draw_registration_result(template_cloud, object_cloud, icp_result.transformation)

draw_registration_result(template_cloud, object_cloud, icp_result.transformation)

o3d.visualization.draw_geometries([object_cloud])

np.asarray(object_cloud.points)

np.asarray(template_cloud.points)

# a = np.asarray(template_cloud.points)
# np.savetxt("xyzz.csv", a, delimiter=",")

# 5. lépés: a távolságok kiszámítása

template_cloud_temp = copy.deepcopy(template_cloud)
template_cloud_temp.transform(icp_result.transformation)

dists = object_cloud.compute_point_cloud_distance(template_cloud_temp)

print(min(dists))
print(max(dists))
# print(dists)
plt.hist(dists, bins=20)
plt.show()

print(max(dists))

max(dists) * 25  # max távolság mm-ben

# 6. lépés: colormap vizualizáció

my_cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["green", "yellow", "red"])


COL = MplColorHelper('autumn_r', min(dists), np.percentile(dists, 95))

cols = []
for d in dists:
    cols.append(COL.get_rgb(d))
np_colors = np.array(cols)

object_cloud.colors = o3d.utility.Vector3dVector(np_colors[:, :3])

o3d.visualization.draw_geometries([object_cloud])

np.percentile(dists, 97)

# 7. lépés: jelöljük meg egy bizonyos hátárérték fölötti pontokat

kuszob = np.percentile(dists, 90)  # minél nagyobb lehet, kis hiba kimutatásához
counter = 0
outliers = []
outliers_normals = []
complementer = []
complementer_normals = []
object_cloud.paint_uniform_color([1, 0.706, 0])

for d in dists:
    if d > kuszob:
        np_colors[counter] = [0.0, 0.0, 0.0, 0.0]
        outliers.append(np.asarray(object_cloud.points)[counter])
        outliers_normals.append(np.asarray(object_cloud.normals)[counter])
    else:
        np_colors[counter] = [1, 0.706, 0, 0]
        complementer.append(np.asarray(object_cloud.points)[counter])
        complementer_normals.append(np.asarray(object_cloud.normals)[counter])
    counter += 1

object_cloud.colors = o3d.utility.Vector3dVector(np_colors[:, :3])
np_outliers = np.array(outliers)
np_outliers_normals = np.array(outliers_normals)

o3d.visualization.draw_geometries([object_cloud])

# new_pcr = np.average(object_cloud.compute_nearest_neighbor_distance()) #0.39

# 8. lépés: klaszterezük a kiugró részeket DBSCAN használatával #nem távolság alapu kell..
# sűrűség alapu klaszterezés, egy kupacban lévőket vizsgálja, o3d-ben ez van alapbol
cluster_count_threshold = 100  # minél kisebb a szám annál érzékenyebb
selected_cluster_ind = []

outlier_cloud = convert2pc2(np_outliers, np_outliers_normals)
comp_cloud = convert2pc2(np.asarray(complementer), np.asarray(complementer_normals))
comp_cloud.paint_uniform_color([1, 0.706, 0])

# o3d.visualization.draw_geometries([outlier_cloud])

dbscan_res = outlier_cloud.cluster_dbscan(pcr * 10, 100)  # sűrűség alapu klaszterezés,
print(len(np.unique(dbscan_res)))

uni = np.unique(dbscan_res)
cluster_clouds = []
cluster_ind = 0
for u in uni:  # végigmegyünk az egyedi klasztereken a kiugrók kivételével
    if u != -1:
        np_temp = np.asarray(outlier_cloud.points)[dbscan_res == u]
        np_temp_normals = np.asarray(outlier_cloud.normals)[dbscan_res == u]
        temp = convert2pc2(np_temp, np_temp_normals)
        if (len(np_temp) > cluster_count_threshold):
            selected_cluster_ind.append(cluster_ind)
            temp.paint_uniform_color([0, 0, 0])
        else:
            temp.paint_uniform_color([1, 0.706, 0])
        cluster_clouds.append(temp)
    cluster_ind += 1

i = 0
dbscan_cols = []
for p in np.asarray(outlier_cloud.points):
    c = cm.tab20(dbscan_res[i] + 1)
    dbscan_cols.append(c)
    i += 1

outlier_cloud.colors = o3d.utility.Vector3dVector(np.asarray(dbscan_cols)[:, :3])
o3d.visualization.draw_geometries([outlier_cloud, comp_cloud])

print(np_outliers)

# a = np.asarray(np_outliers)
# np.savetxt("out99.csv", a, delimiter=",")

print(selected_cluster_ind)
print(outlier_cloud)

cluster_clouds.append(comp_cloud)
o3d.visualization.draw_geometries(cluster_clouds)

# selected_cluster_ind

# np.asarray(cluster_clouds)[0]

# worst_cluster_cloud = np.asarray(cluster_clouds)[selected_cluster_ind][0]

# powerof2 = lambda x: x * 2

# error_dists = np.array(worst_cluster_cloud.compute_point_cloud_distance(template_cloud))
# rmse = np.sqrt(np.sum(powerof2(error_dists))/len(error_dists))
# rmse

# rmse*25
