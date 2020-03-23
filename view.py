# file: view.py
# author: Luc Yuki Marrie
# date: 2/23/2015
# class: CS251

import numpy as np
import math


# Class that holds the current viewing parameters and can
## build a view transformation matrix [VTM] based on the parameters.
class View:


	# View class constructor method
	def __init__(self):
		
		self.vrp = np.matrix([0.5, 0.5, 1])
		self.vpn = np.matrix([0, 0, -1])
		self.vup = np.matrix([0, 1, 0])
		self.u = np.matrix([1, 0, 0])
		self.extent = np.matrix([1, 1, 1])
		self.screen = np.matrix([400, 400])
		self.offset = np.matrix([20, 20])		


	# method that that uses the current viewing parameters to return a view matrix
	def build(self):
	
		vtm = np.identity( 4, float )
		t1 = np.matrix( [[1, 0, 0, -self.vrp[0, 0]],
                    [0, 1, 0, -self.vrp[0, 1]],
                    [0, 0, 1, -self.vrp[0, 2]],
                    [0, 0, 0, 1] ] )

		vtm = t1 * vtm
		tu = np.cross(self.vup, self.vpn)
		tvup = np.cross(self.vpn, tu)
		tvpn = self.vpn
		tu = self.normalize(tu)
		tvup = self.normalize(tvup)
		tvpn = self.normalize(tvpn)
		self.u = tu
		self.vup = tvup
		self.vpn = tvpn
		
		# align the axes with rotation matrix
		
		r1 = np.matrix( [[ tu[0, 0], tu[0, 1], tu[0, 2], 0.0 ],
                    [ tvup[0, 0], tvup[0, 1], tvup[0, 2], 0.0 ],
                    [ tvpn[0, 0], tvpn[0, 1], tvpn[0, 2], 0.0 ],
                    [ 0.0, 0.0, 0.0, 1.0 ] ] );

		vtm = r1 * vtm
		
		# translate the lower left corner of the view space to the origin
		
		tm = np.matrix([[1, 0, 0, 0.5 * self.extent[0, 0]],
			   			[0, 1, 0, 0.5 * self.extent[0, 1]],
			   			[0, 0, 1, 0],
			   			[0, 0, 0, 1]] );
		vtm = tm * vtm		
		
		# Use the extent and screen size values to scale to the screen
		
		s = np.matrix( [[-self.screen[0, 0] / self.extent[0,0], 0, 0, 0],
						 [0, -self.screen[0, 1] / self.extent[0, 1], 0, 0],
						 [0, 0, 1 / self.extent[0, 2], 0],
						 [0, 0, 0, 1]] );
		vtm = s * vtm
		
		# translate the lower left corner to the origin and add the view offset,
		## which gives a little buffer around the top and left edges of the window.
				
		tm2 = np.matrix( [[1, 0, 0, self.screen[0, 0] + self.offset[0, 0]],
						  [0, 1, 0, self.screen[0, 1] + self.offset[0, 1]],
						  [0, 0, 1, 0],
						  [0, 0, 0, 1]] );
		
		vtm = tm2 * vtm
		
		return vtm
		
	# VRP accessor method
	def getVRP(self):
		return self.vrp	
	
	# VPN accessor method
	def getVPN(self):
		return self.vpn			
		
	# VUP accessor method
	def getVUP(self):
		return self.vup	
		
	# U accessor method	
	def getU(self):
		return self.u
		
	# extent accessor method
	def getExtent(self):
		return self.extent	

	# screen size accessor method
	def getScreen(self):
		return self.screen
	
	# VRP setter method	
	def setVRP(self, vector):
		self.vrp = vector
		
	# VPN setter method	
	def setVPN(self, vector):
		self.vpn = vector
		
	# VUP setter method	
	def setVUP(self, vector):
		self.vup = vector

	# U setter method	
	def setU(self, vector):
		self.u = vector

	# Extent setter method	
	def setExtent(self, extent):
		self.extent = extent
	
	# Screen setter method	
	def setScreen(self,vector):
		self.screen	= vector

	
	# Method that normalizes data
	def normalize(self, v):
		Length = math.sqrt( (v[0, 0]*v[0, 0]) + (v[0, 1]*v[0, 1]) + (v[0, 2]*v[0, 2]) )
		v[0, 0] = v[0, 0] / Length
		v[0, 1] = v[0, 1] / Length
		v[0, 2] = v[0, 2] / Length
		return v


# Make a translation matrix to move the point ( VRP + VPN * extent[Z] * 0.5 ) to the origin. Put it in t1.
# Make an axis alignment matrix Rxyz using u, vup and vpn.
# Make a rotation matrix about the Y axis by the VUP angle, put it in r1.
# Make a rotation matrix about the X axis by the U angle. Put it in r2.
# Make a translation matrix that has the opposite translation from step 1.
# Make a numpy matrix where the VRP is on the first row, with a 1 in the homogeneous coordinate,
	#  and u, vup, and vpn are the next three rows, with a 0 in the homogeneous coordinate.
