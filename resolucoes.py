formato = '.mp4'
resolucoes = []
resolucoes.append('320:180')
resolucoes.append('640:360')
resolucoes.append('832:480')
resolucoes.append('1280:720')
resolucoes.append('1920:1080')
resStr = []
resStr.append('320x180')
resStr.append('640x360')
resStr.append('720x480')
resStr.append('1280x720')
resStr.append('1920x1080')
codigo = 'arquivo_original'

for i in range(0, len(resolucoes)):
	print('ffmpeg -i '+codigo+formato+' -vf scale='+resolucoes[i]+' -c:a copy '+codigo+'_'+resStr[i]+formato)
