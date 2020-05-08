from bottle import route, run, HTTPError, request
import re
import album


@route("/albums/<artist>")
def albums(artist):
	albums_list = album.find(artist)
	if not albums_list:
		message = f"Альбомов {artist} не найдено"
		result = HTTPError(404, message)
	else: 
		album_names = [album.album for album in albums_list]
		result = f"Список альбомов {artist}. Всего {len(albums_list)} шт.<br><br>"
		result+='<br>'.join(album_names)
	return result

@route("/albums", method='POST')
def create_album():
	# создаем словарь для обработки POST запросов
	album_data = {
		"artist": request.forms.get("artist"),
		"genre": request.forms.get("genre"),
		"year": int(request.forms.get("year")),
		"album": request.forms.get("album"),
	}
	# валидатор запросов
	for item in album_data:
		if not album_data[item]:
			return f"Упс... Вы не ввели '{item}' "

	match = re.match(r"[1-2][0-9]{3}", str(album_data['year']))
	if not match:
		return f"Неверно указан год"


	# переводим словарь в экземпляр класса
	new_album = album.Album(**album_data)

	# записываем новый альбом 
	if album.save(new_album): 
		result = f"Альбом {album_data['album']} артиста {album_data['artist']} сохранен"
	else:
		message = f"Альбом {album_data['album']} в исполнении {album_data['artist']} уже есть в базе"
		result = HTTPError(409, message)
	return result



if __name__ == '__main__':
	run(server='tornado', host='localhost', port=8080, debug=True) 