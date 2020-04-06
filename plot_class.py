# General imports
# ---------------
import pandas as pd
import numpy as np
from bokeh.io import show, output_notebook, export_png, export_svgs
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import all_palettes,brewer,viridis,mpl
from bokeh.layouts import gridplot

def category_plot(pd, column, order,cmap, title = 'title', force_list = False, list_array_force = [], show_plot = False):
    """
    Goal:
    -----
    Plot figure of the column to analyse for categorical plots
    
    Input:
    -----
    pd: pandas dataframe
    column: column of the data to analyse
    order: order list of the y axis
    title: title of the figure
    cmap: colormap
    force_list: if True put the value of the list
    list_array_force: value of the list
    show_plot: if False (default) do not show the figure
    
    Ouput:
    -----
    fig: bokeh figure
    
    Author:
    -------
    Martin Szinte (mail@martinszinte.net)
    
    """

    header = list(pd)[column]
    list_array = pd[header].unique()
    list_array = np.array(list_array)
    if force_list == True: 
        list_array = np.array(list_array_force)
    
    sum_cat = []

    for cat_num,cat in enumerate(list_array):
        sum_cat.append(pd[pd[header]==list_array[cat_num]][header].count())

    sum_array = np.array(sum_cat)
    ratio_array = sum_array/sum_array.sum()
    
    # basic settings
    plot_width = 1000
    num_bar = len(list_array)
    val_bar = 40
    if num_bar == 2:     add_pix = 10
    elif num_bar == 3:   add_pix = 4
    elif num_bar == 4:   add_pix = 3
    elif num_bar == 5:   add_pix = 2
    elif num_bar == 6:   add_pix = 0
    elif num_bar == 7:   add_pix = 0
    plot_height = (val_bar+add_pix)*num_bar
    
    bar_height = 0.8
    x_range = (0, 1.5)
    
    # define text addition to plot
    txt_val = []
    for ratio,num in zip(ratio_array,sum_array):
        txt_val.append("  {:1.0f} % (n = {:1.0f})".format(ratio*100,num))
    txt_val = np.array(txt_val)
    
    # define source dictionnary
    num_palette = ratio_array.size
    if num_palette < 3: 
        color = np.array(brewer[cmap][6])
        color = (color[1],color[-2])
    elif num_palette == 4: 
        color = np.array(brewer[cmap][num_palette+1])[np.arange(0,num_palette)]
    else:
        color = np.array(brewer[cmap][num_palette+2])[np.arange(0,num_palette)]
    
    dict_ds = dict( x_val = ratio_array[order], 
                    y_val = list_array[order],
                    txt_val = txt_val[order],
                    color = color)

    source = ColumnDataSource(data = dict_ds)
    fig = figure(x_range = x_range, y_range = list_array[order], plot_width = plot_width, 
                 plot_height = plot_height,title = title)

    fig.hbar(y = 'y_val', left = 0, right = 'x_val', height = bar_height, color = 'color', source = source)
    fig.text(x = 'x_val', y = 'y_val',text = 'txt_val',text_font_style = 'normal', text_font_size = '10pt',text_align = 'left',text_baseline = 'middle',source = source)

    fig.xaxis.axis_label = '';                          fig.toolbar_location = None;
    fig.yaxis.axis_label = '';                          fig.grid.grid_line_color = None;
    fig.axis.minor_tick_in = 0;                         fig.axis.minor_tick_out = 0;                
    fig.axis.major_tick_in = 0;                         fig.axis.major_tick_out = 0;
    fig.outline_line_alpha = 0;                         fig.background_fill_color = (255,255,255);
    fig.axis.major_label_text_font_style = 'italic';    fig.yaxis.major_label_text_font_size = '10pt';
    fig.outline_line_alpha = 0;                         fig.xaxis.major_label_text_font_size = '0pt';
    fig.axis.axis_line_color = None;                    fig.title.text_font_size = '10pt';
    fig.y_range.range_padding = 0;
    
    if show_plot:
        show(fig)

    return fig


