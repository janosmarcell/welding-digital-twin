from pandemonium import exposed, export, signal, Node, ArrayMesh, Image
from pandemonium.bindings import _Thread as Thread
from pandemonium.bindings import _Mutex as Mutex
from pandemonium import *

import os
from io import BytesIO

import open3d as o3d
import numpy as np
import copy
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.figure import Figure

class MplColorHelper:
	def __init__(self, cmap_name, start_val, stop_val, my_cmap):
		self.cmap_name = cmap_name
		#self.cmap = plt.get_cmap(cmap_name)
		self.cmap=my_cmap
		self.norm = mpl.colors.Normalize(vmin=start_val, vmax=stop_val)
		self.scalarMap = cm.ScalarMappable(norm=self.norm, cmap=self.cmap)

	def get_rgb(self, val):
		return self.scalarMap.to_rgba(val)

@exposed
class PointCloudProcessor(Node):
	work_finished = export(bool)
	
	results = Array()
	results_version = 0
	result_mutex = None
	
	worklog = ""
	worklog_version = 0
	worklog_mutex = None
	
	worker_thread = None
	worker_thread_cancel = False
	
	template_mesh_path = ""
	object_mesh_path = ""
	
	def draw_registration_result(self, source, target, transformation):
		source_temp = copy.deepcopy(source)
		target_temp = copy.deepcopy(target)
		source_temp.paint_uniform_color([1, 0.706, 0])
		target_temp.paint_uniform_color([0, 0.651, 0.929])
		source_temp.transform(transformation)
		#o3d.visualization.draw_geometries([source_temp, target_temp])
		
		return Array([
			self.o3dpoint_cloud_to_mesh(source_temp),
			self.o3dpoint_cloud_to_mesh(target_temp)
		])
		

	def convert2pc(self, cloud):
		temp = o3d.geometry.PointCloud()
		for point in cloud:
			temp.points.append(point.reshape(3,1))
		return temp

	def convert2pc2(self, cloud, normal):
		temp = o3d.geometry.PointCloud()
		for point in cloud:
			temp.points.append(point.reshape(3,1))
		for norm in normal:
			temp.normals.append(norm.reshape(3,1))
		return temp
	
	# Logging API
	
	def get_log(self):
		self.worklog_mutex.lock()
		ls = GDString(self.worklog)
		self.worklog_mutex.unlock()
		return ls
	
	def append_log(self, line):
		self.worklog_mutex.lock()
		
		if self.worklog != "":
			self.worklog += "\n"
			
		self.worklog += line
		self.worklog_version += 1
		self.worklog_mutex.unlock()
		
	def clear_log(self):
		self.worklog_mutex.lock()
		self.worklog = ""
		self.worklog_version = 0
		self.worklog_mutex.unlock()
	
	def get_log_version(self):
		self.worklog_mutex.lock()
		ver = self.worklog_version
		self.worklog_mutex.unlock()
		
		return ver
	
	# Results API
	
	def get_results(self):
		self.result_mutex.lock()
		res = self.results.duplicate()
		self.result_mutex.unlock()
		return res
	
	def append_result(self, data, increase_version = True):
		self.result_mutex.lock()
		self.results.append(data)
		
		if increase_version:
			self.results_version += 1
		
		self.result_mutex.unlock()
		
	def clear_results(self):
		self.result_mutex.lock()
		self.results = Array()
		self.results_version = 0
		self.result_mutex.unlock()
	
	def get_results_version(self):
		self.worklog_mutex.lock()
		ver = self.results_version
		self.worklog_mutex.unlock()
		
		return ver
	
	# Conversions
	
	def fig_to_image(self, fig):
		buf = BytesIO()
		fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
		view = buf.getbuffer()
		
		png_data = PoolByteArray()
		
		for i in range(len(view)):
			png_data.push_back(view[i])
			
		img = Image()
		img.load_png_from_buffer(png_data)
		
		return img
	
	def o3dmesh_to_mesh(self, mesh):
		arrs = Array()
		arrs.resize(ArrayMesh.ARRAY_MAX)
		
		if mesh.has_textures():
			print("mesh.has_textures()!")
			print(mesh.has_textures())
		
		if mesh.has_triangle_material_ids():
			print(mesh.has_triangle_material_ids())
			
		if mesh.has_vertex_normals():
			normals = np.asarray(mesh.vertex_normals)
			
			ns = PoolVector3Array()
			
			for n in normals:
				ns.push_back(Vector3(n[0], n[1], n[2]))
			
			arrs[ArrayMesh.ARRAY_NORMAL] = ns
			

		if mesh.has_triangle_uvs():
			uvs = np.asarray(mesh.triangle_uvs)
			
			ns = PoolVector2Array()
			
			for n in uvs:
				ns.push_back(Vector2(n[0], n[1]))
			
			arrs[ArrayMesh.ARRAY_TEX_UV] = ns
			
			
		if mesh.has_vertex_colors():
			colors = np.asarray(mesh.vertex_colors)
			
			ns = PoolColorArray()
			
			for n in colors:
				ns.push_back(Color(n[0], n[1], n[2]))
			
			arrs[ArrayMesh.ARRAY_COLOR] = ns
			
					
		if mesh.has_vertices():
			vertices = np.asarray(mesh.vertices)
			
			ns = PoolVector3Array()
			
			for n in vertices:
				ns.push_back(Vector3(n[0], n[1], n[2]))
			
			arrs[ArrayMesh.ARRAY_VERTEX] = ns
		
		
		if mesh.has_triangles():
			triangles = np.asarray(mesh.triangles)

			ns = PoolIntArray()

			for n in triangles:
				ns.push_back(n[1])
				ns.push_back(n[0])
				ns.push_back(n[2])

			arrs[ArrayMesh.ARRAY_INDEX] = ns
		
		am = ArrayMesh()
		
		am.add_surface_from_arrays(ArrayMesh.PRIMITIVE_TRIANGLES, arrs)
		
		return am

	def o3dpoint_cloud_to_mesh(self, mesh):
		arrs = Array()
		arrs.resize(ArrayMesh.ARRAY_MAX)
		
		if mesh.has_normals():
			normals = np.asarray(mesh.normals)
			
			ns = PoolVector3Array()
			
			for n in normals:
				ns.push_back(Vector3(n[0], n[1], n[2]))
			
			arrs[ArrayMesh.ARRAY_NORMAL] = ns
			
			
		if mesh.has_colors():
			colors = np.asarray(mesh.colors)
			
			ns = PoolColorArray()
			
			for n in colors:
				ns.push_back(Color(n[0], n[1], n[2]))
			
			arrs[ArrayMesh.ARRAY_COLOR] = ns
			
					
		if mesh.has_points():
			vertices = np.asarray(mesh.points)
			
			ns = PoolVector3Array()
			
			for n in vertices:
				ns.push_back(Vector3(n[0], n[1], n[2]))
			
			arrs[ArrayMesh.ARRAY_VERTEX] = ns
		
		
		am = ArrayMesh()
		
		am.add_surface_from_arrays(ArrayMesh.PRIMITIVE_POINTS, arrs)
		
		return am
		
	# Main

	def run(self, template_mesh_path, object_mesh_path):
		if self.worker_thread is not None:
			if self.worker_thread.is_alive():
				return
				
			self.worker_thread.wait_to_finish()
			self.worker_thread = None
			
		self.template_mesh_path = template_mesh_path
		self.object_mesh_path = object_mesh_path
		
		self.clear_log()
		self.clear_results();
		
		self.work_finished = False
		self.worker_thread_cancel = False
		
		self.worker_thread = Thread()
		self.worker_thread.start(self, "_thread_run")
	
	def cancel(self):
		self.worker_thread_cancel = True
		
		if self.worker_thread is None:
			return
		
		self.worker_thread.wait_to_finish()
		self.worker_thread = None
	
	def _thread_run(self, userdata):
		# 1. lépés: olvassuk be a mesheket
		
		self.append_log("Step 1: Reading in the meshes.")

		template_mesh = o3d.io.read_triangle_mesh(str(self.template_mesh_path))
		object_mesh = o3d.io.read_triangle_mesh(str(self.object_mesh_path))

		template_mesh.compute_vertex_normals()
		object_mesh.compute_vertex_normals()

		self.append_result(Dictionary({ 
			"result_type": "display_single_mesh",
			"mesh_data": self.o3dmesh_to_mesh(template_mesh),
			"result_description": "Step 1, 1 / 3:\n\nTemplate Mesh: Display",
		}), False)
		
		self.append_result(Dictionary({ 
			"result_type": "display_single_mesh",
			"mesh_data": self.o3dmesh_to_mesh(object_mesh),
			"result_description": "Step 1, 2 / 3:\n\nObject Mesh: Display",
		}), False)
		
		self.append_result(Dictionary({ 
			"result_type": "display_meshes",
			"meshes": Array([self.o3dmesh_to_mesh(template_mesh), self.o3dmesh_to_mesh(object_mesh)]),
			"result_description": "Step 1, 3 / 3:\n\nBoth meshes: Display",
		}))
		
		self.append_log("Done.")
		
		# This method runs in a different thread, this lets you exit earlier
		if self.worker_thread_cancel:
			return

		# 2. lépés: mintavételezzük a mesheket, hogy egyforma sűrűségű részeket kapjunk
		
		self.append_log("Step 2: Sampling the meshes uniformly.")

		#template_cloud = template_mesh.sample_points_poisson_disk(number_of_points=50, init_factor=4)
		#object_cloud = object_mesh.sample_points_poisson_disk(number_of_points=50, init_factor=4) # lassubb

		template_cloud = template_mesh.sample_points_uniformly(number_of_points=250000) #kevésbé szép de gyors
		object_cloud = object_mesh.sample_points_uniformly(number_of_points=250000)
		
		self.append_result(Dictionary({ 
			"result_type": "display_single_mesh",
			"mesh_data": self.o3dpoint_cloud_to_mesh(template_cloud),
			"result_description": "Step 2, 1 / 3:\n\nTemplate Mesh: Uniformly sampled mesh cloud display",
		}), False)
		
		self.append_result(Dictionary({ 
			"result_type": "display_single_mesh",
			"mesh_data": self.o3dpoint_cloud_to_mesh(object_cloud),
			"result_description": "Step 2, 2 / 3:\n\nObject Mesh: Uniformly sampled mesh cloud display",
		}), False)
		
		self.append_result(Dictionary({ 
			"result_type": "display_meshes",
			"meshes": Array([self.o3dpoint_cloud_to_mesh(template_cloud), self.o3dpoint_cloud_to_mesh(object_cloud)]),
			"result_description": "Step 2, 3 / 3:\n\nBoth meshes: Uniformly sampled mesh cloud display",
		}))

		#print(len(np.asarray(object_cloud.points)))
		
		self.append_log("Done.")
		
		if self.worker_thread_cancel:
			return
		
		#o3d.io.write_point_cloud("c:/users/dell/3mmvarratu/02vas.pcd", template_cloud)
		#o3d.io.write_point_cloud("c:/users/dell/3mmvarratu/a5vn.pcd", object_cloud)

		# 3. lépés: feature-alapú regisztráció: feature kiszámítása
		
		self.append_log("Step 3, 1 / 2: Feature based registration: Feature calculation. (Will hang the main thread for a bit.)")

		template_pcr = np.mean(template_cloud.compute_nearest_neighbor_distance())
		object_pcr = np.mean(object_cloud.compute_nearest_neighbor_distance())
		pcr = (template_pcr + object_pcr)/2

		template_cloud_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
			template_cloud, 
			o3d.geometry.KDTreeSearchParamHybrid(radius=pcr*10, max_nn=1000))

		object_cloud_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
			object_cloud, 
			o3d.geometry.KDTreeSearchParamHybrid(radius=pcr*10, max_nn=1000))

		self.append_log("Done.")
		
		if self.worker_thread_cancel:
			return

		# 3. lépés: feature-alapú regisztráció: regisztráció
		
		self.append_log("Step 3, 2 / 2: Feature based registration: Registration.")

		distance_threshold = pcr*10

		result = o3d.pipelines.registration.registration_fast_based_on_feature_matching(
				template_cloud, object_cloud, template_cloud_fpfh, object_cloud_fpfh,
				o3d.pipelines.registration.FastGlobalRegistrationOption(
					maximum_correspondence_distance=distance_threshold, 
					iteration_number=500,
					maximum_tuple_count=2500))
					

		#print(result)
		drr = self.draw_registration_result(template_cloud, object_cloud, result.transformation)
		
		self.append_result(Dictionary({ 
			"result_type": "display_meshes",
			"meshes": drr,
			"result_description": "Step 3:\n\nFeature based registration",
		}))

		self.append_log("Done.")
		
		if self.worker_thread_cancel:
			return
		
		# 4. lépés: iteartív regisztráció
		
		self.append_log("Step 4: Iterative registration.")

		icp_distance_threshold = pcr*10

		icp_result = o3d.pipelines.registration.registration_icp(
				template_cloud, object_cloud, icp_distance_threshold, result.transformation,
				o3d.pipelines.registration.TransformationEstimationPointToPlane(),
				o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=2000))

		#print(icp_result)
		#o3d.visualization.draw_geometries([object_cloud])
		
		drr = self.draw_registration_result(template_cloud, object_cloud, icp_result.transformation)
		
		self.append_result(Dictionary({ 
			"result_type": "display_meshes",
			"meshes": drr,
			"result_description": "Step 4:\n\nIterative registration",
		}))
		
		self.append_log("Done.")
		
		if self.worker_thread_cancel:
			return

		#5. lépés: a távolságok kiszámítása
		
		self.append_log("Step 5: Distance calculations.")

		template_cloud_temp = copy.deepcopy(template_cloud)
		template_cloud_temp.transform(icp_result.transformation)

		dists = object_cloud.compute_point_cloud_distance(template_cloud_temp)

		#print(min(dists))
		#print(max(dists))
		#min(dists)*25              # max távolság mm-ben
		#print(dists)
		
		# non-pyplot style
		fig = Figure()
		ax = fig.subplots()
		ax.hist(dists, bins=20)
		#plt.hist(dists, bins=20)
		res_img = self.fig_to_image(fig)
		
		disttext = "Step 5, 1 / 2:\n\nDistance results:\nMin distance: " + str(min(dists)*25) + " mm\nMax distance: " + str(max(dists)*25) + " mm"
		
		self.append_result(Dictionary({ 
			"result_type": "display_text",
			"result_description": disttext,
		}), False)
		
		self.append_result(Dictionary({ 
			"result_type": "display_image",
			"image": res_img,
			"result_description": "Step 5, 2 / 2:\n\nDistance Histogram",
		}))
		
		self.append_log("Done.")

		# 6. lépés: colormap vizualizáció
		
		self.append_log("Step 6: Colormap visualization. (Will hang the main thread for a bit.)")

		my_cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["green","yellow","red"])

		COL = MplColorHelper('autumn_r', min(dists), np.percentile(dists, 95), my_cmap)

		cols = []
		for d in dists:
			cols.append(COL.get_rgb(d))
		np_colors = np.array(cols)

		object_cloud.colors = o3d.utility.Vector3dVector(np_colors[:,:3])

		#o3d.visualization.draw_geometries([object_cloud])

		self.append_result(Dictionary({ 
			"result_type": "display_single_mesh",
			"mesh_data": self.o3dpoint_cloud_to_mesh(object_cloud),
			"result_description": "Step 6:\n\nObject Cloud with Colormap",
		}))
		
		#np.percentile(dists, 90)
		
		self.append_log("Done.")
		
		if self.worker_thread_cancel:
			return

		## 7. lépés: jelöljük meg egy bizonyos hátárérték fölötti pontokat
		
		self.append_log("Step 7: Mark points if they ar above a certain threshold.")

		kuszob = np.percentile(dists, 90)  #minél nagyobb lehet, kis hiba kimutatásához
		counter = 0
		outliers = []
		outliers_normals = []
		complementer = []
		complementer_normals = []
		object_cloud.paint_uniform_color([1, 0.706, 0])

		for d in dists:
			if d > kuszob:
				np_colors[counter] = [0.0,0.0,0.0,0.0]
				outliers.append(np.asarray(object_cloud.points)[counter])
				outliers_normals.append(np.asarray(object_cloud.normals)[counter])
			else:
				np_colors[counter] = [1, 0.706, 0, 0]
				complementer.append(np.asarray(object_cloud.points)[counter])
				complementer_normals.append(np.asarray(object_cloud.normals)[counter])
			counter+=1

		object_cloud.colors = o3d.utility.Vector3dVector(np_colors[:,:3])
		np_outliers = np.array(outliers)
		np_outliers_normals = np.array(outliers_normals)

		#o3d.visualization.draw_geometries([object_cloud])
		
		self.append_result(Dictionary({ 
			"result_type": "display_single_mesh",
			"mesh_data": self.o3dpoint_cloud_to_mesh(object_cloud),
			"result_description": "Step 7:\n\nObject Cloud with Points above a certain threshold marked.",
		}))

		#new_pcr = np.average(object_cloud.compute_nearest_neighbor_distance()) #0.39
		
		self.append_log("Done.")
		
		if self.worker_thread_cancel:
			return

		## 8. lépés: klaszterezük a kiugró részeket DBSCAN használatával
		
		self.append_log("Step 8: Clustering using DBSCAN.")
		
		#nem távolság alapu kell..
		#sűrűség alapu klaszterezés, egy kupacban lévőket vizsgálja, o3d-ben ez van alapbol
		cluster_count_threshold = 400   # minél kisebb a szám annál érzékenyebb
		selected_cluster_ind = []

		outlier_cloud = self.convert2pc2(np_outliers, np_outliers_normals)
		comp_cloud = self.convert2pc2(np.asarray(complementer), np.asarray(complementer_normals))
		comp_cloud.paint_uniform_color([1, 0.706, 0])

		#o3d.visualization.draw_geometries([outlier_cloud])

		dbscan_res = outlier_cloud.cluster_dbscan(pcr*15, 100) #sűrűség alapu klaszterezés, 
		#print(len(np.unique(dbscan_res)))

		uni = np.unique(dbscan_res)
		cluster_clouds = []
		cluster_ind = 0
		for u in uni: # végigmegyünk az egyedi klasztereken a kiugrók kivételével
			if u != -1:
				np_temp = np.asarray(outlier_cloud.points)[dbscan_res==u]
				np_temp_normals = np.asarray(outlier_cloud.normals)[dbscan_res==u]
				temp = self.convert2pc2(np_temp, np_temp_normals)
				if(len(np_temp) > cluster_count_threshold):
					selected_cluster_ind.append(cluster_ind)
					temp.paint_uniform_color([0,0,0])
				else:
					temp.paint_uniform_color([1, 0.706, 0])
				cluster_clouds.append(temp)
			cluster_ind += 1
				
		i = 0
		dbscan_cols = []
		for p in np.asarray(outlier_cloud.points):
			c = cm.tab20(dbscan_res[i]+1)
			dbscan_cols.append(c)
			i+=1

		outlier_cloud.colors = o3d.utility.Vector3dVector(np.asarray(dbscan_cols)[:,:3])
		#o3d.visualization.draw_geometries([outlier_cloud, comp_cloud])
		
		self.append_result(Dictionary({ 
			"result_type": "display_meshes",
			"meshes": Array([ self.o3dpoint_cloud_to_mesh(outlier_cloud), self.o3dpoint_cloud_to_mesh(comp_cloud) ]),
			"result_description": "Step 8, 1 / 2:\n\nOutlier and Comp clouds.",
		}))

		cluster_clouds.append(comp_cloud)
		#o3d.visualization.draw_geometries(cluster_clouds)
		
		cc_mesh_data = Array()
		
		for c in cluster_clouds:
			cc_mesh_data.append(self.o3dpoint_cloud_to_mesh(c))
		
		self.append_result(Dictionary({ 
			"result_type": "display_meshes",
			"meshes": cc_mesh_data,
			"result_description": "Step 8, 2 / 2:\n\nCluster clouds.",
		}))
		
		self.append_log("Done.")

