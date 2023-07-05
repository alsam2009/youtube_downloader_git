"""
COMMENT:
Программа для скачивания видео с Youtube. Скачивает одиночное видео, все видео из плейлиста, пакетное скачивание видео по ссылкам, все видео на канале со ссылками в файл csv

Ссылка на документацию pytube:
https://pytube.io/en/latest/user/install.html

Интересное решение по скачиванию видео: https://www.geeksforgeeks.org/pytube-python-library-download-youtube-videos/
 + GUI: https://www.geeksforgeeks.org/create-gui-for-downloading-youtube-video-using-python/
"""


from pytube import YouTube
from pytube import Playlist
from pytube.cli import on_progress

import http.client as http
import datetime
import os

from Youtube_videos_channel import channel_parser

http.HTTPConnection._http_vsn = 10
http.HTTPConnection._http_vsn_str = 'HTTP/1.0'

"""
COMMENT:
если хочешь чтобы 'прогресс' отображался быстрее, поменяй множитель у чанка: меньший множитель => больше отображения 'прогресс': *10 или *1. Комментирование строки => отображение по дефолту
pytube.request.default_range_size = 1048576*10    # this is for chunck size, 1MB * n size

Возвращает все видео и аудио потоки возможные к скачиванию, в двух вариантах progressive & adaptive (новая фича YTube, без аудио потока. Аудиопоток скачивается отдельно и затем нужно его совеместить в видео редакторе)
print(yt.streams)

Отфильтовать варианты с аудио потоком в одном файле:
print(yt.streams.filter(progressive=True))

Отфильтровать только файлы в формате mp4:
  yt.streams.filter(file_extension='mp4')

Получить itag аудио дорожки:
stream = yt.streams.get_audio_only()
print(stream)

Скачивание выбранного файла по itag 22 (tag="22" mime_type="video/mp4" res="720p" fps="30fps"):
stream = yt.streams.get_by_itag(22)
stream.download()

YouTube video stream format codes:
https://gist.github.com/sidneys/7095afe4da4ae58694d128b1034e01e2

"""


def link_save(save_path, link):
    # print(save_path)
    file_path = save_path+'playlist_url.txt'
    with open(f'{file_path}', 'w') as file:
        file.write(link)


def single_video_download(link, save_path, flag=0):
    # Счетчик ошибок
    count_error = 0
    accept_file_size = 'n'
    try:
        # COMMENT: Создание объекта Youtube для скачивание одного файла по ссылке
        yt = YouTube(link, on_progress_callback=on_progress)
        stream = yt.streams.get_by_itag(22)
        print(
            f'\ntitle: {yt.title} \nauthor: {yt.author}\nsize: {round(stream.filesize/(1024**2))} MB \nduration: {round(yt.length/60)} min')
        if flag == 0:
            accept_file_size = input('Download? (y|n): ')
        if accept_file_size == 'y' or flag == 1:
            print(f'\nDownloading...Be patiens...')
            filename = f'{yt.author.split(": ")[0].split("| ")[0]} {stream.default_filename}'
            # stream.configure_progress_bar(show=True)
            stream.download(save_path, filename=filename,
                            timeout=2000, max_retries=3)
    except Exception as e:
        print(
            f'\nThe file couldn\'t be download. Try it next time...\nError: {e}')
        count_error += 1
        return count_error
    return count_error


def playlist_download(link, save_path):
    count_error = 0
    try:
        #  Создание объекта PlayList для скачивания всех видео из ПЛЕЙЛИСТА
        pl = Playlist(link)
        for count, video in enumerate(pl.videos, 1):
            print(
                f'\nDownloading {count} from {len(pl.videos)} files...Be patiens...')
            save_path_playlist = save_path + \
                video.author.split(": ")[0].split("| ")[0]+" YOUTUBE "+pl.title+'\\'
            video.register_on_progress_callback(on_progress)
            stream = video.streams.get_by_itag(22)
            print(
                f'{video.title}\nsize: {round(stream.filesize/(1024**2))} MB\nduration: {round(video.length/60)} min')
            filename = f'[{count}] {stream.default_filename}'
            # stream.configure_progress_bar(show=True)

            stream.download(save_path_playlist, filename=filename, timeout=2000, max_retries=3)
            count += 1
            print()
        link_save(save_path_playlist, link)
    except Exception as e:
        count_error += 1
        print(
            f'\nThe file couldn\'t be download. Try it next time... Error: {e}')
        return count_error
    return count_error


def get_channel_url(link) -> None:
    try:
        yt = YouTube(link)
        channel_url = yt.channel_url
        print(channel_url)
    except Exception as e:
        print(f'URL is wrong... Error: {e}')


def get_playlist_link_from_single_video():
    link = input('Copy and paste your YouTube URL here: ')
    """
        This function supports only the following patterns:

    - :samp:`https://youtube.com/playlist?list={playlist_id}`
    - :samp:`https://youtube.com/watch?v={video_id}&list={playlist_id}`

       """
    try:
        pld = Playlist(link)
        print(f'\nplaylist : {pld.title}\nURL: {pld.playlist_url}')
    except Exception as e:
        print(f'URL is wrong... Error: {e}')


def get_link_start():
    link = input('Copy and paste your YouTube URL here: ')
    start = datetime.datetime.now()
    return link, start

# function for bach downloading


def get_video_urls():
    urls = []
    if os.stat('batch_download.txt').st_size != 0:
        with open('batch_download.txt', 'r') as f:
            for line in f:
                urls.append(line.rstrip('\n'))
    return urls


def get_end(start, count_error=0):
    end = datetime.datetime.now()
    print(
        f"\nDone!\n{count_error} err occured in process of downloading. Check it!\nWorking time (H:M:S): {str(end-start).split('.')[0]}")


def main():
    save_path = '.\\video\\'
    count_error_all = 0
    while True:
        desire_user = input(
            '\nPress key:\n[1] Single video\n[2] Playlist\n[3] Playlist url from single video\n[4] All videos on channel => csv file\n[5] URL channel\n[6] Batch dowload videos\n[7] Exit\n')

        match desire_user:
            case "1":
                link, start = get_link_start()
                count_error = single_video_download(link, save_path)
                get_end(start, count_error)
            case "2":
                link, start = get_link_start()
                count_error = playlist_download(link, save_path)
                get_end(start, count_error)
            case "3":
                get_playlist_link_from_single_video()
            case "4":
                start, _, count_error = channel_parser()
                get_end(start, count_error)
            case "5":
                link, _ = get_link_start()
                get_channel_url(link)
            case "6":
                links = get_video_urls()
                if links != []:
                    start = datetime.datetime.now()
                    bach_flag = 1
                    for link in links:
                        count_error = single_video_download(
                            link, save_path, bach_flag)
                        count_error_all += count_error
                    get_end(start, count_error_all)
                else:
                    print('Source is emty! Add links to bach_download.txt')
            case "7":
                print('Goodbye!')
                break
            case _: print("\nYour input is wrong! Try again...")


if __name__ == "__main__":
    welcom = "*** YOUTUBE DOWNLOADER ***"
    print(f'\n{welcom}\n{"_"*len(welcom)}')
    start = main()