def calendar_plot(pd, col_start, title, order, cmap, show_plot = False):
    """
    Goal:
    -----
    Plot figure for calendar plots
    
    Input:
    -----
    pd: pandas dataframe
    col_start: column where the values of the poll start
    header: title of the figure
    order: order list of the y axis
    cmap: colormap
    show_plot: if false (default) do not show the figure
    
    Ouput:
    -----
    fig0: bokeh figure 0
    fig1: bokeh figure 0
    fig2: bokeh figure 0
    
    Author:
    -------
    Martin Szinte (mail@martinszinte.net)
    
    """
    

    # compute values
    # --------------
    days = np.array(['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche'])
    parts = np.array(['matin','après-midi','soirée'])
    list_select = ['O','X']

    sum_array = []
    sum_mor_array = []
    sum_aft_array = []
    sum_eve_array = []
    for day in days:
        if day == days[0]:  columns = [col_start+ 0, col_start+ 1, col_start+ 2]
        elif day == days[1]:columns = [col_start+ 3, col_start+ 4, col_start+ 5]
        elif day == days[2]:columns = [col_start+ 6, col_start+ 7, col_start+ 8]
        elif day == days[3]:columns = [col_start+ 9, col_start+10, col_start+11]
        elif day == days[4]:columns = [col_start+12, col_start+13, col_start+14]
        elif day == days[5]:columns = [col_start+15, col_start+16, col_start+17]
        elif day == days[6]:columns = [col_start+18, col_start+19, col_start+20]

        pd[list(pd)[columns[0]]].fillna(list_select[0])
        pd[list(pd)[columns[1]]].fillna(list_select[0])
        pd[list(pd)[columns[2]]].fillna(list_select[0])
        sum_mor_array.append(pd[pd[list(pd)[columns[0]]]==list_select[1]].count()[list(pd)[columns[0]]])
        sum_aft_array.append(pd[pd[list(pd)[columns[1]]]==list_select[1]].count()[list(pd)[columns[1]]])
        sum_eve_array.append(pd[pd[list(pd)[columns[2]]]==list_select[1]].count()[list(pd)[columns[2]]])

        for column in columns:
            sum_array.append(pd[pd[list(pd)[column]]==list_select[1]].count()[list(pd)[column]])

    sum_mor_array = np.array(sum_mor_array)
    sum_aft_array = np.array(sum_aft_array)
    sum_eve_array = np.array(sum_eve_array)

    # response per day
    sum_days_array = sum_mor_array+sum_aft_array+sum_eve_array
    ratio_days_array = (sum_mor_array+sum_aft_array+sum_eve_array)/(sum_mor_array.sum()+sum_aft_array.sum()+sum_eve_array.sum())

    # response per part of days
    sum_parts_array = np.array([sum_mor_array.sum(),sum_aft_array.sum(),sum_eve_array.sum()])
    ratio_parts_array = sum_parts_array/sum_parts_array.sum()

    # stacked per day in parts
    ratio_part_mor_array = sum_mor_array/(sum_mor_array+sum_aft_array+sum_eve_array)
    ratio_part_aft_array = sum_aft_array/(sum_mor_array+sum_aft_array+sum_eve_array)
    ratio_part_eve_array = sum_eve_array/(sum_mor_array+sum_aft_array+sum_eve_array)

    # Draw figure
    # -----------

    # general settings
    
    val_bar = 40
    plot_width = 1000
    bar_height = 0.8
    x_range = (0, 1.5)
        
    # plot per day
    # ------------
    num_bar = len(days)
    plot_height0 = val_bar*num_bar
    txt_days_val = []
    for ratio,num in zip(ratio_days_array,sum_days_array):
        txt_days_val.append("  {:1.0f} % (n = {:1.0f})".format(ratio*100,num))
    txt_days_val = np.array(txt_days_val)
    
    dict_ds0 = dict( x_val = ratio_days_array[order[0]], 
                    y_val = days[order[0]],
                    txt_val = txt_days_val[order[0]],
                    color = np.array(brewer[cmap][7+2])[np.arange(0,7)]
                   )

    source0 = ColumnDataSource(data = dict_ds0)
    fig0 = figure(x_range = x_range, y_range = days[order[0]], plot_width = plot_width, plot_height = plot_height0, title = title[0])

    fig0.hbar(y = 'y_val', left = 0, right = 'x_val', height = bar_height, color = 'color', source = source0)
    fig0.text(x = 'x_val', y = 'y_val',text = 'txt_val',text_font_style = 'normal', text_font_size = '10pt',text_align = 'left',text_baseline = 'middle',source = source0)

    fig0.xaxis.axis_label = '';                         fig0.toolbar_location = None
    fig0.yaxis.axis_label = '';                         fig0.grid.grid_line_color = None;
    fig0.axis.minor_tick_in = 0;                        fig0.axis.minor_tick_out = 0;
    fig0.axis.major_tick_in = 0;                        fig0.axis.major_tick_out = 0;
    fig0.outline_line_alpha = 0;                        fig0.background_fill_color = (255,255,255);
    fig0.axis.major_label_text_font_style = 'italic';   fig0.yaxis.major_label_text_font_size = '10pt';
    fig0.outline_line_alpha = 0;                        fig0.xaxis.major_label_text_font_size = '0pt';
    fig0.axis.axis_line_color = None;                   fig0.title.text_font_size = '10pt';
    fig0.y_range.range_padding = 0;
    
    # plot per parts
    # --------------
    num_bar = len(parts)
    plot_height1 = (val_bar+4)*num_bar
    txt_parts_val = []
    for ratio,num in zip(ratio_parts_array,sum_parts_array):
        txt_parts_val.append("  {:1.0f} % (n = {:1.0f})".format(ratio*100,num))
    txt_parts_val = np.array(txt_parts_val)
    
    dict_ds1 = dict( x_val = ratio_parts_array[order[1]], 
                     y_val = parts[order[1]],
                     txt_val = txt_parts_val[order[1]],
                     color = np.array(brewer[cmap][3+2])[np.arange(0,3)])

    source1 = ColumnDataSource(data = dict_ds1)
    fig1 = figure(x_range = x_range, y_range = parts[order[1]], plot_width = plot_width, plot_height = plot_height1, title = title[1])

    fig1.hbar(y = 'y_val', left = 0, right = 'x_val', height = bar_height, color = 'color', source = source1)
    fig1.text(x = 'x_val', y = 'y_val',text = 'txt_val',text_font_style = 'normal', text_font_size = '10pt',text_align = 'left',text_baseline = 'middle',source = source1)

    fig1.xaxis.axis_label = '';                         fig1.toolbar_location = None;
    fig1.yaxis.axis_label = '';                         fig1.grid.grid_line_color = None;
    fig1.axis.minor_tick_in = 0;                        fig1.axis.minor_tick_out = 0;
    fig1.axis.major_tick_in = 0;                        fig1.axis.major_tick_out = 0;
    fig1.outline_line_alpha = 0;                        fig1.background_fill_color = (255,255,255);
    fig1.axis.major_label_text_font_style = 'italic';   fig1.yaxis.major_label_text_font_size = '10pt';
    fig1.outline_line_alpha = 0;                        fig1.xaxis.major_label_text_font_size = '0pt';
    fig1.axis.axis_line_color = None;                   fig1.title.text_font_size = '10pt';
    fig1.y_range.range_padding = 0;
    
    # Plot per parts and days
    # -----------------------
    num_bar = len(days)
    plot_height2 = val_bar*num_bar
    dict_ds2 = {'days': days[order[2]],
                parts[0]: ratio_part_mor_array[order[2]],
                parts[1]: ratio_part_aft_array[order[2]],
                parts[2]: ratio_part_eve_array[order[2]]}
    

    source2 = ColumnDataSource(data = dict_ds2)
    fig2 = figure(x_range = x_range, y_range = days[order[2]], 
                 plot_width = plot_width, plot_height = plot_height2, title = title[2])

    color_stack = tuple(np.array(brewer[cmap][3+1])[[2,1,0]])
    fig2.hbar_stack(parts, y = 'days', height = bar_height, color = color_stack,legend_label=["%s" % part for part in parts],source = source2)

    txt_val_mor = []
    txt_val_aft = []
    txt_val_eve = []
    for ratio_mor,ratio_aft,ratio_eve in zip(ratio_part_mor_array,ratio_part_aft_array,ratio_part_eve_array):
        txt_val_mor.append("{:1.0f} %".format(ratio_mor*100))
        txt_val_aft.append("{:1.0f} %".format(ratio_aft*100))
        txt_val_eve.append("{:1.0f} %".format(ratio_eve*100))
    txt_val_mor = np.array(txt_val_mor)
    txt_val_aft = np.array(txt_val_aft)
    txt_val_eve = np.array(txt_val_eve)

    fig2.text(x = ratio_part_mor_array[order[2]]/2, 
              y = days[order[2]],text = txt_val_mor[order[2]],text_font_style = 'normal',text_font_size = '10pt',text_align = 'center',text_baseline = 'middle')
    fig2.text(x = ratio_part_mor_array[order[2]] + ratio_part_aft_array[order[2]]/2, 
              y = days[order[2]],text = txt_val_aft[order[2]],text_font_style = 'normal',text_font_size = '10pt',text_align = 'center',text_baseline = 'middle')
    fig2.text(x = ratio_part_mor_array[order[2]] + ratio_part_aft_array[order[2]] + ratio_part_eve_array[order[2]]/2, 
              y = days[order[2]],text = txt_val_eve[order[2]],text_font_style = 'normal',text_font_size = '10pt',text_align = 'center',text_baseline = 'middle')

    fig2.y_range.range_padding = 0;                     fig2.xaxis.axis_label = ''
    fig2.toolbar_location = None;                       fig2.yaxis.axis_label = ''
    fig2.grid.grid_line_color = None;                   fig2.axis.minor_tick_in = 0
    fig2.axis.minor_tick_out = 0;                       fig2.axis.major_tick_in = 0
    fig2.axis.major_tick_out = 0;                       fig2.outline_line_alpha = 0
    fig2.background_fill_color = (255,255,255);         fig2.axis.major_label_text_font_style = 'italic' 
    fig2.yaxis.major_label_text_font_size = '10pt';     fig2.outline_line_alpha = 0
    fig2.xaxis.major_label_text_font_size = '0pt';      fig2.axis.axis_line_color = None
    fig2.title.text_font_size = '10pt';                 fig2.legend.location = "top_right"
    fig2.legend.label_text_font_style = 'italic';       fig2.legend.padding = 0
    fig2.legend.title_text_font_style ='bold';          fig2.legend.border_line_alpha = 0
    fig2.legend.margin = 0

    if show_plot:
        show(fig0);
        show(fig1)
        show(fig2)

    return fig0, fig1, fig2

