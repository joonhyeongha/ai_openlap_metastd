import json
import os
import copy

import jsonmerge

import pandas

def procSoltlux(dataset): # 솔트룩스에서 제공한 데이터 처리기
    dir = './' + dataset + "/"

    files = os.listdir(dir)
    l = list()

    for file in files:
        if file.endswith(".json"):
            print(file)
            f = open(dir + file, encoding="utf8")
            j = json.load(f)       

            meta = j['metadata']
            #metaKeys = meta.keys()
            #print(metaKeys)
            speakers = j['speaker']

            for speaker in speakers:
                #print(speaker.keys())
                merge = jsonmerge.merge(meta, speaker)
                l.append(merge)

    df = pandas.json_normalize(l)
    df.to_excel( dataset + ".xlsx")

def procBokjiCallcenter():
    dir = './복지 분야 콜센터 상담/'

    l = list()
    for path, currentDirectory, files in os.walk(dir):
        for file in files:
            if file.endswith(".json"):
                print(file)
                f = open(path + '/' + file, "r", encoding="utf8")
                j = json.load(f)
                meta = j['info'][0]['metadata']
                assert(len(j['info']) == 1)
                audiopath = j['dialogs'][0]['audioPath']
                audiopathSplit = audiopath.split("\\")
                splitlen = len(audiopathSplit)
                id = audiopathSplit[splitlen-2]
                subid = audiopathSplit[splitlen-1].split('.')[0]
                meta['id'] = id
                meta['subid'] = subid
                l.append(meta)

    df = pandas.json_normalize(l)
    df.to_excel('복지 분야 콜센터 상담.xlsx')

# ㈜메트릭스리서치 에서 만든 데이터
def procMatrix(dataset):
    dir = './' + dataset + '/'

    alllist = list()
    for path, currentDirectory, files in os.walk(dir):
        for file in files:
            if file.endswith('.json'):
                print(file)
                f = open(path +'/'+ file, encoding = 'utf-8')
                j = json.load(f)
                ds = j['dataset']

                info = j['info'][0]
                infodict = copy.deepcopy(info)
                del infodict['annotations']
                #print(infodict)
                
                annotation = info['annotations']
                annodict = copy.deepcopy(annotation)
                del annodict['lines']
                del annodict['text']
                #print(annodict)

                infoanno = jsonmerge.merge(infodict, annodict)
                #print(infoanno)

                linelist = list()
                lines = annotation['lines']
                for line in lines:
                    speaker = line['speaker']
                    speaker['speaker-id'] = speaker.pop('id')

                    if not findSpeaker(linelist, speaker['speaker-id']):
                        infoannospeaker = jsonmerge.merge(infoanno,speaker)
                        linelist.append(infoannospeaker)

                print(linelist)
                alllist.extend(linelist)

    df = pandas.json_normalize(alllist)
    df.to_excel(dataset + '.xlsx')

def findSpeaker(linelist, speakerID):
    for line in linelist:
        if line['speaker-id'] == speakerID:
            return True
    return False

def procYongdo():
    procMatrix('용도별 목적대화')

def procJooje():
    procMatrix('주제별 텍스트 일상 대화')
    

def procGoseoHanja(datasetDir):
    l = list()
    for path, dir, files in os.walk(datasetDir):
        print(path)
        for file in files:
            if file.endswith('.json'):
                print(file)
                f = open(path + "/" + file, encoding='utf8')
                j = json.load(f)
                f.close()

                meta = copy.deepcopy(j)
                del meta['Image_Text_Coord']

                imgtexcoordList = j['Image_Text_Coord']
                for imgtexcoord in imgtexcoordList:
                    for coord in imgtexcoord:
                        metacoord = jsonmerge.merge(meta, coord)
                        l.append(metacoord)

    df = pandas.json_normalize(l)
    df.to_excel('고서 한자 인식 OCR 데이터.xlsx')

def procGeumYung(datasetDir):
    l = list()
    for path, dir, files in os.walk(datasetDir):
        for file in files:
            if file.endswith('.json'):
                print(file)
                f = open(path + "/" + file, encoding='utf8')
                j = json.load(f)
                f.close()

                meta = copy.deepcopy(j)
                del meta['images']
                del meta['annotations']

                imginfo = j['images'][0]

                for annotation in j['annotations']:
                    for polygon in annotation['polygons']:
                        metaimg = jsonmerge.merge(meta, imginfo)
                        metaimgpolygon = jsonmerge.merge(metaimg, polygon)
                        l.append(metaimgpolygon)

    df = pandas.json_normalize(l)
    df.to_excel('금융업 특화 문서 OCR.xlsx')

