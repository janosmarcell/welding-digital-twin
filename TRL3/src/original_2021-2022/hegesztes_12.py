#!/usr/bin/env python
# coding: utf-8

# In[1]:


import open3d as o3d
import numpy as np
import copy
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm

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
        temp.points.append(point.reshape(3,1))
    return temp

def convert2pc2(cloud, normal):
    temp = o3d.geometry.PointCloud()
    for point in cloud:
        temp.points.append(point.reshape(3,1))
    for norm in normal:
        temp.normals.append(norm.reshape(3,1))
    return temp

class MplColorHelper:

  def __init__(self, cmap_name, start_val, stop_val):
    self.cmap_name = cmap_name
    #self.cmap = plt.get_cmap(cmap_name)
    self.cmap=my_cmap
    self.norm = mpl.colors.Normalize(vmin=start_val, vmax=stop_val)
    self.scalarMap = cm.ScalarMappable(norm=self.norm, cmap=self.cmap)

  def get_rgb(self, val):
    return self.scalarMap.to_rgba(val)


# In[2]:


# 1. lépés: olvassuk be a mesheket

template_mesh = o3d.io.read_triangle_mesh("x:/12/idealis_a3.ply")
object_mesh = o3d.io.read_triangle_mesh("x:/12/amk_a3C.ply")

template_mesh.compute_vertex_normals()
object_mesh.compute_vertex_normals()


# In[3]:


o3d.visualization.draw_geometries([template_mesh, object_mesh])


# In[4]:


get_ipython().run_cell_magic('time', '', '\n# 2. lépés: mintavételezzük a mesheket, hogy egyforma sűrűségű részeket kapjunk\n\n#template_cloud = template_mesh.sample_points_poisson_disk(number_of_points=50, init_factor=4)\n#object_cloud = object_mesh.sample_points_poisson_disk(number_of_points=50, init_factor=4) # lassubb\n\ntemplate_cloud = template_mesh.sample_points_uniformly(number_of_points=250000) #kevésbé szép de gyors\nobject_cloud = object_mesh.sample_points_uniformly(number_of_points=250000)\no3d.visualization.draw_geometries([object_cloud])\n\nprint(len(np.asarray(object_cloud.points)))')


# In[8]:


#o3d.io.write_point_cloud("c:/users/dell/3mmvarratu/02vas.pcd", template_cloud)
#o3d.io.write_point_cloud("c:/users/dell/3mmvarratu/a5vn.pcd", object_cloud)


# In[5]:


get_ipython().run_cell_magic('time', '', '\n# 3. lépés: feature-alapú regisztráció: feature kiszámítása\n\ntemplate_pcr = np.mean(template_cloud.compute_nearest_neighbor_distance())\nobject_pcr = np.mean(object_cloud.compute_nearest_neighbor_distance())\npcr = (template_pcr + object_pcr)/2\n \ntemplate_cloud_fpfh = o3d.pipelines.registration.compute_fpfh_feature(\n    template_cloud,\n    o3d.geometry.KDTreeSearchParamHybrid(radius=pcr * 10, max_nn=1000))\n\nobject_cloud_fpfh = o3d.pipelines.registration.compute_fpfh_feature(\n    object_cloud,\n    o3d.geometry.KDTreeSearchParamHybrid(radius=pcr * 10, max_nn=1000))')


# In[6]:


get_ipython().run_cell_magic('time', '', '\n# 3. lépés: feature-alapú regisztráció: regisztráció\n\ndistance_threshold = pcr*10\n\nresult = o3d.pipelines.registration.registration_fgr_based_on_feature_matching(\n        template_cloud, object_cloud, template_cloud_fpfh, object_cloud_fpfh,\n        o3d.pipelines.registration.FastGlobalRegistrationOption(\n            maximum_correspondence_distance=distance_threshold, \n            iteration_number=500,\n            maximum_tuple_count=2500))\n\nprint(result)\ndraw_registration_result(template_cloud, object_cloud, result.transformation)')


# In[7]:


get_ipython().run_cell_magic('time', '', '\n# 4. lépés: iteartív regisztráció\n\nicp_distance_threshold = pcr*10\n\nicp_result = o3d.pipelines.registration.registration_icp(\n        template_cloud, object_cloud, icp_distance_threshold, result.transformation,\n        o3d.pipelines.registration.TransformationEstimationPointToPlane(),\n        o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=2000))\n\nprint(icp_result)\ndraw_registration_result(template_cloud, object_cloud, icp_result.transformation)')


# In[30]:


draw_registration_result(template_cloud, object_cloud, icp_result.transformation)


# In[31]:


o3d.visualization.draw_geometries([object_cloud])


# In[8]:


get_ipython().run_cell_magic('time', '', '\n#5. lépés: a távolságok kiszámítása\n\ntemplate_cloud_temp = copy.deepcopy(template_cloud)\ntemplate_cloud_temp.transform(icp_result.transformation)\n\ndists = object_cloud.compute_point_cloud_distance(template_cloud_temp)')


# In[9]:


print(min(dists))
print(max(dists))

plt.hist(dists, bins=20)
plt.show()


# In[10]:


print(max(dists))


# In[11]:


max(dists)*25              # max távolság mm-ben