def free_question_plot(pd, columns, order, cmap, title = 'title', show_plot = False):
    """
    Goal:
    -----
    Plot figure of the column to analyse for free question plots
    
    Input:
    -----
    pd: pandas dataframe
    columns: column of the data to analyse
    order: order list of the y axis
    cmap : colormap
    title: title of the figure
    show_plot: if False (default) do not show the figure
    
    Ouput:
    -----
    fig: bokeh figure
    
    Author:
    -------
    Martin Szinte (mail@martinszinte.net)
    
    """
    
    list_select = ['O','X']
    sum_array = []
    cat_array = []
    for colunm in columns:
        pd[list(pd)[colunm]] = pd[list(pd)[colunm]].fillna(list_select[0])
        sum_array.append(pd[pd[list(pd)[colunm]]==list_select[1]].count()[list(pd)[colunm]])
        cat_array.append(list(pd)[colunm])

    sum_array = np.array(sum_array)
    ratio_array =  sum_array/sum_array.sum()
    cat_array = np.array(cat_array)

    # basic settings
    plot_width = 1000
    num_bar = len(cat_array)
    val_bar = 40
    if num_bar == 2:     add_pix = 10
    elif num_bar == 3:   add_pix = 4
    elif num_bar == 4:   add_pix = 3
    elif num_bar == 5:   add_pix = 2
    elif num_bar == 6:   add_pix = 0
    elif num_bar == 7:   add_pix = 0
    elif num_bar == 8:   add_pix = 0
    plot_height = (val_bar+add_pix)*num_bar

    bar_height = 0.8
    x_range = (0, 1.5)

    # define text addition to plot
    txt_val = []
    for ratio,num in zip(ratio_array,sum_array):
        txt_val.append("  {:1.0f} % (n = {:1.0f})".format(ratio*100,num))
    txt_val = np.array(txt_val)

    # define source dictionnary
    num_palette = ratio_array.size
    if num_palette < 3: 
        color = np.array(brewer[cmap][6])
        color = (color[1],color[-2])
    elif num_palette == 8:
        color = np.array(brewer[cmap][num_palette+1])[np.arange(0,num_palette)]
    else:
        color = np.array(brewer[cmap][num_palette+2])[np.arange(0,num_palette)]

    dict_ds = dict( x_val = ratio_array[order], 
                    y_val = cat_array[order],
                    txt_val = txt_val[order],
                    color = color)

    source = ColumnDataSource(data = dict_ds)
    fig = figure(x_range = x_range, y_range = cat_array[order], plot_width = plot_width, 
                 plot_height = plot_height,title = title)

    fig.hbar(y = 'y_val', left = 0, right = 'x_val', height = bar_height, color = 'color', source = source)
    fig.text(x = 'x_val', y = 'y_val',text = 'txt_val',text_font_style = 'normal', text_font_size = '10pt',text_align = 'left',text_baseline = 'middle',source = source)

    fig.xaxis.axis_label = '';                          fig.toolbar_location = None;
    fig.yaxis.axis_label = '';                          fig.grid.grid_line_color = None;
    fig.axis.minor_tick_in = 0;                         fig.axis.minor_tick_out = 0;                
    fig.axis.major_tick_in = 0;                         fig.axis.major_tick_out = 0;
    fig.outline_line_alpha = 0;                         fig.background_fill_color = (255,255,255);
    fig.axis.major_label_text_font_style = 'italic';    fig.yaxis.major_label_text_font_size = '10pt';
    fig.outline_line_alpha = 0;                         fig.xaxis.major_label_text_font_size = '0pt';
    fig.axis.axis_line_color = None;                    fig.title.text_font_size = '10pt';
    fig.y_range.range_padding = 0;

    if show_plot:
        show(fig)
    
    return fig