def procGisul(datasetDir):
    l = list()

    for path, dir, files in os.walk(datasetDir):
        for file in files:
            if file.endswith('.json'):
                print(file)
                f = open(path + "/" + file, encoding='utf8')
                j = json.load(f)
                f.close()

                meta = j['data']

                for datum in meta:
                    l.append(datum)

    df = pandas.json_normalize(l)
    df.to_excel('기술과학 분야 한영 번역 병렬 말뭉치 데이터.xlsx')

def procDaguk(datasetDir):
    l = list()

    for path,dir,files in os.walk(datasetDir):
        for file in files:
            if file.endswith('.json'):
                print(file)
                f = open(path + '/' + file, encoding = 'utf8')
                j = json.load(f)
                f.close()

                for item in j:
                    l.append(item)

    df = pandas.json_normalize(l)
    df.to_excel('다국어 구어체 번역 병렬 말뭉치.xlsx')

def procDaeyong(datasetDir):
    l = list()

    for path,dir,files in os.walk(datasetDir):
        for file in files:
            if file.endswith('.json'):
                print(file)
                f = open(path + '/' + file, encoding = 'utf8')
                j = json.load(f)
                f.close()

                anno = j['Annotation']
                data = j['Dataset']
                img = j['Images']

                annodataimg = jsonmerge.merge((jsonmerge.merge(anno,data)), img)

                for bbox in j['bbox']:
                    annodataimgbbox = jsonmerge.merge(annodataimg, bbox)
                    l.append(annodataimgbbox)

    df = pandas.json_normalize(l)
    df.to_excel('대용량 손글씨 OCR 데이터.xlsx')   

def procBangsongTranslate(datasetDir):
    l = list()

    for path,dir,files in os.walk(datasetDir):
        for file in files:
            if file.endswith('.json'):
                print(file)
                f = open(path + '/' + file, encoding = 'utf8')
                j = json.load(f)
                f.close()

                for item in j['data']:
                    l.append(item)

    df = pandas.json_normalize(l)
    df.to_excel('방송 콘텐츠 한-중, 한-일 번역 병렬 말뭉치 데이터.xlsx')

def procSusik(datasetDir):
    l = list()

    for path,dir,files in os.walk(datasetDir):
        for file in files:
            if file.endswith('.json'):
                print(file)
                f = open(path + '/' + file, encoding = 'utf8')
                j = json.load(f)
                f.close()

                meta = copy.deepcopy(j)
                del meta['segments']

                for segment in j['segments']:
                    metasegment = jsonmerge.merge(meta, segment)
                    l.append(metasegment)


    df = pandas.json_normalize(l)
    df.to_excel('수식, 도형, 낙서기호 OCR.xlsx')

def procYetHangeul(datasetDir):
    l = list()

    for path,dir,files in os.walk(datasetDir):
        for file in files:
            if file.endswith('.json'):
                print(file)
                f = open(path + '/' + file, encoding = 'utf-8-sig')
                j = json.load(f)
                f.close()

                meta = copy.deepcopy(j)
                del meta['Text_Coord']

                for textcoord in j['Text_Coord']:
                    metatextcoord = jsonmerge.merge(meta, textcoord)
                    l.append(metatextcoord)


    df = pandas.json_normalize(l)
    df.to_excel('옛한글 문자인식(OCR) 인공지능 학습용 데이터.xlsx')    

def procWoonjeon(datasetDir):
    l = list()

    for path,dir,files in os.walk(datasetDir):
        for file in files:
            if file.endswith('.json'):
                print(file)
                f = open(path + '/' + file, encoding = 'utf-8-sig')
                j = json.load(f)
                f.close()

                meta = j['metadata']
                sceneinfo = j['scene_info']
                occupantinfo = j['occupant_info'][0]
                scene = j['scene']

                metasceneinfo = jsonmerge.merge(meta, sceneinfo)

                metasceneinfooccupantinfo = jsonmerge.merge(metasceneinfo, occupantinfo)

                for data in scene['data']:
                    dataoccupant = jsonmerge.merge(data, data['occupant'][0])
                    del dataoccupant['occupant']

                    metasceneinfooccupantinfodata = jsonmerge.merge(metasceneinfooccupantinfo, dataoccupant)
                    l.append(metasceneinfooccupantinfodata)

    df = pandas.json_normalize(l)
    df.to_excel('운전자 및 탑승자 상태 및 이상행동 모니터링.xlsx')

def procPackagingOCR(datasetDir):
    l = list()

    for path,dir,files in os.walk(datasetDir):
        for file in files:
            if file.endswith('.json'):
                print(file)
                f = open(path + '/' + file, encoding = 'utf-8-sig')
                j = json.load(f)
                f.close()

                meta = copy.deepcopy(j)
                meta = jsonmerge.merge(meta, meta['images'][0])
                del meta['images']
                del meta['annotations']

                annotation = j['annotations'][0]

                for i in range (0, len(annotation['polygons'])):
                    poly = annotation['polygons'][i]
                    bbox = annotation['bbox'][i]

                    polybbox = jsonmerge.merge(poly, bbox)
                    metapolybbox = jsonmerge.merge(meta, polybbox)

                    l.append(metapolybbox)

    df = pandas.json_normalize(l)
    df.to_excel('의약품, 화장품 패키징 OCR.xlsx')   

