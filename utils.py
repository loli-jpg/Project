from yandex_music import Client
import os
from dotenv import load_dotenv
import logging

load_dotenv()

class YandexMusic:
    """����� ��� ������ � API ������.������."""
    
    def __init__(self):
        """�������������� ������ ������.������."""
        self.client = Client().init()

    def search(self, query, limit=5):
        """���� ����� � ������.������.
        
        Args:
            query (str): ��������� ������
            limit (int): ������������ ���������� �����������
            
        Returns:
            list[dict]: ������ ��������� ������ � �����������
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
    """���� ������ � ������.������.
    
    Args:
        query (str): ��������� ������
        limit (int): ������������ ���������� �����������
        
    Returns:
        list[dict]: ������ ��������� ������
    """
    yandex = YandexMusic()
    return yandex.search(query, limit)