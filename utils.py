from yandex_music import Client
import os
from dotenv import load_dotenv
import logging

load_dotenv()

class YandexMusic:
    """Класс для работы с API Яндекс.Музыки."""
    
    def __init__(self):
        """Инициализирует клиент Яндекс.Музыки."""
        self.client = Client().init()

    def search(self, query, limit=5):
        """Ищет треки в Яндекс.Музыке.
        
        Args:
            query (str): Поисковый запрос
            limit (int): Максимальное количество результатов
            
        Returns:
            list[dict]: Список найденных треков с информацией
        """
        try:
            search_result = self.client.search(query, type_='track')
            tracks = []
            for track in search_result.tracks.results[:limit]:
                artists = ', '.join([artist.name for artist in track.artists])
                tracks.append({
                    'title': track.title,
                    'artist': artists,
                    'url': f"https://music.yandex.ru/track/{track.id}",
                    'platform': 'yandex'
                })
            return tracks
        except Exception as e:
            logging.error(f"Yandex Music error: {e}")
            return []

def search_music(query, limit=5):
    """Ищет музыку в Яндекс.Музыке.
    
    Args:
        query (str): Поисковый запрос
        limit (int): Максимальное количество результатов
        
    Returns:
        list[dict]: Список найденных треков
    """
    yandex = YandexMusic()
    return yandex.search(query, limit)