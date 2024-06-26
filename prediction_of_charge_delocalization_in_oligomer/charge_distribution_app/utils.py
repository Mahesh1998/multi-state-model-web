import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_charges(data, group_by='FN', value='value', align='left', bar_width=0.25, margin=0.05, bar_color='green',
                 edge_color='black', edge_thickness=1.5):
    """
    Plot charges as a series of bar plots
    
    :param data: data frame with charges
    :param group_by: column name to group by
    :param value: column name with charge values
    :param align: alignment of the bars
    :param bar_width: width of the bars
    :param margin: margin around the bars
    :param bar_color: color of the bars
    :param edge_color: color of the edges
    :param edge_thickness: thickness of the edges
    :return: plot
    """
    charges = data.groupby(group_by)

    max_nbars = max([len(group) for _, group in charges])

    fig, ax = plt.subplots()
    ax.axis('off')
    ax.set_frame_on(False)

    for j, (name, group) in enumerate(charges):
        n_bars = len(group[value])
        # Plotting rectangles
        if align == 'center':
            start_x = (max_nbars - n_bars) * bar_width / 2
        elif align == 'right':
            start_x = (max_nbars - n_bars) * bar_width  # right align
        elif align == 'left':
            start_x = 0
        else:
            start_x = 0

        for i, charge in enumerate(group[value]):
            rect = patches.Rectangle((start_x + i * bar_width, -j), 0.8 * bar_width, charge, edgecolor=edge_color,
                                     facecolor=bar_color)
            rect.set_linewidth(edge_thickness)
            ax.add_patch(rect)

        # Add text on the right from the last rectangle
        #ax.text(start_x + (n_bars + 0.25)*bar_width, 0.07-j, name, fontsize=14, va='center', ha='left')
        # Add text on the left aligned with the bar height
        ax.text(0, -j + max(group[value]), name, fontsize=14, va='top', ha='left')

    ax.set_xlim(-margin, max_nbars + margin)
    ax.set_ylim(-margin - j, 1 + margin)

    # set plot height
    fig.set_figheight(1 + j)
    # set plot width
    fig.set_figwidth(max_nbars)
    # Optionally display the plot
    return plt


def lean_charges_right(charges):
    """
    If the charge distribution is asymmetric, lean it to the right
    :param charges: charge distribution
    :return: leaned charge distribution
    """
    q = np.array(charges)
    q_rev = np.flip(q)
    indices = np.arange(len(q))
    if q_rev @ indices > q @ indices:
        return q_rev
    return q

