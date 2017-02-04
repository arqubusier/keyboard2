import Part

from FreeCAD import Base

KEY_DEPTH = 3
KEY_WIDTH = 14
KEY_LENGTH = 14
KEY_WIDTH_EXTRA = 1.5
KEY_LENGTH_EXTRA = 2.5
RIM_WIDTH = KEY_WIDTH + 2*KEY_WIDTH_EXTRA
RIM_LENGTH = KEY_LENGTH + 2*KEY_LENGTH_EXTRA
COLUMN_SPACING = 3


class KeyData:
	def __init__(self, rim, hole, front, back, side_l, side_r,
				 edge_tl, edge_tr, edge_tf, edge_tb,
				point_tfl, point_tfr, point_tbl, point_tbr):
		self.rim = rim
		self.hole = hole
		self.front = front
		self.back = back
		self.side_l = side_l
		self.side_r = side_r
		self.edge_tl = edge_tl
		self.edge_tr = edge_tr
		self.edge_tf = edge_tf
		self.edge_tb = edge_tb
		self.point_tfl = point_tfl
		self.point_tfr = point_tfr
		self.point_tbl = point_tbl
		self.point_tbr = point_tbr
		self.shapes = (rim,hole,front,back,side_l,side_r,
						edge_tl,edge_tr,edge_tf,edge_tb)

	def rotate(self, pos, axis, angle):
		for s in self.shapes:
			s.rotate(pos,axis,angle)

	def translate(self, vec):
		for s in self.shapes:
			s.translate(vec)


"""
	pos determines the lower left corner
"""
def key(pos, depth= 3, length_extra = KEY_LENGTH_EXTRA, width_extra = KEY_WIDTH_EXTRA, length = KEY_LENGTH, width = KEY_WIDTH):
	
	outer = Part.makeBox(length + 2*length_extra, width+2*width_extra, depth, Base.Vector(0,0,0))
	inner = Part.makeBox(length, width,depth,Base.Vector(length_extra, width_extra, 0))
	rim = outer.cut(inner)	

	w = width+2*width_extra
	l = length+2*length_extra
	d=depth
	back = Part.makePolygon(
		[Base.Vector(0,0,0), Base.Vector(l,0,0), Base.Vector(l,0,d), 
		 Base.Vector(0,0,d), Base.Vector(0,0,0)])
	front = Part.makePolygon(
		[Base.Vector(0,w,0), Base.Vector(l,w,0), Base.Vector(l,w,d), 
		 Base.Vector(0,w,d), Base.Vector(0,w,0)])
	side_l = Part.makePolygon(
		[Base.Vector(0,0,0), Base.Vector(0,w,0), Base.Vector(0,w,d), 
		 Base.Vector(0,0,d), Base.Vector(0,0,0)])
	side_r = Part.makePolygon(
		[Base.Vector(l,0,0), Base.Vector(l,w,0), Base.Vector(l,w,d), 
		 Base.Vector(l,0,d), Base.Vector(l,0,0)])
	edge_tl = Part.makeLine((0,0,d),(0,w,d))
	edge_tr = Part.makeLine((l,0,d),(l,w,d))
	edge_tf = Part.makeLine((0,w,d),(l,w,d))
	edge_tb = Part.makeLine((0,0,d),(l,0,d))
	point_tfl = Base.Vector(0,w,d)
	point_tfr = Base.Vector(l,w,d)
	point_tbl = Base.Vector(0,w,d)
	point_tbr = Base.Vector(l,w,d)
	
	k = KeyData(rim, inner, front, back, side_l, side_r,
				edge_tl, edge_tr, edge_tf, edge_tb,
				point_tfl, point_tfr, point_tbl, point_tbr)
	k.translate(pos)
	return k


class Column:
	def __init__(self, keys, lofts):
		self.keys = keys
		self.lofts = lofts
		#self.edge_l0_left = edge_l0_left
		#self.edge_l0_right = edge_l0_right
		#self.edge_l1_left = edge_l1_left
		#self.edge_l1_right = edge_l1_right


	def show(self):
		for key in self.keys:
			Part.show(key.rim)
			Part.show(key.edge_tf)
			Part.show(key.edge_tb)
			Part.show(key.edge_tl)
			Part.show(key.edge_tr)
			Part.show(key.side_l)
			Part.show(key.side_r)
			Part.show(key.front)
			Part.show(key.back)

		for loft in self.lofts:
			Part.show(loft)

"""
"""
def col(pos, angle=12):
	#position keys	
	k0 = key(Base.Vector(0,-RIM_WIDTH,0))
	k1 = key(Base.Vector(0,0,0))
	k2 = key(Base.Vector(0, RIM_WIDTH, 0))
	k0.rotate(Base.Vector(0,0,KEY_DEPTH), Base.Vector(1,0,0), -angle)
	k0.translate(Base.Vector(0,-COLUMN_SPACING,0))
	k0.rotate(Base.Vector(0,0,KEY_DEPTH), Base.Vector(1,0,0), -angle)
	k2 = key(Base.Vector(0, RIM_WIDTH, 0))
	k2.rotate(Base.Vector(0,RIM_WIDTH,KEY_DEPTH), Base.Vector(1,0,0), angle)
	k2.translate(Base.Vector(0,COLUMN_SPACING,0))
	k2.rotate(Base.Vector(0,RIM_WIDTH,KEY_DEPTH), Base.Vector(1,0,0), angle)
	#fill in spacing
	l1 = Part.makeLoft([k0.front,k1.back])
	l2 = Part.makeLoft([k1.front,k2.back])

	return Column((k0,k1,k2), (l1,l2))

col1 = col(Base.Vector(0,10,0))
col1.show()