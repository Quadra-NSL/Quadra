import threading
import math

from rplidar import *

def rplidar2d_Array(minimize=False):
	'''
	This function takes readings from the lidar 
	and converts the readings into 30 degree intervals.
	
	Note:-
	====
	1. The value of the reading in the array is 20, if there is no scan in that region.
	2. Right now every alternate scan is detected, try out multi-threading.
	
	INPUT:-
	=====
	minimize- it reduces the array to a 3 length one(if true)
	Possibly an array
	OUTPUT:-
	======
	return an array of shape 3(if minimize), 12(else)
	'''
	global array
	lidar = RPLidar('/dev/ttyUSB0')
#	t1=time.time()
	array1=[20,20,20,20,20,20,20,20,20,20,20,20]
#	print("lidar_data")
	try:
		for i, scan in enumerate(lidar.iter_scans(max_buf_meas=500,min_len=2)):
			if i>7:break
			for j in scan:
				#print(j)
				m=int(j[1]/30)
				if m>11:m=0
				array1[m]=min(array1[m],j[2]/1000)
#				array[int(j[1]/30)]=j[2]/1000
#				print('scan:',int(j[1]/30),j[2]/1000)
		for i in range(0,len(array)):
			if array[i]!=array1[i] and array1[i]!=20:
				array[i]=array1[i]
		print(array)
#		print(array1)
		if minimize:
			array=minimize_Array(array)
		lidar.stop()
#		return array
	except:
		pass
#		if minimize:
#			return array[:3],0
#		else:
#			return array,0
		
		
def stop_lidar():
	global lidar		
	lidar.stop()
	lidar.stop_motor()
	lidar.disconnect()


def minimize_Array(array):
	if array[0]==20:
		front=min(array[0],array[-1])
	else:
		front=array[0]
	if array[2]==20:
		left=min(array[1],array[2])
	else:
		left=array[2]
	if array[-4]==20:
		right=min(array[-4],array[-3])
	else:
		right=array[-4]
	return [left,front,right]

def bendy_ruler():
	global array
	rplidar2d_Array()
	print("array:",array)
	p=math.pi/180
	m1,m2=math.cos(15*p),math.cos(45*p)
	value=(m1*array[0]+m2*array[1]-m2*array[4]-m1*array[5])/max(array[0],array[1],array[4],array[5])
	array_mal=minimize_Array(array)
	return array_mal,value
	

lidar = RPLidar('/dev/ttyUSB0')
array=[20,20,20,20,20,20,20,20,20,20,20,20]

def print_chacha():
#	print("chacha")
	time.sleep(0.5)
'''
if __name__=="__main__":
	while True:
		t1=threading.Thread(target=rplidar2d_Array(),name='lidar_macha')
		t2=threading.Thread(target=print_chacha(),name='printer')
		t1.start()
		t2.start()
	
	#	print(t1)
#		print(array)
'''
