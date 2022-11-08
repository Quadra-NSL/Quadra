import websockets
import json
import asyncio
from rplidar_thread import *

async def run():
	global device
	uri = "ws://localhost:4778/control"
	data = {"command":{"mode":"rest"}}
	async with websockets.connect(uri) as websocket:
		while(True):
#			left,front,right=rplidar2d_Array()
			[left,front,right],value=bendy_ruler()
			print("lidar data:",left,front,right)
			if front<1.5 or left<1.5 or right<1.5:
				print("condition 1")
				xadd=min(left,right,2)*100
				xadd=90-(200-xadd)*90/200
				if front<0.85:front=-0.2
				else:front=0.2
				if left<1.5:
					data = {"command":{"mode":"walk","log":"disable","v_R":[front,0,0],"w_R":[0,0,-math.cos(xadd*math.pi/180)/5],"walk":{"step_height":1,"maximize_flight":False}}}
				else:
					data = {"command":{"mode":"walk","log":"disable","v_R":[front,0,0],"w_R":[0,0,math.cos(xadd*math.pi/180)/5],"walk":{"step_height":1,"maximize_flight":False}}}

			
			elif front<2:
				print("condition 2")
				data = {"command":{"mode":"rest"}}
			else:
				pass
				###BELOW IS FOR RC CONTROL
				'''
				print("condition 3")
				max_speed = device.getRCSpeedValue()
				# max_speed = max(((max_speed - 1000)/1000)-0.72,0.05)
				if max_speed> 1900:
					max_speed = 1
				elif max_speed>1400:
					max_speed = 0.5
				else:
					max_speed = 0.1
				max_speed = 0.3 # added just becz throttle not working
				if (device.mode == "MANUAL"):
					side,rot,forward = device.getRCValues()
					if (1400<side<1600) and (1400<rot<1600) and (1400<forward<1600):
						data = {"command":{"mode":"rest"}}
					else:
						side	= (side - 1500)/500
						rot		= (rot - 1500)/500
						forward = ((forward-1500)/500)*max_speed #min(((forward - 1500)/500),max_speed)
						data = {"command":{"mode":"walk","log":"disable","v_R":[forward,side,0],"w_R":[0,0,rot+value],"walk":{"step_height":1,"maximize_flight":False}}}
				elif (device.mode == "ACRO"):
					data = {"command":{"mode":"zero_velocity"}}
					if (device.getRCPowerOff()>1500):
						data = {"command":{"mode":"stopped"}}
				elif (device.mode == "AUTO" or device.mode == "GUIDED" or device.mode=="RTL"):
					servo1,servo2 = device.getPWMValue()
					print(servo1,servo2)
					f_val = ((servo2 - 1500)/500)*0.8
					r_val = ((servo1 - 1500)/500)*5
					if (1400<servo1<1600) and (1400<servo2<1600):
						data = {"command":{"mode":"rest"}}
					else:
						data = {"command":{"mode":"walk","log":"disable","v_R":[f_val,0,0],"w_R":[0,0,r_val+value],"walk":{"step_height":1,"maximize_flight":False}}}
				else:
					data = {"command":{"mode":"rest"}}
					# print(servo1,servo2)
			'''
#			print(data)
#			print(device.mode)
#			print(device.vehicle._velocity)
			await websocket.send(json.dumps(data))
			data1 = await websocket.recv()

			time.sleep(0.2)
			# asyncio.sleep(0.2)
		
		
if __name__=="__main__":
	t1=threading.Thread(target=rplidar2d_Array(),name='lidar_macha')
	t1.start()
	
asyncio.get_event_loop().run_until_complete(run())
