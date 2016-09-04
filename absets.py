#plugin info and stuff
bl_info = {
    "name": "Absets",
    "description": "Abdou's asset manager",
    "author": "Abdou Bouam",
    "version": (0, 0),
    "blender": (2, 7, 8),
    "location": "View3D > Toolshelf",
    "description": "Adds assets",
    "warning": "",
    "wiki_url": "http://make_a_wiki_for_this",
    "category": "Import-Export"}




"""
	ABSets, Abdou's Asset manager
	work in progress, main goals are :
		a functionnal asset manager with basic operations (export, import, edit)
		automated asset exportation to libraries
		main asset types are models with their materials

	secondary goals :
	full materials with possibility of customization (re-export after tweaks)
	possible replacement for "node presets" by Campbell Barton with more features
	(add categories and previews to the nodes, don't show incompativle nodes
	(no compositor node groups inside material editor for example))
	light setups and backgrounds

bpy.ops.image.open(filepath="/home/abdou/Desktop/blender/images/HDRI/studio3.exr"\
, directory="/home/abdou/Desktop/blender/images/HDRI/", files=[{"name":"studio3.exr"\
, "name":"studio3.exr"}], relative_path=False, show_multiview=False)

"""
def abset_env():
    #import HDR
    img_path="~/Desktop/blender/images/HDRI/studio3.exr"
    path =os.path.expanduser(img_path)
    img=bpy.data.images.load(path)
    img.name="studio"
    world = bpy.context.scene.world
    nodetree=world.node_tree.nodes
    #clean everything and start from scratch
    for node in nodetree:
        nodetree.remove(node)
        #add environment nodes
    node_out=nodetree.new(type="ShaderNodeOutputWorld")
    node_bg=nodetree.new(type="ShaderNodeBackground")
    node_tex=nodetree.new(type="ShaderNodeTexEnvironment")
    node_tex.image=bpy.data.images.get("studio")
    #attach nodes
    world.node_tree.links.new(node_tex.outputs[0],node_bg.inputs[0])
    world.node_tree.links.new(node_bg.outputs[0],node_out.inputs[0])
def abset_cam():
    #create camera
    cam = bpy.data.cameras.new("Absets_cam")
    cam_ob = bpy.data.objects.new("Absets_cam", cam)
    bpy.context.scene.objects.link(cam_ob)
    #translate and rotate
    cam_ob.location=[-10,-10,10]
    cam_ob.rotation_euler=[pi/3,0,-pi/4]
    #make larger lens to zoom in
    bpy.data.objects['Absets_cam'].data.lens=40
    bpy.context.scene.camera = bpy.data.objects['Absets_cam']
    #select everything and fit to the view
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.view3d.camera_to_view_selected()
    #zoom out a little
    bpy.data.objects['Absets_cam'].data.lens=35
def abset_scene():
    #adjust scene settings
    abscene=bpy.context.scene
    abscene.render.engine = 'CYCLES'
    abscene.cycles.caustics_reflective = False
    abscene.cycles.caustics_refractive = False
    abscene.cycles.glossy_bounces = 2
    abscene.cycles.diffuse_bounces = 2
    abscene.cycles.transmission_bounces = 6
    abscene.cycles.volume_bounces = 1
    abscene.cycles.min_bounces = 2
    abscene.cycles.transparent_min_bounces = 8
    abscene.cycles.transparent_max_bounces = 8
    abscene.render.resolution_y = 256
    abscene.render.resolution_x = 256
    abscene.render.pixel_aspect_x = 1
    abscene.render.pixel_aspect_y = 1
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.cycles.samples = 64
    bpy.context.scene.cycles.sample_clamp_direct = 5
    bpy.context.scene.cycles.sample_clamp_indirect = 2
    abset_env()
    abset_cam()

def abmake():
	"""
	to do:
		position camera to display the whole selected object
		render
		if single object, name it the same as the rendering
		if multiple objects, parent all to the active element, add a prefix
			(eg: "h_")to hide them from showing as independant renders later,
			append the parent's name as a prefix for the children's name to avoid
			collisions (eg:
						objects engine is active, gear1,gear2 are selected
						objects gear1 and gear2 share the same mesh data
						after abmake : engine, h_engine_gear1, h_engine_gear2
								!:;
	options:
		Blender Internal render
		high quality for a better/cleaner but longer render
		openGL render
	"""
	absActiveObj=abscene.objects.active
	bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, \
	location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, \
	False, False, False, False, False, False, False, False, False, False, False, False))
	bpy.ops.view3d.view_selected()

def abexport():
	"""
		save render result, name the image properly similar to the active asset (parent)
		pack it (or use external forder)
		export the active element (with all its children, if any)
		check if datablocks already exist (mesh, material, objects with same name)

		options:
			on existing datablock ?:
				rename
				overwrite
				cancel/skip
			apply modifiers (add function later)?
			export as single object?
			pack textures?
			select library (blend file) or create a new one


	"""
def abimport():
	"""
	to do
		read all libraries and load object images (see image with same name as
			a model, otherwise show default no preview image)
		a full interface with previews

	optional/future releases
		search
		tags(can be custom proprety that will be deleted from imported model?)
		object in multiple categories if needed ("car" can be toy and vehicle for example)
		material library, possibly in separate blend file

	options :
		as single object
		apply modifiers
		append or link
		textures:
			linked path relative to the plugin libraries
			saved in current working directory
			packed into blend file
		unit scale
	"""