# In[12]:


get_ipython().run_cell_magic('time', '', '\n# 6. lépés: colormap vizualizáció\n\nmy_cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["green","yellow","red"])\n\nimport numpy as np\n\nCOL = MplColorHelper(\'autumn_r\', min(dists), np.percentile(dists, 95))\n\ncols = []\nfor d in dists:\n    cols.append(COL.get_rgb(d))\nnp_colors = np.array(cols)\n\nobject_cloud.colors = o3d.utility.Vector3dVector(np_colors[:,:3])\n\no3d.visualization.draw_geometries([object_cloud])')


# In[17]:


np.percentile(dists, 99)


# In[29]:


get_ipython().run_cell_magic('time', '', '\n## 7. lépés: jelöljük meg egy bizonyos hátárérték fölötti pontokat\n\nkuszob = np.percentile(dists, 90)  #minél nagyobb lehet, kis hiba kimutatásához\ncounter = 0\noutliers = []\noutliers_normals = []\ncomplementer = []\ncomplementer_normals = []\nobject_cloud.paint_uniform_color([1, 0.706, 0])\n\nfor d in dists:\n    if d > kuszob:\n        np_colors[counter] = [0.0,0.0,0.0,0.0]\n        outliers.append(np.asarray(object_cloud.points)[counter])\n        outliers_normals.append(np.asarray(object_cloud.normals)[counter])\n    else:\n        np_colors[counter] = [1, 0.706, 0, 0]\n        complementer.append(np.asarray(object_cloud.points)[counter])\n        complementer_normals.append(np.asarray(object_cloud.normals)[counter])\n    counter+=1\n\nobject_cloud.colors = o3d.utility.Vector3dVector(np_colors[:,:3])\nnp_outliers = np.array(outliers)\nnp_outliers_normals = np.array(outliers_normals)\n\no3d.visualization.draw_geometries([object_cloud])\n\n#new_pcr = np.average(object_cloud.compute_nearest_neighbor_distance()) #0.39')


# In[21]:


get_ipython().run_cell_magic('time', '', '\n## 8. lépés: klaszterezük a kiugró részeket DBSCAN használatával #nem távolság alapu kell..\n#sűrűség alapu klaszterezés, egy kupacban lévőket vizsgálja, o3d-ben ez van alapbol\ncluster_count_threshold = 400   # minél kisebb a szám annál érzékenyebb\nselected_cluster_ind = []\n\noutlier_cloud = convert2pc2(np_outliers, np_outliers_normals)\ncomp_cloud = convert2pc2(np.asarray(complementer), np.asarray(complementer_normals))\ncomp_cloud.paint_uniform_color([1, 0.706, 0])\n\n#o3d.visualization.draw_geometries([outlier_cloud])\n\ndbscan_res = outlier_cloud.cluster_dbscan(pcr*15, 100) #sűrűség alapu klaszterezés, \nprint(len(np.unique(dbscan_res)))\n\nuni = np.unique(dbscan_res)\ncluster_clouds = []\ncluster_ind = 0\nfor u in uni: # végigmegyünk az egyedi klasztereken a kiugrók kivételével\n    if u != -1:\n        np_temp = np.asarray(outlier_cloud.points)[dbscan_res==u]\n        np_temp_normals = np.asarray(outlier_cloud.normals)[dbscan_res==u]\n        temp = convert2pc2(np_temp, np_temp_normals)\n        if(len(np_temp) > cluster_count_threshold):\n            selected_cluster_ind.append(cluster_ind)\n            temp.paint_uniform_color([0,0,0])\n        else:\n            temp.paint_uniform_color([1, 0.706, 0])\n        cluster_clouds.append(temp)\n    cluster_ind += 1\n        \ni = 0\ndbscan_cols = []\nfor p in np.asarray(outlier_cloud.points):\n    c = cm.tab20(dbscan_res[i]+1)\n    dbscan_cols.append(c)\n    i+=1\n\noutlier_cloud.colors = o3d.utility.Vector3dVector(np.asarray(dbscan_cols)[:,:3])\no3d.visualization.draw_geometries([outlier_cloud, comp_cloud])')


# In[22]:


cluster_clouds.append(comp_cloud)
o3d.visualization.draw_geometries(cluster_clouds)


# selected_cluster_ind

# In[23]:


np.asarray(cluster_clouds)[0]


# In[25]:


worst_cluster_cloud = np.asarray(cluster_clouds)[selected_cluster_ind][0]


# In[26]:


powerof2 = lambda x: x * 2

error_dists = np.array(worst_cluster_cloud.compute_point_cloud_distance(template_cloud))
rmse = np.sqrt(np.sum(powerof2(error_dists))/len(error_dists))
rmse


# In[27]:


rmse*25


# In[28]:


sump = np.array([0,0,0])
for p in np.asarray(worst_cluster_cloud.points):
    sump = sump + p
meanp = sump/len(np.asarray(worst_cluster_cloud.points))
meanp


# In[39]:


worst_cluster_cloud.translate([np.asarray(worst_cluster_cloud.points)[:,0].min(),                              np.asarray(worst_cluster_cloud.points)[:,1].min(),                              np.asarray(worst_cluster_cloud.points)[:,2].min()])

