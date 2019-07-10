import argparse

def construct_arguments():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the video file")
    ap.add_argument("-a", "--min-area", type=int, default=13000, help="minimum area size")
    ap.add_argument("-d", "--debugging", type=bool, default=True, help="debugging mode")
    ap.add_argument("-t", "--test", type=str, default=None,help="testing mode")  # Прописываем аргумент -t и название файла JSON
    ap.add_argument("-skip", "--skip", type=int, default=0,help="skip n videos")  # Можно скипнуть некоторое количество видосов
    args = vars(ap.parse_args())

    return args

def point_in_box(point, box):
    if point[0] > box['start'][0] and point[0] < box['end'][0] and \
        point[1] > box['start'][1] and point[1] < box['end'][1]:
        return True
    return  False
