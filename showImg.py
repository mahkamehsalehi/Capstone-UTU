import matplotlib.pyplot as plt

def show_img(img, k, pss, open_img):
    cs = [{'co': 'bo', 'c': 'b'},    
          {'co': 'mo', 'c': 'm'},    
          {'co': 'co', 'c': 'c'},
          {'co': 'yo', 'c': 'y'}]

    m = len(pss)
    plt.clf()
    fig = plt.figure()  # create a new figure window
    ax1 = fig.add_subplot(111)  # add subplot to the figure
    ax1.imshow(img)
    ax1.set_title(str(k))
    
    for i in range(1, m):
        ps = pss[i]['ps']
        n = ps.shape[0]
        l = 1 + pss[i]['ori']  # orientation index
        co, c = cs[l - 1]['co'], cs[l - 1]['c']
        ax1.plot(ps[:, 0], ps[:, 1], co)
        ax1.plot(ps[:, 0], ps[:, 1], c)

    if open_img == 1:
        plt.show()

    return None
