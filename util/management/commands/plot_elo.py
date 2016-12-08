from django.core.management.base import BaseCommand
from matplotlib import pyplot as plt, mlab
from matplotlib import gridspec

from TBAW.models import Team
import numpy as np
import numpy.random as nprand

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--file', dest='f', default='', type=str)

    def handle(self, *args, **options):
        if options['f'] is '':
            elo_array = [t.elo_mu for t in Team.objects.exclude(elo_mu=1500.0).order_by('id')]
            id_array = [t.id for t in Team.objects.exclude(elo_mu=1500.0).order_by('id')]
        else:
            pass  # implement read from CSV

        gs = gridspec.GridSpec(2, 3, width_ratios=[1, 1, 2])

        # Spane topmost row
        plt.subplot(gs[0, :])
        num_bins = 100
        elo_mean = np.mean(elo_array)
        elo_var = np.var(elo_array)
        elo_stddev = np.sqrt(elo_var)
        elo_median = np.median(elo_array)

        inner = [x for x in elo_array if elo_mean - elo_stddev<= x <= elo_mean + elo_stddev]
        print("%f%% of elos fall within 1 stddev (%f, %f)" % (100 * len(inner) / len(elo_array), elo_mean - elo_stddev, elo_mean + elo_stddev))

        inner = [x for x in elo_array if elo_mean - 2*elo_stddev <= x <= elo_mean + 2*elo_stddev]
        print("%f%% of elos fall within 2 stddev (%f, %f)" % (100 * len(inner) / len(elo_array), elo_mean - 2*elo_stddev, elo_mean + 2*elo_stddev))

        inner = [x for x in elo_array if elo_mean - 3*elo_stddev <= x <= elo_mean + 3*elo_stddev]
        print("%f%% of elos fall within 3 stddev (%f, %f)" % (100 * len(inner) / len(elo_array), elo_mean - 3*elo_stddev, elo_mean + 3*elo_stddev))

        # Probability Distribution and Fit Line
        n, bins, patches = plt.hist(elo_array, num_bins, normed=True, facecolor='black', alpha=0.9)
        y = mlab.normpdf(bins, elo_mean, elo_stddev)
        plt.plot(bins, y, 'r--')
        plt.title("Current ELO Distribution")
        plt.xlabel("ELO")
        plt.ylabel("Frequency")

        # Mean and Median lines w/ Labels
        median_label_fnt = {
            'size': 'small',
            'weight': 'roman',
            'ha': 'left'
        }

        mean_label_fnt = median_label_fnt.copy()
        mean_label_fnt['ha'] = 'right'

        mean_label_delta = -30
        median_label_delta = 30
        if elo_median < elo_mean:
            mean_label_delta *= -1
            median_label_delta *= -1
            median_label_fnt['ha'], mean_label_fnt['ha'] = mean_label_fnt['ha'], median_label_fnt['ha']

        _, max_freq = plt.ylim()
        plt.axvline(x=elo_median, color="magenta")
        plt.text(elo_median+median_label_delta, max_freq/10, 'Median:\n%.3f' % elo_median, fontdict=median_label_fnt, color="magenta")
        plt.axvline(x=elo_mean, color="orange")
        plt.text(elo_mean+mean_label_delta, max_freq/10, 'Mean:\n%.3f' % elo_mean, fontdict=mean_label_fnt, color="orange")

        # Std Deviation
        plt.text(10, max_freq*.99, "Std Dev: %.3f" % elo_stddev, va='top')
        plt.subplots_adjust(left=0.15, hspace=0.5, wspace=0.3)

        # Plot 2nd subplot in second row, same grid
        ax = plt.subplot(gs[1, 0:2])
        plt.scatter(id_array, elo_array)
        plt.xlabel("Team Number")
        plt.ylabel("ELO")
        ax.set_title("Elo by Team Number")

        # Normal Probability Plot
        ax = plt.subplot(gs[1, 2])

        actual_data = elo_array[:]
        actual_data.sort()
        normal_data = nprand.normal(elo_mean, elo_stddev, size = len(elo_array))
        normal_data.sort()

        plt.plot(normal_data, actual_data, "o")

        z = np.polyfit(normal_data, actual_data, 1)
        p = np.poly1d(z)
        plt.plot(normal_data, p(normal_data), "r--")
        ax.set_title("Normal Probability Plot")
        plt.xlabel("Theoretical ELO (If Normal)")
        plt.ylabel("Actual ELO")
        (xmin, xmax) = plt.xlim()
        ax.margins(x=0.05)
        ax.set_xticks(np.arange(xmin, xmax, 300))
        ax.set_xticks(np.arange(xmin, xmax, 50), minor=True)

        plt.show()