def quality_plot(pd, column, order, cmap, title = 'title', show_plot = False):

    """
    Goal:
    -----
    Plot figure of the quality plot
    
    Input:
    -----
    pd: pandas dataframe
    column: starter column
    order: order list of the y axis
    title: title of the figure
    cmap : colormap
    show_plot: if False (default) do not show the figure
    
    Ouput:
    -----
    fig: bokeh figure
    
    Author:
    -------
    Martin Szinte (mail@martinszinte.net)
    
    """
    categories = np.array(['le choix','la qualité','le prix'])
    valences = np.array(["très bien","bien","pas terrible","mauvais"])


    header_choice = list(pd)[column]
    header_quality = list(pd)[column+1]
    header_price = list(pd)[column+2]
    sum_array_choice = []
    sum_array_quality = []
    sum_array_price = []
    for cat_num,cat in enumerate(valences):
        sum_array_choice.append(pd[pd[header_choice]==valences[cat_num]][header_choice].count())
        sum_array_quality.append(pd[pd[header_quality]==valences[cat_num]][header_quality].count())
        sum_array_price.append(pd[pd[header_price]==valences[cat_num]][header_price].count())

    sum_array_choice = np.array(sum_array_choice)
    sum_array_quality = np.array(sum_array_quality)
    sum_array_price = np.array(sum_array_price)

    ratio_array_choice = sum_array_choice/sum_array_choice.sum()
    ratio_array_quality = sum_array_quality/sum_array_quality.sum()
    ratio_array_price = sum_array_price/sum_array_price.sum()

    ratio_array_val0 = np.array([ratio_array_choice[0],ratio_array_quality[0],ratio_array_price[0]])
    ratio_array_val1 = np.array([ratio_array_choice[1],ratio_array_quality[1],ratio_array_price[1]])
    ratio_array_val2 = np.array([ratio_array_choice[2],ratio_array_quality[2],ratio_array_price[2]])
    ratio_array_val3 = np.array([ratio_array_choice[3],ratio_array_quality[3],ratio_array_price[3]])


    # Draw figure
    # -----------
    # general settings
    val_bar = 40
    plot_width = 1000
    bar_height = 0.8
    x_range = (0, 1.5)


    # Plot per parts and days
    # -----------------------
    num_bar = len(categories)
    plot_height = (val_bar+4)*num_bar
    dict_ds = {'categories': categories[order],
                valences[0]: ratio_array_val0[order],
                valences[1]: ratio_array_val1[order],
                valences[2]: ratio_array_val2[order],
                valences[3]: ratio_array_val3[order],
               }

    source = ColumnDataSource(data = dict_ds)
    fig = figure(x_range = x_range, y_range = categories[order], 
                 plot_width = plot_width, plot_height = plot_height, title = title)

    color_stack = tuple(np.array(brewer[cmap][4+1])[[3,2,1,0]])

    fig.hbar_stack(valences, y = 'categories', color = color_stack, height = bar_height,legend_label=["%s" % valence for valence in valences],source = source)
    txt_val0 = []
    txt_val1 = []
    txt_val2 = []
    txt_val3 = []
    for ratio0,ratio1,ratio2,ratio3 in zip(ratio_array_val0,ratio_array_val1,ratio_array_val2,ratio_array_val3):
        if ratio0*100 > 1: txt_val0.append("{:1.0f} %".format(ratio0*100))
        else: txt_val0.append("")
            
        if ratio1*100 > 1: txt_val1.append("{:1.0f} %".format(ratio1*100))
        else: txt_val1.append("")
            
        if ratio2*100 > 1: txt_val2.append("{:1.0f} %".format(ratio2*100))
        else: txt_val2.append("")
            
        if ratio3*100 > 1: txt_val3.append("{:1.0f} %".format(ratio3*100))
        else: txt_val3.append("")
        

    txt_val0 = np.array(txt_val0)
    txt_val1 = np.array(txt_val1)
    txt_val2 = np.array(txt_val2)
    txt_val3 = np.array(txt_val3)


    fig.text(x = ratio_array_val0[order]/2, 
             y = categories[order], text = txt_val0[order],text_font_style = 'normal',text_font_size = '10pt',text_align = 'center',text_baseline = 'middle')
    fig.text(x = ratio_array_val0[order] + ratio_array_val1[order]/2, 
             y = categories[order], text = txt_val1[order],text_font_style = 'normal',text_font_size = '10pt',text_align = 'center',text_baseline = 'middle')
    fig.text(x = ratio_array_val0[order] + ratio_array_val1[order] + ratio_array_val2[order]/2, 
             y = categories[order], text = txt_val2[order],text_font_style = 'normal',text_font_size = '10pt',text_align = 'center',text_baseline = 'middle')
    fig.text(x = ratio_array_val0[order] + ratio_array_val1[order] + ratio_array_val2[order] + ratio_array_val3[order]/2, 
             y = categories[order], text = txt_val3[order],text_font_style = 'normal',text_font_size = '10pt',text_align = 'center',text_baseline = 'middle')

    fig.y_range.range_padding = 0;                     fig.xaxis.axis_label = ''
    fig.toolbar_location = None;                       fig.yaxis.axis_label = ''
    fig.grid.grid_line_color = None;                   fig.axis.minor_tick_in = 0
    fig.axis.minor_tick_out = 0;                       fig.axis.major_tick_in = 0
    fig.axis.major_tick_out = 0;                       fig.outline_line_alpha = 0
    fig.background_fill_color = (255,255,255);         fig.axis.major_label_text_font_style = 'italic' 
    fig.yaxis.major_label_text_font_size = '10pt';     fig.outline_line_alpha = 0
    fig.xaxis.major_label_text_font_size = '0pt';      fig.axis.axis_line_color = None
    fig.title.text_font_size = '10pt';                 fig.legend.location = "top_right"
    fig.legend.label_text_font_style = 'italic';       fig.legend.margin = 0
    fig.legend.title_text_font_style ='bold';          fig.legend.border_line_alpha = 0
    fig.legend.padding = 0

    if show_plot == True:
        show(fig)
        
    return fig