def procIlsangEngKor(datasetDir):
    l = list()

    for path, dir, files in os.walk(datasetDir):
        for file in files:
            if file.endswith('.json'):
                print(file)
                f = open(path + "/" + file, encoding='utf8')
                j = json.load(f)
                f.close()

                meta = j['data']

                for datum in meta:
                    l.append(datum)

    df = pandas.json_normalize(l)
    df.to_excel('일상생활 및 구어체 한-영 번역 병렬 말뭉치 데이터.xlsx')    

def procIlsangChJpKor(datasetDir):
    l = list()

    for path, dir, files in os.walk(datasetDir):
        for file in files:
            if file.endswith('.json'):
                print(file)
                f = open(path + "/" + file, encoding='utf8')
                j = json.load(f)
                f.close()

                for datum in j:
                    l.append(datum)

    df = pandas.json_normalize(l)
    df.to_excel('일상생활 및 구어체 한-중, 한-일 번역 병렬 말뭉치.xlsx')    


def procJeonmoon(datasetDir):
    l = list()

    for path, dir, files in os.walk(datasetDir):
        for file in files:
            if file.endswith('.json'):
                print(file)
                f = open(path + "/" + file, encoding='utf8')
                j = json.load(f)
                f.close()

                meta = j['data']

                for datum in meta:
                    l.append(datum)

    df = pandas.json_normalize(l)
    df.to_excel('전문분야 영-한·중-한 번역 말뭉치 (식품).xlsx')    

def procCharyang(datasetDir):
    l = list()

    for path,dir,files in os.walk(datasetDir):
        for file in files:
            if file.endswith('.json'):
                print(file)
                f = open(path + '/' + file, encoding = 'utf-8-sig')
                j = json.load(f)
                f.close()

                meta = j['metadata']
                sceneinfo = j['scene_info']
                occupantinfo = j['occupant_info']
                scene = j['scene']

                metasceneinfo = jsonmerge.merge(meta, sceneinfo)

                metasceneinfooccupantinfo = jsonmerge.merge(metasceneinfo, occupantinfo)

                for data in scene['data']:
                    datautterance = jsonmerge.merge(data, data['utterance_info'])
                    del datautterance['utterance_info']

                    metasceneinfooccupantinfodata = jsonmerge.merge(metasceneinfooccupantinfo, datautterance)
                    l.append(metasceneinfooccupantinfodata)

    df = pandas.json_normalize(l)
    df.to_excel('차량 내 인터페이스 개선을 위한 멀티모달 데이터.xlsx')  

if __name__ == "__main__":
    print()
    #procSoltlux('방송 콘텐츠 대화체 음성인식')
    #procSoltlux('주요 영역별 회의 음성인식')
    #procBokjiCallcenter()      
    #procYongdo()     
    #procJooje() 
    #procGoseoHanja('E:\\[aihub2]\\고서 한자 인식 OCR 데이터')
    #procGeumYung('E:\\[aihub2]\\금융업 특화 문서 OCR')
    #procGisul('E:\\[aihub2]\\기술과학 분야 한영 번역 병렬 말뭉치 데이터')
    #procDaguk('E:\\[aihub2]\\다국어 구어체 번역 병렬 말뭉치')
    #procDaeyong('E:\\[aihub2]\\대용량 손글씨 OCR 데이터')
    #procBangsongTranslate('E:\\[aihub2]\\방송 콘텐츠 한-중, 한-일 번역 병렬 말뭉치 데이터')
    #procSusik('E:\\[aihub2]\\수식, 도형, 낙서기호 OCR (Formula, Shape, Scribble Symbol OCR)')
    #procYetHangeul('E:\\[aihub2]\\옛한글 문자인식(OCR) 인공지능 학습용 데이터')
    #procWoonjeon('E:\\[aihub2]\\운전자 및 탑승자 상태 및 이상행동 모니터링')
    #procPackagingOCR('E:\\[aihub2]\\의약품, 화장품 패키징 OCR')
    #procIlsangEngKor('E:\\[aihub2]\\일상생활 및 구어체 한-영 번역 병렬 말뭉치 데이터')
    #procIlsangChJpKor('E:\\[aihub2]\\일상생활 및 구어체 한-중, 한-일 번역 병렬 말뭉치')
    #procJeonmoon('E:\\[aihub2]\\전문분야 영-한·중-한 번역 말뭉치 (식품)')
    procCharyang('E:\[aihub2]\차량 내 인터페이스 개선을 위한 멀티모달 데이터')
