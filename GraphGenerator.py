import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import textwrap

from Search_mechanism_output import *
 
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from pdfrw import PdfReader, PdfWriter, PageMerge


plt.style.use('ggplot')


RT_DS = 'Recliner torque - DS [Nm]'
RT_TS = 'Recliner torque - TS [Nm]'

FBF_DS = 'DS Front bracket force [kN]'
FBF_TS = 'TS Front bracket force [kN]'


KW_BELT_BRACKET_FORCE_ = 'Belt bracket force'
LAP_FORCE = 'Lap bracket force'
Rear_Bracket_Force_DS = 'Rear bracket force DS'
Rear_Bracket_Force_TS = 'Rear bracket force TS'

BFD_DS = 'Belt Fixation DS displacement [mm]'

# all keywords
KW_LOADCASE = [['loadcase_short_name']]
KW_latch_DS = [['Latch force DS']]
KW_latch_TS = [['Latch force TS']]  

KW_Belt_disp_DS = [['Belt displacement DS']]       
KW_Belt_disp_TS = [['Belt displacement TS']] 
KW_recliner_torque_DS = [['recliner torque DS']]      
KW_recliner_torque_TS = [['recliner torque TS']]      

KW_Front_Bracket_Force_DS = [['Front bracket force DS']]
KW_Front_Bracket_Force_TS = [['Front bracket force TS']]

KW_Belt_Bracket_Force = [['Belt bracket force']]

KW_Rear_Bracket_Force_DS = [['Rear bracket force DS']]
KW_Rear_Bracket_Force_TS = [['Rear bracket force TS']]



