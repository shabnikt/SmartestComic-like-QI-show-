def get_rely_dict(relheight, players=4):
    realy_y = (100 - (int(relheight * 100) * players)) / ((players + 1) * 100)
    rely_dict = {'0': realy_y + relheight / 2,
                 '1': (realy_y + relheight / 2) + (realy_y + relheight) * 1,
                 '2': (realy_y + relheight / 2) + (realy_y + relheight) + (realy_y + relheight),
                 '3': (realy_y + relheight / 2) + (realy_y + relheight) + (realy_y + relheight) + (realy_y + relheight)}
    return rely_dict


def get_rely_list(relheight, players=4):
    realy_y = (100 - (int(relheight * 100) * players)) / ((players + 1) * 100)
    rely_list = [realy_y + relheight / 2,
                 (realy_y + relheight / 2) + (realy_y + relheight) * 1,
                 (realy_y + relheight / 2) + (realy_y + relheight) + (realy_y + relheight),
                 (realy_y + relheight / 2) + (realy_y + relheight) + (realy_y + relheight) + (realy_y + relheight)]
    return rely_list
