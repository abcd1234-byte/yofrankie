'''
Use this script when running into a wall with the "slip" property
either run allongside the wall or reflect off it.
'''
import GameLogic

from Mathutils import CrossVecs, Vector, Matrix, RotationMatrix, AngleBetweenVecs, DotVecs

def main(cont):
	own = cont.getOwner()
	
	sens_wall_ray = cont.getSensor('wall_ray')
	sens_wall_time = cont.getSensor('wall_run_time')
	actu_motion = cont.getActuator('wall_run_motion')
	
	if not sens_wall_time.isPositive():
		# We must turn off this actuator once the time limit sensor
		# is false, otherwise it will keep benig applied
		
		# This will happen when first touching the wall which is not needed
		# but there is no harm in it either.		
		# There is a small chance the time will run out but the ray will be hitting somthing.
		# so just to be sure, always remove motion when the wall timer is false.

		GameLogic.addActiveActuator( actu_motion, False )
		if not sens_wall_ray.isPositive():
			return
	
	# when to apply the rebound force from the wall and turn frankie
	# make sure its lower then the wall_run_time sensor maximum
	LIMIT_REBOUND_TIME = 0.25
	
	REBOUND_LINV = 1.0
	
	#if not sens_wall_ray.isPositive():
	#if 1:
	if not sens_wall_time.isPositive() and sens_wall_ray.isPositive():
		# Either initialize a rebound, of if the angle is low, just run paralelle to the wall
		wall_nor = Vector(sens_wall_ray.getHitNormal())
		wall_nor.z = 0.0
		
		own_neg_y = Vector(own.getAxisVect([0,-1,0]))
		own_neg_y.z = 0.0
		
		ang = AngleBetweenVecs(own_neg_y, wall_nor) 
		if ang > 22.5:
			cross = CrossVecs(wall_nor, own_neg_y)
			if cross.z > 0.0:
				paralelle_dir = wall_nor * RotationMatrix(-90, 3, 'z')	
			else:
				paralelle_dir = wall_nor * RotationMatrix(90, 3, 'z')	
			
			own.alignAxisToVect(paralelle_dir, 1, 0.1)
			return
		
		else:
			# Rebount! - we're running directly into it
			
			own.wall_run_timer = 0.0
			
			# Set the direction velocity, apply this later
			
			''' # Simple direct off wall, not that fun
			wall_nor = sens_wall_ray.getHitNormal()
			actu_motion.setLinearVelocity(wall_nor[0]*REBOUND_LINV, wall_nor[1]*REBOUND_LINV, 0.0, 0)
			'''
			
			# Nicer to reflect
			wall_nor.normalize()
			ref = own_neg_y.reflect(wall_nor)
			actu_motion.setLinearVelocity(ref[0]*REBOUND_LINV, ref[1]*REBOUND_LINV, 0.0, 0)
			
			actu_anim = cont.getActuator('run_wall')
			GameLogic.addActiveActuator( actu_anim, True )
		
	else:
		## We are not facing the wall anymore, just orient to the reflection vector
		# Apply rebound and face that direction
		if own.wall_run_timer > LIMIT_REBOUND_TIME:
			vel = actu_motion.getLinearVelocity()[0:3]
			own.alignAxisToVect(vel, 1, 0.2)
			GameLogic.addActiveActuator( actu_motion, True )