# This class contains functions to draw different types of graphs
class GraphGenerator():
    def __init__(self,filepath,design_loop = ''):
        print("PATH:",filepath)
        self.df_origin = pd.read_excel(filepath)
        self.df_origin.columns = self.df_origin.columns.str.strip()  #remove white space in each column name
        self.df_origin = self.df_origin.apply(lambda x: x.str.strip() if x.dtype == "object" else x)


    def two_pie_chart(self,column_name1 = 'integrity', column_name2 = 'specs'):
        fig = plt.figure()
        fig.add_subplot(121)
        pie_chart(self.df,column_name1)
        fig.add_subplot(122)
        pie_chart(self.df,column_name2)

        oem, pjt_name, _ = self.basic_info()
        oem_str, pjt_name_str = 'Oem: ','Project: '
        for s in oem:
            oem_str+=s+' '
        for s in pjt_name:
            pjt_name_str+=s+' '

        plt.text(0.70,0.10,oem_str, transform=fig.transFigure, size=10)
        plt.text(0.70,0.05,pjt_name_str, transform=fig.transFigure, size=10)
        return fig
        
    def belt_bracket(self,dataframe,column_type='loadcase_short_name', column_bar=KW_BELT_BRACKET_FORCE_,column_line=BFD_DS, title = "Belt Bracket on track"):

        xs_bar,ys_bar = dfToDict(dataframe,column_type,column_bar)
        xs_line,ys_line = dfToDict(dataframe,column_type,column_line)

        fig = plt.figure()

        # ax1 = fig.add_subplot(111)
        plt.bar(xs_bar,ys_bar,alpha=.7,color='dodgerblue',edgecolor = "k", label=column_bar)
        plt.legend(prop={'size':8},loc='upper right')
        plt.ylabel("Load[kN]")
        # plt.xlabel(column_type)
        
        # ax2 = ax1.twinx()   # add another plot, sharing the same x-axis
        
        # ax2.plot(xs_line,ys_line,'o-',color = 'mediumblue',lw = 3,label = column_line)
        # ax2.set_ylabel("Disp[mm]")
        # ax2.grid(None)
        plt.ylim(bottom = 0)    # set coordinate limits
        plt.title(title,fontsize= 'large' , pad = 0)
        # ax2.legend(prop={'size': 8}, loc=4)
        
        x_axis = range(len(xs_bar))
        plt.xticks(x_axis, [textwrap.fill(label, 8) for label in xs_bar], 
        rotation = 90, fontsize=8, horizontalalignment="center")
        plt.tight_layout(pad=1.0)           # makes space on the figure canvas for the labels
        plt.tick_params(axis='x', pad=6)
        
        return fig

    def longitudinal_load(self,dataframe,abs_column_name='loadcase_short_name', vert_column_name1='Latch Outer force', vert_column_name2='Latch Inner force', loadcase_name = ''):
        title = "Longitudinal Load" if not self.compare_mode else "Longitudinal Load ("+ loadcase_name + ")"
        fig = self.double_bar_chart(dataframe,abs_column_name, vert_column_name1, vert_column_name2,title,abs_column_name,'Load[kN]')
        # plt.axhline(y=20, color='red', linestyle='--')
        return fig


    def recliner_torque(self,dataframe,abs_column_name='loadcase_short_name', vert_column_name1='recliner torque DS', vert_column_name2='recliner torque TS', loadcase_name = ''):    
        title = "Recliner Torque" if not self.compare_mode else "Longitudinal Load ("+ loadcase_name + ")"
        fig = self.double_bar_chart(dataframe,abs_column_name, vert_column_name1, vert_column_name2,title,abs_column_name,'Torque[N.m]')
        # plt.axhline(y=2000, color='red', linestyle='--')
        return fig

    def front_brackets_load(self,loadcase_column_name = 'loadcase_short_name', doorside_column_name = FBF_DS , tunnelside_column_name= FBF_TS):
        fig = self.double_bar_chart(self.df,loadcase_column_name, doorside_column_name, tunnelside_column_name,'Front Brackets Load','loadcase_short_name','Load[kN]')
        return fig

    def rear_brackets_load(self,loadcase_column_name = 'loadcase_short_name', doorside_column_name = Rear_Bracket_Force_DS, tunnelside_column_name = Rear_Bracket_Force_TS):
        fig = self.double_bar_chart(self.df,loadcase_column_name, doorside_column_name, tunnelside_column_name,'Rear Brackets Load','loadcase_short_name','Load[kN]')
        return fig

    def double_bar_chart(self,dataframe,abs_column_name, vert_column_name1, vert_column_name2,title,xlabel,ylabel):
        fig, xs, _ = double_bar(dataframe,abs_column_name, vert_column_name1, vert_column_name2)
        # plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(prop={'size':8},loc = 'upper right')
        # plt.xticks([x for x in range(len(xs))],xs)  #set x labels and locations
        x_axis = range(len(xs))
        plt.xticks(x_axis, [textwrap.fill(label, 8) for label in xs], 
        rotation = 90, fontsize='small', horizontalalignment="center")
        plt.tight_layout(pad=1.0)           # makes space on the figure canvas for the labels
        plt.tick_params(axis='x', pad=6)
        plt.title(title,pad=0)
        return fig

    def single_bar_chart(self, dataframe,abs_column_name, vert_column_name, title = ''):

        xs_bar,ys_bar = dfToDict(dataframe,abs_column_name,vert_column_name)
        fig = plt.figure()
        plt.bar(xs_bar,ys_bar,alpha=.8,color='dodgerblue',edgecolor = "k",label = vert_column_name)
        plt.legend(prop={'size':8},loc=3)
        # plt.xlabel(abs_column_name)
        plt.ylabel(vert_column_name)
        x_axis = range(len(xs_bar))
        plt.xticks(x_axis, [textwrap.fill(label, 8) for label in xs_bar], 
           rotation = 90, fontsize='small', horizontalalignment="center")
        # plt.tight_layout(pad=1.0)           # makes space on the figure canvas for the labels
        plt.tick_params(axis='x', pad=4)
        
        if title:
            plt.title(title,pad=0)
        else:
            plt.title(vert_column_name,pad=0)
        return fig

    # return basic information of the component
    def basic_info(self):
        x_axis_lable = 'loadcase_short_name'
        df_selected = self.df[['OEM','project_name',x_axis_lable]]
        dic_oem = df_selected.groupby(['OEM']).apply(list).to_dict()
        dic_pjt_name = df_selected.groupby(['project_name']).apply(list).to_dict()
        dic_loadcase = df_selected.groupby([x_axis_lable]).apply(list).to_dict()

        oem_list = [k for k in dic_oem.keys()]
        oem_list = list(filter(None, oem_list))
        pjtname_list = [k for k in dic_pjt_name.keys()]
        pjtname_list = list(filter(None, pjtname_list))
        loadcase_list = [k for k in dic_loadcase.keys()]
        loadcase_list = list(filter(None, loadcase_list))
        print(oem_list)
        print(pjtname_list)
        print(loadcase_list)
        return oem_list, pjtname_list, loadcase_list

    # function to combine multiple PDF pages into one page
    def combine_pages(self,srcpages):
        SCALE = 0.5
        srcpages = PageMerge() + srcpages
        print(srcpages.xobj_box[2:])
        x_increment, y_increment = (SCALE * i for i in srcpages.xobj_box[2:])

        nb_page = len(srcpages)
        for i, page in enumerate(srcpages):
            page.scale(SCALE)
            page.x = x_increment if i & 1 else 0
            page.y = y_increment*((nb_page-1-i) // 2)
        return srcpages.render()

    # functino to generate PDF file
    def generate_pdf(self,cb_selected,design_loop,otheritems, savepath = "THC_Summery_Report"+datetime.today().strftime("%d_%m_%Y")+".pdf", max_per_page = 6):
        # filter design loop
        self.df = self.df_origin[self.df_origin.design_loop.isin(design_loop)]
        _,_,self.loadcase_short_name = self.basic_info()
        self.compare_mode = len(design_loop)>1

        # empty warning message list
        msg_list = []
        with PdfPages(savepath) as pdf:  # create a PDF file
            loadcase_column_name = get_found_column(self.df,KW_LOADCASE,nb_col = 1)
            
            # add figure to the PDF file
            if(cb_selected[0]):
                fig1 = self.two_pie_chart('integrity', 'specs')
                pdf.savefig(fig1)
                plt.close(fig1)

            if not self.compare_mode:
                if(cb_selected[1]):
                    # draw status
                    fbf_ds_column_name = get_found_column(self.df,KW_Belt_Bracket_Force)
                    bfd_ds_column_name = get_found_column(self.df,KW_Belt_disp_DS)
                    if(fbf_ds_column_name and bfd_ds_column_name):
                        fig2 = self.belt_bracket(self.df,loadcase_column_name[0],fbf_ds_column_name[0],bfd_ds_column_name[0])
                        pdf.savefig(fig2)
                        plt.close(fig2)
                if(cb_selected[2]):  
                    # draw Belt bracket on DS track
                    latch_column_name1 = get_found_column(self.df,KW_latch_DS)
                    latch_column_name2 = get_found_column(self.df,KW_latch_TS)
                    if(latch_column_name1 and latch_column_name2):
                        fig3 = self.longitudinal_load(self.df, loadcase_column_name[0], latch_column_name1[0], latch_column_name2[0])
                        pdf.savefig(fig3)
                        plt.close(fig3)
                if(cb_selected[3]):
                    recliner_column_name1 = get_found_column(self.df,KW_recliner_torque_DS)
                    recliner_column_name2 = get_found_column(self.df,KW_recliner_torque_TS)
                    if(recliner_column_name1 and recliner_column_name2):
                        fig4 = self.recliner_torque(self.df, loadcase_column_name[0], recliner_column_name1[0], recliner_column_name2[0])
                        pdf.savefig(fig4)
                        plt.close(fig4)

                if(cb_selected[4]):
                    fbf_ds_column_name = get_found_column(self.df,KW_Front_Bracket_Force_DS)
                    fbf_ts_column_name = get_found_column(self.df,KW_Front_Bracket_Force_TS)
                    if(fbf_ds_column_name and fbf_ts_column_name):
                        fig5 = self.front_brackets_load(loadcase_column_name[0],fbf_ds_column_name[0],fbf_ts_column_name[0])
                        pdf.savefig(fig5)
                        plt.close(fig5)
                        
                if(cb_selected[5]):
                    KW_BELT_BRACKET_FORCE___column_name = get_found_column(self.df,KW_Rear_Bracket_Force_DS)
                    LAP_FORCE_column_name = get_found_column(self.df,KW_Rear_Bracket_Force_TS)
                    if(KW_BELT_BRACKET_FORCE___column_name and LAP_FORCE_column_name):
                        fig6 = self.rear_brackets_load(loadcase_column_name[0],KW_BELT_BRACKET_FORCE___column_name[0],LAP_FORCE_column_name[0])
                        pdf.savefig(fig6)
                        plt.close(fig6)

                # generate other graphs selected
                for item in otheritems:
                    fig = self.single_bar_chart(self.df, loadcase_column_name[0],item)
                    pdf.savefig(fig)
                    plt.close(fig)
                

            # if in compare mode (multiple design loops selected)
            else:
                if(cb_selected[1]):
                    fbf_ds_column_name = get_found_column(self.df,KW_Belt_Bracket_Force)   
                    bfd_ds_column_name = get_found_column(self.df,KW_Belt_disp_DS)
                    
                    if(fbf_ds_column_name and bfd_ds_column_name):
                        for loadcase_short_name in self.loadcase_short_name:
                            dataframe = self.df[self.df.loadcase_short_name == loadcase_short_name]
                            title = "Belt Bracket on track (" + loadcase_short_name + ")"
                            fig = self.belt_bracket(dataframe,column_type='design_loop',column_bar = fbf_ds_column_name[0], column_line = bfd_ds_column_name[0], title = title)
                            pdf.savefig(fig)
                            plt.close(fig)
                if(cb_selected[2]):
                    latch_column_name1 = get_found_column(self.df,KW_latch_DS)
                    latch_column_name2 = get_found_column(self.df,KW_latch_TS)
                    
                    if(latch_column_name1 and latch_column_name2):
                        for loadcase_short_name in self.loadcase_short_name:
                            dataframe = self.df[self.df.loadcase_short_name == loadcase_short_name]
                            fig = self.longitudinal_load(dataframe, 'design_loop', latch_column_name1[0], latch_column_name2[0], loadcase_name = loadcase_short_name)
                            pdf.savefig(fig)
                            plt.close(fig)
                if(cb_selected[3]): 
                    recliner_column_name1 = get_found_column(self.df,KW_recliner_torque_DS)
                    recliner_column_name2 = get_found_column(self.df,KW_recliner_torque_TS)
                    
                    if(recliner_column_name1 and recliner_column_name2):
                        for loadcase_short_name in self.loadcase_short_name:
                            dataframe = self.df[self.df.loadcase_short_name == loadcase_short_name]
                            title  = "Recliner Torque ("+ loadcase_short_name + ")"
                            fig = self.double_bar_chart(dataframe,'design_loop',recliner_column_name1[0],recliner_column_name2[0], title ,'design_loop','Torque[Nm]')
                            pdf.savefig(fig)
                            plt.close(fig)
                if(cb_selected[4]): 
                    fbf_ds_column_name = get_found_column(self.df,KW_Front_Bracket_Force_DS)
                    
                    fbf_ts_column_name = get_found_column(self.df,KW_Front_Bracket_Force_TS)
                    
                    if(fbf_ds_column_name and fbf_ts_column_name):
                        for loadcase_short_name in self.loadcase_short_name:
                            dataframe = self.df[self.df.loadcase_short_name == loadcase_short_name]
                            title  = "Front Brackets Load ("+ loadcase_short_name + ")"
                            fig = self.double_bar_chart(dataframe,'design_loop', fbf_ds_column_name[0], fbf_ts_column_name[0], title ,'design_loop','Load[KN]')
                            pdf.savefig(fig)
                            plt.close(fig)
                if(cb_selected[5]): 
                    KW_BELT_BRACKET_FORCE___column_name = get_found_column(self.df,KW_Rear_Bracket_Force_DS)
                    LAP_FORCE_column_name = get_found_column(self.df,KW_Rear_Bracket_Force_TS)
                    if(KW_BELT_BRACKET_FORCE___column_name and LAP_FORCE_column_name):          
                        for loadcase_short_name in self.loadcase_short_name:
                            dataframe = self.df[self.df.loadcase_short_name == loadcase_short_name]
                            title  = "Rear Brackets Load ("+ loadcase_short_name + ")"
                            fig = self.double_bar_chart(dataframe,'design_loop', KW_BELT_BRACKET_FORCE___column_name[0], LAP_FORCE_column_name[0], title ,'design_loop','Load[KN]')
                            pdf.savefig(fig)
                            plt.close(fig)

                for item in otheritems:
                    for loadcase_short_name in self.loadcase_short_name:
                        dataframe = self.df[self.df.loadcase_short_name == loadcase_short_name]
                        title  = item +" ("+ loadcase_short_name + ")"
                        fig = self.single_bar_chart(self.df, 'design_loop', item, title)
                        pdf.savefig(fig)
                        plt.close(fig)



        # original multi-pages PDF file generated      

        # read the original multi-pages DF file
        pages = PdfReader(savepath).pages

        # overwrite the original PDF file by single page with multiple graphs
        writer = PdfWriter(savepath)
        for index in range(0, len(pages), max_per_page):
            writer.addpage(self.combine_pages(pages[index:index + max_per_page]))
        writer.write()

        return msg_list



# draw a pie chart
def pie_chart(dataframe,column):
    column = column.strip()
    color_dict = {"OK":'limegreen',"OK Limit":'yellow',"NOK Limit":'orange',"NOK":'r','None':'w'}
    df = dataframe[['RunID',column]]    #select columns and generate a dataframe
    dic = df.groupby([column])['RunID'].apply(list).to_dict()  #convert the dataframe to a dictionary

    group_key = []
    group_value = []
    colors = []
    for key in dic:
        group_key.append(key)
        group_value.append(len(dic[key]))
        colors.append(color_dict[key])
        
    def my_autopct(pct):    # function which allows to display the actual amount on the chart
        total = sum(group_value)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%({v:d})'.format(p=pct,v=val)

    plt.pie(group_value, labels = group_key, colors = colors, shadow=True, textprops = {'fontsize':9, 'color':'k'}, startangle=90, autopct=my_autopct, wedgeprops = {'linewidth': 1, 'edgecolor':'k'})  #draw a pie chart
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(column)
    return plt

# draw a double bar chart
def double_bar(dataframe,column_type, column_bar1, column_bar2, subplot = False):
    fig = plt.figure()  #create a empty figure
    xs,ys_1 = dfToDict(dataframe,column_type,column_bar1)   #generate the dictionary
    _,ys_2 = dfToDict(dataframe,column_type,column_bar2)

    # define x coordinate
    x = np.arange(len(xs)) 
    total_width, n = 0.9 , 2
    width = total_width / n
    x = x - (total_width - width) / 2

    plt.bar(x, ys_1, color = "dodgerblue",edgecolor = "k",width=width,label=column_bar1)    #draw bar chart
    plt.bar(x + width, ys_2, color = "mediumblue",edgecolor = "k",width=width,label=column_bar2)
    plt.legend(prop={'size': 8}, loc='upper right')
    
    # display the maximum
    max1, max2 = 0,0
    if len(ys_1)>0:
        max1 = max(ys_1)
    if len(ys_2)>0:
        max2 = max(ys_2)
    plt.text(0.05,0.95,'MAX TS', transform=fig.transFigure, size=10)
    plt.text(0.05,0.90,max1, transform=fig.transFigure, size=10)
    plt.text(0.15,0.95,'MAX DS', transform=fig.transFigure, size=10)
    plt.text(0.15,0.90,max2, transform=fig.transFigure, size=10)
    return fig, xs, plt

# convert a data frame to a dictionary which contains the selected column
def dfToDict(dataframe,column_key,column_value):
    column_key = column_key.strip()
    column_value = column_value.strip()
    df = dataframe[[column_key,column_value]]       # temporary df which contains only 2 columns
    dic = df.groupby([column_key])[column_value].apply(list).to_dict()  # generate a dictionary whose key is the column name, and the value are all values in this column
    dic = {k.strip():v for k,v in dic.items()}  # remove blank space
    dic = {k:v for k,v in dic.items() if k != ''} # remove empty column name
    dic = {k:np.around(np.nanmean(v),2) for k,v in dic.items() if k != ''}  # calculate the average for each key
    xs = [k for k in dic.keys()]    # extract keys and values into 2 lists
    ys = [v for v in dic.values()]
    return xs,ys