#		#selected_cluster_ind
#
#		self.append_log("Step 9: Cluster cloud generation")
#
#		np.asarray(cluster_clouds)[0]
#
#		worst_cluster_cloud = np.asarray(cluster_clouds)[selected_cluster_ind][0]
#
#		powerof2 = lambda x: x * 2
#
#		error_dists = np.array(worst_cluster_cloud.compute_point_cloud_distance(template_cloud))
#		rmse = np.sqrt(np.sum(powerof2(error_dists))/len(error_dists))
#
#		print(rmse*25)
#
#		sump = np.array([0,0,0])
#		for p in np.asarray(worst_cluster_cloud.points):
#			sump = sump + p
#		meanp = sump/len(np.asarray(worst_cluster_cloud.points))
#		meanp
#
#		worst_cluster_cloud.translate([np.asarray(worst_cluster_cloud.points)[:,0].min(), \
#									 np.asarray(worst_cluster_cloud.points)[:,1].min(), \
#									 np.asarray(worst_cluster_cloud.points)[:,2].min()])
#
#
#		self.append_log("Done.")
		
		self.append_log("Processing Done!")
		
		self.work_finished = True

	def _ready(self):
		self.work_finished = False
		self.worklog_mutex = Mutex()
		self.result_mutex = Mutex()
		
		self.results = Array()
		self.results_version = 0
		self.worklog = ""
		self.worklog_version = 0
		
		self.worker_thread = None
		self.worker_thread_cancel = False
		
		self.template_mesh_path = ""
		self.object_mesh_path = ""
		
		# This code is needed to be able to use matplotlib with pyplot
		# (It will be able to open tk windows, etc)
		
		if OS.has_feature("Windows"):
			os.environ["TCL_LIBRARY"] = os.path.abspath(".") + "/addons/pythonscript/windows-64/tcl/tcl8.6/"
			os.environ["TK_LIBRARY"] = os.path.abspath(".") + "/addons/pythonscript/windows-64/tcl/tcl8.6/"
		elif OS.has_feature("X11"):
			os.environ["TCL_LIBRARY"] = os.path.abspath(".") + "/addons/pythonscript/x11-64/lib/tcl8.6/"
			os.environ["TK_LIBRARY"] = os.path.abspath(".") + "/addons/pythonscript/x11-64/lib/tcl8.6/"
		
		# Pyplot style plotting example:
		
#		fig = plt.figure()
#		x = np.arange(10)
#		y = 2.5 * np.sin(x / 20 * np.pi)
#		yerr = np.linspace(0.05, 0.2, 10)
#		plt.errorbar(x, y + 3, yerr=yerr, label='both limits (default)')
#		plt.errorbar(x, y + 2, yerr=yerr, uplims=True, label='uplims=True')
#		plt.errorbar(x, y + 1, yerr=yerr, uplims=True, lolims=True,
#					 label='uplims=True, lolims=True')
#		upperlimits = [True, False] * 5
#		lowerlimits = [False, True] * 5
#		plt.errorbar(x, y, yerr=yerr, uplims=upperlimits, lolims=lowerlimits,
#					 label='subsets of uplims and lolims')
#		plt.legend(loc='lower right')
#		plt.show()
	
	def _exit_tree(self):
		self.worker_thread_cancel = True
		
		if self.worker_thread is None:
			return
		
		self.worker_thread.wait_to_finish()
		self.worker_thread = None
