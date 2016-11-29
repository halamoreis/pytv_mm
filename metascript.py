import json
from pprint import pprint

formato = '.mp4'
codigo = 'nome_resolucao'

with open('log.json') as data_file:    
    data = json.load(data_file)

framesI = []

tam = len(data['frames'])

for i in range(0, tam):
	if data["frames"][i]["pict_type"] == 'I':
		framesI.append(i)

framesI.append(tam-1)
length = (len(framesI)-1)

for i in range(0, length):
	ini = data["frames"][framesI[i]]["pkt_pts_time"]
	fim = data["frames"][framesI[i+1]]["pkt_pts_time"]
	str = 'ffmpeg -i '+codigo+formato+' -ss ' + ini + ' -to ' + fim + ' -q:v 0 -acodec copy -vcodec h264 -acodec aac -strict -2 '+codigo+'_'+'%.3d' % (i,) + formato
	print(str)
