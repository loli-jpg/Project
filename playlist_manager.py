from database import Session, User, Playlist, Track

class PlaylistManager:
    """Класс для управления плейлистами и треками в базе данных."""
    
    @staticmethod
    def get_or_create_user(telegram_id):
        """Находит или создает пользователя по telegram_id.
        
        Args:
            telegram_id (int): ID пользователя в Telegram
            
        Returns:
            User: Объект пользователя
        """
        session = Session()
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            user = User(telegram_id=telegram_id)
            session.add(user)
            session.commit()
        session.close()
        return user

    @staticmethod
    def create_playlist(user_id, name):
        """Создает новый плейлист.
        
        Args:
            user_id (int): ID владельца плейлиста
            name (str): Название плейлиста
            
        Returns:
            Playlist: Созданный плейлист
        """
        session = Session()
        playlist = Playlist(name=name, user_id=user_id)
        session.add(playlist)
        session.commit()
        session.close()
        return playlist

    @staticmethod
    def get_user_playlists(user_id):
        """Возвращает все плейлисты пользователя.
        
        Args:
            user_id (int): ID пользователя
            
        Returns:
            list[Playlist]: Список плейлистов пользователя
        """
        session = Session()
        playlists = session.query(Playlist).filter_by(user_id=user_id).all()
        session.close()
        return playlists

    @staticmethod
    def get_playlist_tracks(playlist_id):
        """Возвращает все треки в плейлисте.
        
        Args:
            playlist_id (int): ID плейлиста
            
        Returns:
            list[Track]: Список треков в плейлисте
        """
        session = Session()
        tracks = session.query(Track).filter_by(playlist_id=playlist_id).all()
        session.close()
        return tracks

    @staticmethod
    def add_track_to_playlist(playlist_id, title, artist, url):
        """Добавляет трек в плейлист.
        
        Args:
            playlist_id (int): ID плейлиста
            title (str): Название трека
            artist (str): Исполнитель
            url (str): Ссылка на трек
            
        Returns:
            Track: Добавленный трек
        """
        session = Session()
        track = Track(title=title, artist=artist, url=url, playlist_id=playlist_id)
        session.add(track)
        session.commit()
        session.close()
        return track

    @staticmethod
    def remove_track_from_playlist(track_id):
        """Удаляет трек из плейлиста.
        
        Args:
            track_id (int): ID трека
            
        Returns:
            bool: True если трек был удален, False если не найден
        """
        session = Session()
        track = session.query(Track).filter_by(id=track_id).first()
        if track:
            session.delete(track)
            session.commit()
        session.close()
        return track is not None

    @staticmethod
    def get_playlist_by_id(playlist_id):
        """Возвращает плейлист по ID.
        
        Args:
            playlist_id (int): ID плейлиста
            
        Returns:
            Playlist: Найденный плейлист или None
        """
        session = Session()
        playlist = session.query(Playlist).filter_by(id=playlist_id).first()
        session.close()
        return playlist
