
import csv
from datetime import datetime
import os
from pytube import YouTube
from pytube import Channel

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36',
    "accept": "*/*"
}

def make_progress_view(index, progress_view, len_channel, counter):
    if index < progress_view:
        return progress_view
    else:
        print(
            f'Обработано {index} видео из {len_channel} | {round(index*100/len_channel)} %')
        progress_view += counter
        return progress_view


def get_channel_info(channel_url):
    count_error = 0
    try:
        c = Channel(channel_url)
        channel = c.channel_name.split(":")[0]
        get_videos_channel_dir(channel)
        len_channel = len(c.videos)
        progress_view = len_channel // 10
        counter = progress_view
        # for index, video in enumerate(c.videos[205:]):
        # for video in c.videos[205:]:
        #     print(video.title)
        try:
            for index, video in enumerate(c.videos):
                title = video.title
                url = c.video_urls[index]
                duration = round(video.length/60)
                pub_date = video.publish_date
                views_video = video.views

                with open(f"2. Channels/{channel}/{channel}_all_video.csv", "a", newline='', encoding='utf-8') as f:
                    csv.writer(f, delimiter=';').writerow(
                        (
                            title,
                            url,
                            duration,
                            pub_date,
                            views_video
                        )
                    )

                if progress_view > 1:
                    progress_view = make_progress_view(
                        index, progress_view, len_channel, counter)
        except Exception as e:
            count_error += 1
            print(e)
    except Exception as e:
        count_error += 1
        print(e)
        return count_error
    return count_error


def get_videos_channel_dir(channel):
    if not os.path.exists(f'2. Channels\{channel}'):
        os.mkdir(f'2. Channels\{channel}')


def get_channel_url(link):
    try:
        yt = YouTube(link)
        channel_url = yt.channel_url
        return channel_url
    except Exception as e:
        print(e)


def channel_parser():
    channel_url = input("Copy and paste your YouTube Channel's URL here: ")
    start = datetime.now()
    count_error = get_channel_info(channel_url)
    end = datetime.now()
    return start, end, count_error
    # channel_url = "https://www.youtube.com/@PythonToday"
    # link = 'https://www.youtube.com/watch?v=sFrGDeMbxE4'
    # channel_url = get_channel_url(link)
    # print(channel_url)


if __name__ == '__main__':
    start, end, count_error = channel_parser()
    print(
        f"\nDone!\n{count_error} err occured in process of downloading. Check it!\nWorking time (H:M:S): {str(end-start).split('.')[0]}")