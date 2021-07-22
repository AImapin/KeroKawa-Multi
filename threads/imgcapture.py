import threading
import time
from libraries.basler_cam import kamera, get_images
from libraries import zmqimage
from utils.Utils import get_plc_data, change_plc_data, connectPLC, save_log

connectPLC()

basler1 = kamera(ip_address='192.168.0.235')
basler2 = kamera(ip_address='192.168.0.234')
basler3 = kamera(ip_address='192.168.0.123')

try:
    zmqo_images = zmqimage.ZmqConnect(connect_to="tcp://localhost:5678")
    save_log('Connected to processing script')
except:
    save_log('Unable to connect to processing script')
FLAG_PART = False
COUNTER = 0
msg = ''
part_type = ''


class CamCapture(threading.Thread):
    def run(self):
        global FLAG_PART, COUNTER, msg, part_type
        while True:
            cam_status = get_plc_data('MR15')
            if cam_status == '1':
                if 0 <= COUNTER < 12:
                    time.sleep(0.25)
                    cam1_img = basler1.ambilgambar()
                    cam2_img = basler2.ambilgambar()
                    cam3_img = basler3.ambilgambar()
                    save_log(f'Done Capture Rotation sec1 no. {COUNTER}')
                    msg = ['1', '_']
                    zmqo_images.imsend(msg, cam1_img)
                    zmqo_images.imsend(msg, cam2_img)
                    zmqo_images.imsend(msg, cam3_img)
                    change_plc_data('MR300', '1')
                    COUNTER += 1
                else:
                    if COUNTER == 12:
                        cam_pos_T1_2 = get_plc_data('MR6')
                        if cam_pos_T1_2 == '1':
                            part_type = 'T1'
                            msg = ['2', 'T1']
                        else:
                            part_type = 'D78'
                            msg = ['2', 'D78']
                    time.sleep(0.25)
                    cam1_img = basler1.ambilgambar()
                    cam2_img = basler2.ambilgambar()
                    cam3_img = basler3.ambilgambar()
                    save_log(f'Done Capture Rotation sec2 no. {COUNTER - 12}')
                    zmqo_images.imsend(msg, cam1_img)
                    zmqo_images.imsend(msg, cam2_img)
                    zmqo_images.imsend(msg, cam3_img)
                    change_plc_data('MR300', '1')
                    FLAG_PART = True
                    COUNTER += 1
                time.sleep(0.05)
                change_plc_data('MR300', '0')
            elif cam_status == '0' and FLAG_PART:
                end_part = get_plc_data('MR301')
                if end_part == '1':
                    FLAG_PART = False
                    COUNTER = 0
                    zmqo_images.imsend(["Done", part_type], get_images())
                    zmqo_images.imsend(["Done", part_type], get_images())
                    zmqo_images.imsend(["Done", part_type], get_images())
                    save_log('FINISH Capture 1 PART')
                else:
                    if get_plc_data('MR1502') == '1':
                        COUNTER = 0
                    time.sleep(0.15)
            else:
                if get_plc_data('MR1502') == '1':
                    COUNTER = 0
                time.sleep(0.15)
