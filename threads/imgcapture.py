import threading
from libraries.basler_cam import kamera
from libraries import zmqimage
from utils.Utils import get_trig_eth, give_trig_eth, connectPLC, save_log
import cv2

connectPLC()

basler1 = kamera(ip_address='192.168.0.235')
basler2 = kamera(ip_address='192.168.0.234')
basler3 = kamera(ip_address='192.168.0.123')

try:
    zmqo_images = zmqimage.ZmqConnect(connect_to="tcp://localhost:5678")
    save_log('Connected to processing script')
except:
    save_log('Unable to connect to processing script')
dummy = cv2.imread('/home/jetsonmapinai/Documents/AI Visual Inspection/7000.png')


class CamCapture(threading.Thread):
    def run(self):
        intd = 0
        while True:
            intd += 1
            save_log(f'Processing part number {intd}')
            print(f'{intd}')
            cam_status = get_trig_eth('MR15')
            cam_pos_T1_1 = get_trig_eth('MR5')
            cam_pos_T1_2 = get_trig_eth('MR6')
            cam_pos_D26_1 = get_trig_eth('MR9')
            cam_pos_D26_2 = get_trig_eth('MR10')
            cam_pos_D78_1 = get_trig_eth('MR11')
            cam_pos_D78_2 = get_trig_eth('MR12')
            end_part = get_trig_eth('MR301')
            if cam_status == '1':
                if cam_pos_T1_1 == '1' or cam_pos_D26_1 == '1' or cam_pos_D78_1 == '1':
                    cam1_img = basler1.ambilgambar()
                    cam2_img = basler2.ambilgambar()
                    cam3_img = basler3.ambilgambar()
                    give_trig_eth('MR300', '1')
                    msg = ['1', '_']
                    zmqo_images.imsend(msg, cam1_img)
                    zmqo_images.imsend(msg, cam2_img)
                    zmqo_images.imsend(msg, cam3_img)
                elif cam_pos_T1_2 == '1' or cam_pos_D26_2 == '1' or cam_pos_D78_2 == '1':
                    if cam_pos_T1_2 == '1':
                        msg = ['2', 'T1']
                    else:
                        msg = ['2', '_']
                    cam1_img = basler1.ambilgambar()
                    cam2_img = basler2.ambilgambar()
                    cam3_img = basler3.ambilgambar()
                    give_trig_eth('MR300', '1')
                    zmqo_images.imsend(msg, cam1_img)
                    zmqo_images.imsend(msg, cam2_img)
                    zmqo_images.imsend(msg, cam3_img)
                give_trig_eth('MR300', '0')
            elif cam_status == '0' and end_part == '1':

                zmqo_images.imsend(["Done", "Done"], dummy)
                zmqo_images.imsend(["Done", "Done"], dummy)
                zmqo_images.imsend(["Done", "Done"], dummy)
                print('SELESAI 1 PART')
