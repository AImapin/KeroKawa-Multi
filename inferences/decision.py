NG_dict = dict(
    Nama='Cacat',
    bbox=[1, 3],
    img=[],
    pengikut=0,
    bagian=0
)


def final_decision(bbox_list, NG_list, img_list):
    Final = [NG_dict]
    for i in range(len(NG_list)):  # pembagi section
        sl = NG_list[i]
        bl = bbox_list[i]
        il = img_list[i]
        ng_bagian = i + 1
        for j in range(len(sl)):  # pembagi frame
            sli = sl[j]
            bli = bl[j]
            imgNG = il[j]
            for k in range(len(sli)):  # pembagi ng type
                tipeNG = sli[k]
                if tipeNG == "OK":
                    continue
                try:
                    bbox_ng = [bli[k][1], bli[k][3], bli[k][0], bli[k][2]]
                except:
                    continue
                isNew = True
                for l in Final:
                    if tipeNG == l['Nama'] and ng_bagian == l['bagian']:
                        if bbox_ng[0] > l['bbox'][0] and bbox_ng[1] < l['bbox'][1]:
                            if bbox_ng[2] > l['bboxY'][0] and bbox_ng[3] < l['bboxY'][1]:  # kasus salah scratch
                                aR = (bbox_ng[1] - bbox_ng[0]) / (bbox_ng[3] - bbox_ng[2])  # aspect ratio
                                if aR > 5:
                                    l['pengikut'] = -2
                            l['pengikut'] += 1
                            isNew = False
                        elif bbox_ng[0] > l['bbox'][0] or bbox_ng[1] < l['bbox'][1]:  ### x,p,y,q
                            qx = (l['bbox'][1] - bbox_ng[0])
                            py = (bbox_ng[0] - l['bbox'][1])
                            union = abs(qx - py)
                            intersect = min(qx, py)
                            iou = intersect / union
                            if iou > 0.3:
                                l['pengikut'] += 1
                                isNew = False

                if isNew:
                    newNG = dict(
                        Nama=tipeNG,
                        bbox=[bbox_ng[0] - 80, bbox_ng[1] + 80],
                        bboxY=[bbox_ng[2] - 50, bbox_ng[3] + 50],
                        img=imgNG,
                        pengikut=1,
                        bagian=ng_bagian)
                    Final.append(newNG)

    list_type_NG = []
    list_pengikut_NG = []
    list_bagian_NG = []
    list_image_NG = []
    for it in Final:
        if (it['Nama'] == 'Kurokawa' and it['pengikut'] >= 4) or \
                (it['Nama'] == 'Scratch' and it['pengikut'] >= 5) or \
                (it['Nama'] == 'Keropos' and it['pengikut'] >= 2) or \
                (it['Nama'] == 'Dakon' and it['pengikut'] >= 2 and it['bagian'] != 4) or \
                (it['Nama'] == 'Dakon' and it['pengikut'] >= 3 and it['bagian'] == 4) or \
                (it['Nama'] == 'Ketsuniku' and it['pengikut'] >= 4) or \
                (it['Nama'] == 'Keropos_Casting' and it['pengikut'] >= 2) or \
                (it['Nama'] == 'Step' and it['pengikut'] >= 2) or \
                (it['Nama'] == 'PartingLine' and it['pengikut'] >= 2) or \
                (it['Nama'] == 'Karat' and it['pengikut'] >= 3):
            list_type_NG.append(it['Nama'])
            list_pengikut_NG.append(it['pengikut'])
            list_bagian_NG.append(it['bagian'])
            list_image_NG.append(it['img'])
    return list_type_NG, list_pengikut_NG, list_bagian_NG, list_image_NG