def quality_plot2(pd, column, order, cmap, title = 'title', show_plot = False):

    """
    Goal:
    -----
    Plot figure of the quality plot of second type
    
    Input:
    -----
    pd: pandas dataframe
    column: starter column
    order: order list of the y axis
    title: title of the figure
    cmap : colormap
    show_plot: if False (default) do not show the figure
    
    Ouput:
    -----
    fig: bokeh figure
    
    Author:
    -------
    Martin Szinte (mail@martinszinte.net)
    
    """

    
    categories = np.array(["apéro mensuel", "concours de tartes", "atelier pâtes avec Arcimboldo","découvrir le pain avec la boulangerie Salvator",
                           "journée portes ouvertes", "décrypter les étiquettes et faire ses courses en conscience", "disco soupe","projection(s) de film(s)"])
    
    
    valences = np.array(["très bien","bien","pas terrible","mauvais"])

    header0, header1, header2, header3 = list(pd)[column],   list(pd)[column+1], list(pd)[column+2], list(pd)[column+3]
    header4, header5, header6, header7 = list(pd)[column+4], list(pd)[column+5], list(pd)[column+6], list(pd)[column+7]
   
    sum_array0, sum_array1, sum_array2, sum_array3 = [], [], [], []
    sum_array4, sum_array5, sum_array6, sum_array7 = [], [], [], []

    for cat_num,cat in enumerate(valences):
        sum_array0.append(pd[pd[header0]==valences[cat_num]][header0].count())
        sum_array1.append(pd[pd[header1]==valences[cat_num]][header1].count())
        sum_array2.append(pd[pd[header2]==valences[cat_num]][header2].count())
        sum_array3.append(pd[pd[header3]==valences[cat_num]][header3].count())
        sum_array4.append(pd[pd[header4]==valences[cat_num]][header4].count())
        sum_array5.append(pd[pd[header5]==valences[cat_num]][header5].count())
        sum_array6.append(pd[pd[header6]==valences[cat_num]][header6].count())
        sum_array7.append(pd[pd[header7]==valences[cat_num]][header7].count())
        
    sum_array0, sum_array1, sum_array2, sum_array3 = np.array(sum_array0), np.array(sum_array0), np.array(sum_array2), np.array(sum_array3),
    sum_array4, sum_array5, sum_array6, sum_array7 = np.array(sum_array4), np.array(sum_array5), np.array(sum_array6), np.array(sum_array7),
    
    ratio_array0, ratio_array1, ratio_array2, ratio_array3 = sum_array0/sum_array0.sum(), sum_array1/sum_array1.sum(), sum_array2/sum_array2.sum(), sum_array3/sum_array3.sum()
    ratio_array4, ratio_array5, ratio_array6, ratio_array7 = sum_array4/sum_array4.sum(), sum_array5/sum_array5.sum(), sum_array6/sum_array6.sum(), sum_array7/sum_array7.sum()

    ratio_array_val0 = np.array([ratio_array0[0],ratio_array1[0],ratio_array2[0],ratio_array3[0],ratio_array4[0],ratio_array5[0],ratio_array6[0],ratio_array7[0]])
    ratio_array_val1 = np.array([ratio_array0[1],ratio_array1[1],ratio_array2[1],ratio_array3[1],ratio_array4[1],ratio_array5[1],ratio_array6[1],ratio_array7[1]])
    ratio_array_val2 = np.array([ratio_array0[2],ratio_array1[2],ratio_array2[2],ratio_array3[2],ratio_array4[2],ratio_array5[2],ratio_array6[2],ratio_array7[2]])
    ratio_array_val3 = np.array([ratio_array0[3],ratio_array1[3],ratio_array2[3],ratio_array3[3],ratio_array4[3],ratio_array5[3],ratio_array6[3],ratio_array7[3]])

    # Draw figure
    # -----------
    # general settings
    val_bar = 40
    plot_width = 1000
    bar_height = 0.8
    x_range = (0, 1.5)

    # Plot per parts and days
    # -----------------------
    num_bar = len(categories)
    plot_height = (val_bar+4)*num_bar
    dict_ds = {'categories': categories[order],
                valences[0]: ratio_array_val0[order],
                valences[1]: ratio_array_val1[order],
                valences[2]: ratio_array_val2[order],
                valences[3]: ratio_array_val3[order],
               }

    source = ColumnDataSource(data = dict_ds)
    fig = figure(x_range = x_range, y_range = categories[order], 
                 plot_width = plot_width, plot_height = plot_height, title = title)

    color_stack = tuple(np.array(brewer[cmap][4+1])[[3,2,1,0]])

    fig.hbar_stack(valences, y = 'categories', color = color_stack, height = bar_height,legend_label=["%s" % valence for valence in valences],source = source)
    txt_val0 = []
    txt_val1 = []
    txt_val2 = []
    txt_val3 = []
    for ratio0,ratio1,ratio2,ratio3 in zip(ratio_array_val0,ratio_array_val1,ratio_array_val2,ratio_array_val3):
        if ratio0*100 > 1: txt_val0.append("{:1.0f} %".format(ratio0*100))
        else: txt_val0.append("")
            
        if ratio1*100 > 1: txt_val1.append("{:1.0f} %".format(ratio1*100))
        else: txt_val1.append("")
            
        if ratio2*100 > 1: txt_val2.append("{:1.0f} %".format(ratio2*100))
        else: txt_val2.append("")
            
        if ratio3*100 > 1: txt_val3.append("{:1.0f} %".format(ratio3*100))
        else: txt_val3.append("")
        

    txt_val0 = np.array(txt_val0)
    txt_val1 = np.array(txt_val1)
    txt_val2 = np.array(txt_val2)
    txt_val3 = np.array(txt_val3)


    fig.text(x = ratio_array_val0[order]/2, 
             y = categories[order], text = txt_val0[order],text_font_style = 'normal',text_font_size = '10pt',text_align = 'center',text_baseline = 'middle')
    fig.text(x = ratio_array_val0[order] + ratio_array_val1[order]/2, 
             y = categories[order], text = txt_val1[order],text_font_style = 'normal',text_font_size = '10pt',text_align = 'center',text_baseline = 'middle')
    fig.text(x = ratio_array_val0[order] + ratio_array_val1[order] + ratio_array_val2[order]/2, 
             y = categories[order], text = txt_val2[order],text_font_style = 'normal',text_font_size = '10pt',text_align = 'center',text_baseline = 'middle')
    fig.text(x = ratio_array_val0[order] + ratio_array_val1[order] + ratio_array_val2[order] + ratio_array_val3[order]/2, 
             y = categories[order], text = txt_val3[order],text_font_style = 'normal',text_font_size = '10pt',text_align = 'center',text_baseline = 'middle')

    fig.y_range.range_padding = 0;                     fig.xaxis.axis_label = ''
    fig.toolbar_location = None;                       fig.yaxis.axis_label = ''
    fig.grid.grid_line_color = None;                   fig.axis.minor_tick_in = 0
    fig.axis.minor_tick_out = 0;                       fig.axis.major_tick_in = 0
    fig.axis.major_tick_out = 0;                       fig.outline_line_alpha = 0
    fig.background_fill_color = (255,255,255);         fig.axis.major_label_text_font_style = 'italic' 
    fig.yaxis.major_label_text_font_size = '10pt';     fig.outline_line_alpha = 0
    fig.xaxis.major_label_text_font_size = '0pt';      fig.axis.axis_line_color = None
    fig.title.text_font_size = '10pt';                 fig.legend.location = "top_right"
    fig.legend.label_text_font_style = 'italic';       fig.legend.margin = 0
    fig.legend.title_text_font_style ='bold';          fig.legend.border_line_alpha = 0
    fig.legend.padding = 0

    if show_plot == True:
        show(fig)
        
    return fig


def save_free_text(pd,f,title,column):
    f.write('\n\n--------------------------------------------------------------------------------------------------------------------------------------\n')
    f.write(str(title))
    f.write('\n--------------------------------------------------------------------------------------------------------------------------------------\n')
    for line in np.array(pd[list(pd)[column]].fillna('')[pd[list(pd)[column]].fillna('')!='']): 
        f.write(str('\n'+line))
        

def save_volunters(pd,f,columns,column_mail,rep):
    for column in columns:
        f.write('\n\n--------------------------------------------------------------------------------------------------------------------------------------\n')
        f.write(str(list(pd)[column]))
        f.write('\n--------------------------------------------------------------------------------------------------------------------------------------\n')
        for line in (pd[pd[list(pd)[column]]==rep][list(pd)[column_mail]]):
            f.write(str('\n'+str(line)))