# Execute the following: tvrc = (t2*Rxyz.T*r2*r1*Rxyz*t1*tvrc.T).T
# Then copy the values from tvrc back into the VPR, U, VUP, and VPN fields and normalize U, VUP, and VPN

	# Rotate VRC method
	def rotateVRC(self, VUP, U):

		# ( VRP + VPN * extent[Z] * 0.5 ) to the origin. Put it in t1.
		t1 = np.matrix([[1, 0, 0, - (self.vrp[0,0] + self.vpn[0,0] * self.extent[0,2] * 0.5)],
						[0, 1, 0, - (self.vrp[0,1] + self.vpn[0,1] * self.extent[0,2] * 0.5)],
						[0, 0, 1, - (self.vrp[0,2] + self.vpn[0,2] * self.extent[0,2] * 0.5)],
						[0, 0, 0, 1]])
						
		# Rxyz using u, vup and vpn
		Rxyz = np.matrix([[self.u[0,0], self.u[0,1], self.u[0,2], 0],
                         [self.vup[0,0], self.vup[0,1], self.vup[0,2], 0],
                         [self.vpn[0,0], self.vpn[0,1], self.vpn[0,2], 0],
                         [0, 0, 0, 1]])
                         
        # rotation about Y axis by the VUP angle, put it in r1.
		r1	= np.matrix([[math.cos(VUP), 0, math.sin(VUP), 0],
						 [0, 1, 0, 0],
						 [-math.sin(VUP), 0, math.cos(VUP), 0],
						 [0, 0, 0, 1]])
						 
		# rotation about x axis by the U angle, put it in r2.
		r2 = np.matrix([[1, 0, 0, 0],
						[0, math.cos(U), -math.sin(U), 0],
						[0, math.sin(U), math.cos(U), 0],
						[0, 0, 0, 1]])
						
		# make translation matrix that is opposite from step 1.
		t2 = np.matrix([[1, 0, 0, (self.vrp[0,0] + self.vpn[0,0] * self.extent[0,2] * 0.5)],
						[0, 1, 0, (self.vrp[0,1] + self.vpn[0,1] * self.extent[0,2] * 0.5)],
						[0, 0, 1, (self.vrp[0,2] + self.vpn[0,2] * self.extent[0,2] * 0.5)],
						[0, 0, 0, 1]])
		# make np matrix where VRP is on first row and 1 is homogenous coordinate
		# u vup and vpn are next three rows with 0 in the homogenous coordinate
		tvrc = np.matrix([[self.vrp[0,0], self.vrp[0,1], self.vrp[0,2], 1],
						   [self.u[0,0], self.u[0,1], self.u[0,2], 0],
						   [self.vup[0,0], self.vup[0,1], self.vup[0,2], 0],
						   [self.vpn[0,0], self.vpn[0,1], self.vpn[0,2], 0]])

		# Execute tvrc = (t2*Rxyz.T*r2*r1*Rxyz*t1*tvrc.T).T
		tvrc = (t2*Rxyz.T*r2*r1*Rxyz*t1*tvrc.T)
		
		# Then copy the values from tvrc back into the VPR, U, VUP, and VPN fields 
		# and normalize U, VUP, and VPN
		self.vrp = tvrc[(np.meshgrid([0, 1, 2], 0))]
		self.u = tvrc[(np.meshgrid([0, 1, 2], 1))]
		self.vup = tvrc[(np.meshgrid([0, 1, 2], 2))]
		self.vpn = tvrc[(np.meshgrid([0, 1, 2], 3))]
		self.u = self.normalize(self.u)
		self.vup = self.normalize(self.vup)
		self.vpn = self.normalize(self.vpn)

	# Makes a duplicate View object and returns it
	def clone(self):
		clone = View()
		clone.vrp = self.vrp.copy()
		clone.vpn = self.vpn.copy()
		clone.u = self.u.copy()
		clone.vup = self.vup.copy()
		clone.extent = self.extent.copy()
		clone.screen = self.screen						
		clone.offset = self.offset
		return clone
		
		
def main():
	v = View()
	c = v.clone()
	print "Printing matrix:"
	print "vrp :" + str(v.getVRP()) + "   u: " + str(v.getU()) + "    vup: " + str(v.getVUP())
	print v.build()
	print "vrp :" + str(v.getVRP()) + "   u: " + str(v.getU()) + "    vup: " + str(v.getVUP())
	print "Printing clone of view:"
	print c.build()


if __name__ == "__main__":	
	main()	

				