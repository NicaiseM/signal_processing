import pickle
from matplotlib import pyplot as plt


def unpickling(file, plotting=False):
    '''
    Возврат запакованного массива пиков

    Parameters
    ----------
    file : .pickle-файл.
    plotting : Необходимость в графопостроении. По-умолчанию False.

    Returns
    -------
    all_peaks : Список экстремумов следующего вида:
        [[[array([time]), array([channel])],    # Канал 1, пик 1
          [array([time]), array([channel])],    # Канал 1, пик 2
          ...                              ,]   # Канал 1, пик n
          [array([time]), array([channel])],    # Канал 2, пик 1
          [array([time]), array([channel])],    # Канал 2, пик 2
          ...                              ,]]  # Канал 2, пик n
    '''
    with open(file, 'rb') as f:
        settings, t, ch, all_peaks = pickle.load(f)
    if plotting:
        for i in range(len(ch)):
            plt.clf()
            plt.plot(t*settings['t_factor'], ch[i]*settings['ch_factor'],
                     'g-', label='u(t)')
            plt.grid(True)
            plt.xlabel(settings['t_unit'])
            plt.ylabel(settings['ch_unit'])
            # plt.ylim(bottom = 0) # Нижняя граница по у
            if settings['show_legend']:
                plt.legend(loc='best')
            if settings['show_title']:
                plt.title('Общий график, канал № {0}'.format(str(i + 1)))
            # plt.show()
            plt.savefig('./plot {0}.{1}'.format(i + 1, settings['fig_format']),
                        format=settings['fig_format'], dpi=settings['fig_dpi'])
            for num, j in enumerate(all_peaks[i]):
                plt.clf()
                plt.plot(t*settings['t_factor'], ch[i]*settings['ch_factor'],
                         'g-', label='u(t)')
                plt.plot(j[0]*settings['t_factor'], j[1]*settings['ch_factor'],
                         'bx')
                plt.grid(True)
                plt.xlabel(settings['t_unit'])
                plt.ylabel(settings['ch_unit'])
                plt.xlim((j[0][0]-settings['t_expand_left'])*settings['t_factor'],
                         (j[0][0]+settings['t_expand_right'])*settings['t_factor'])
                # plt.ylim(bottom=0) # Нижняя граница по у
                if settings['show_legend']:
                    plt.legend(loc='best')
                if settings['show_title']:
                    plt.title('График пика № {0}, канал № {1}'.format(num + 1,
                                                                      i + 1))
                # plt.show()
                plt.savefig('./plot {0}-{1}.{2}'.format(i + 1, num + 1,
                                                        settings['fig_format']),
                                                        format=settings['fig_format'],
                                                        dpi=settings['fig_dpi'])
    return all_peaks

all_peaks = unpickling('all_peaks.pickle')