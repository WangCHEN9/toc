import re
import pandas as pd 
import numpy as np
import os 
from datetime import datetime
import sys
from make_pivot_table import *


class DataTransferer():
    def __init__(self,raw_file_name = r'df2.xlsx', template_filename = r'THC_summary_regular_excel.xlsx'):

        # raw_file_name is the user input, template_filename is the template df.
        # the goal is to send raw_file_name information to template_filename(template with standard criteria names)

        self.template_filename = template_filename
        # self.df1 = pd.read_excel(self.template_filename)

        self.df1 = pd.DataFrame(columns = ['RunID','OEM','project_name','seatversion','loadcase',
                            'dummy','design_loop','TRK_position','HA_position','pulse','integrity','specs'])
        self.df1.columns = self.df1.columns.str.strip()  #remove white space in each column nameprint(df1)

        # filename = r'df2.xlsx'
        self.df2 = pd.read_excel(raw_file_name)
        self.df2.columns = self.df2.columns.str.strip()  #remove white space in each column nameprint(df2)

        # contains names of all basic columns
        self.basic_info_list = ['RunID','OEM','project_name','seatversion','loadcase',
                            'dummy','design_loop','TRK_position','HA_position','pulse','integrity','specs']

        # All keywords are in this dictionary. 
        # For exemple, ['latch','DS'] means a column should match 2 keywords 'latch' and 'DS' at the same time
        ds_list = ['DS', 'Door', 'outer', 'outter', 'external', 'outboard']
        ts_list = ['TS','tunnel','inner','internal','inboard']
        self.dict_keywords = {'Latch force DS': self.create_regex_dict_keywords_two(['latch','HDM'],ds_list),
                       'Latch force TS': self.create_regex_dict_keywords_two(['latch','HDM'],ts_list),
                       'recliner torque DS': self.create_regex_dict_keywords_three(['recliner'],['torque'],ds_list),
                       'recliner torque TS': self.create_regex_dict_keywords_three(['recliner'],['torque'],ts_list),
                       'recliner axial force DS': self.create_regex_dict_keywords_three(['recliner'],['axial','axis','axial','axis'],ds_list),
                       'recliner axial force TS': self.create_regex_dict_keywords_three(['recliner'],['axial','axis','axial','axis'],ts_list),
                       'Belt displacement DS': self.create_regex_dict_keywords_three(['Belt','anchor'],['displacement','dis','disp'],ds_list),
                       'Belt displacement TS': self.create_regex_dict_keywords_three(['Belt','anchor'],['displacement','dis','disp'],ts_list),
                       'Rear bracket force DS': self.create_regex_dict_keywords_three(['rear','re'],['pivot','bracket'],ds_list),  
                       'Rear bracket force TS': self.create_regex_dict_keywords_three(['rear','re'],['pivot','bracket'],ts_list), 
                       'Front bracket force DS': self.create_regex_dict_keywords_three(['front','fr'],['pivot','bracket'],ds_list),
                       'Front bracket force TS': self.create_regex_dict_keywords_three(['front','fr'],['pivot','bracket'],ts_list),
                       'Belt bracket force': [['Belt', 'bracket','Force'],['BBB']], # need to verify
                       'Lap bracket force': [['Lap', 'bracket','Force'],['Lap', 'belt','Force']],  # need to verify
                       'HA torque': self.create_regex_dict_keywords_two(['HA','Nano','Epump','E-pump'],['torque']),
                       'Backrest dynamic angle DS': self.create_regex_dict_keywords_four(['Backrest'],['angle'],['dynamic','dyna','dyn'],ds_list),
                       'Backrest dynamic angle TS': self.create_regex_dict_keywords_four(['Backrest'],['angle'],['dynamic','dyna','dyn'],ts_list),
                       'Backrest static angle DS': self.create_regex_dict_keywords_four(['Backrest'],['angle'],['static','stat'],ds_list),
                       'Backrest static angle TS': self.create_regex_dict_keywords_four(['Backrest'],['angle'],['static','stat'],ts_list),
                       'Backrest x displ' : self.create_regex_dict_keywords_three(['backrest'],['displacement','dis','disp'],['x']),# need to verify
                       'PELVIS DX': [['PELVIS', 'x', 'dis'],['PELVIS', 'Dx']],  # need to verify
                       'PELVIS DZ': [['PELVIS', 'z', 'dis'],['PELVIS', 'Dz']],  # need to verify
                       'Tilt Axial Force': [['Tilt', 'Axial'],['Tilt', 'axis']], # need to verify
                       'Tilt Shear Force': [['Tilt', 'Shear'],['Tilt', 'Share']], # need to verify
                       'Track sliding DS': self.create_regex_dict_keywords_two(['sliding'],ds_list),
                       'Track sliding TS': self.create_regex_dict_keywords_two(['sliding'],ts_list),
                       'Upper profile section force TS': self.create_regex_dict_keywords_two(['PUPP section force','profile section force','profile_section_force'],ts_list),
                       'Upper profile section force DS': self.create_regex_dict_keywords_two(['PUPP section force','profile section force','profile_section_force'],ds_list),
                       
                       }

        # dictionary of regex
        self.dict_regex = {}
        # write all keyword in a regex form. 
        # For exemple, r"((?=.*latch)(?=.*DS))|((?=.*latch)(?=.*Door))|..."
        for key, value in self.dict_keywords.items():
            regex = r''
            for item in value:
                regex += r'('
                for word in item:
                    regex += r'(?=.*'+word+r')'
                regex += r')'
                regex += r'|'
            regex = regex.rstrip('|')
            self.dict_regex[key] = regex

        self.common_criteria = ['Latch force DS','Latch force TS','recliner torque TS']


    def create_regex_dict_keywords_two(self,keywords1,keywords2):
        keywords_list = []
        for keyword1 in keywords1 :
            for keyword2 in keywords2:
                keywords_list.append([keyword1,keyword2])
        return keywords_list

    def create_regex_dict_keywords_three(self,keywords1,keywords2,keywords3):
        keywords_list = []
        for keyword1 in keywords1 :
            for keyword2 in keywords2:
                for keyword3 in keywords3:
                    keywords_list.append([keyword1,keyword2,keyword3])
        return keywords_list

    def create_regex_dict_keywords_four(self,keywords1,keywords2,keywords3,keyword4):
        keywords_list = []
        for keyword1 in keywords1 :
            for keyword2 in keywords2:
                for keyword3 in keywords3:
                    for keyword4 in keyword4:
                        keywords_list.append([keyword1,keyword2,keyword3,keyword4])
        return keywords_list

    # send data from df2 to df1, according to column name
    def send_data(self,df1_column_name,df2_column_name):  
        if df1_column_name not in self.df1.columns:
            # if column name does not exist, create an empty column
            self.df1[df1_column_name] = np.nan
            print('create empty column:',df1_column_name)
        self.df1[df1_column_name] = self.df1[df1_column_name].combine_first(self.df2[df2_column_name])  # combine 2 columns together
        

    # match column according to regex
    def update_df1_according_to_match(self):
        msg_list = []
        for key in self.dict_regex:
            print("Searching column:",key,"...")
            regex = self.dict_regex[key]
            print("  => Regex:",regex)
            matched = False
            for df2_column_name in self.df2.columns:
                if re.match(regex, df2_column_name, re.I):   
                    print("\t> Column matched!")
                    print("\t>","Column founded: ",df2_column_name)
                    self.send_data(key,df2_column_name)
                    matched = True
                    
            if not matched:
                msg =  key +" not found!"
                print("  => ",msg)
                msg_list.append(msg)    
        
        return self.df1, msg_list

    def send_basic_info(self):
        for basic_info in self.basic_info_list:
            self.send_data(basic_info,basic_info)
        return self.df1

    def getAllCriterias(self):
        all_criteria = self.df1.columns[len(self.basic_info_list):].to_list()
        return all_criteria

    def getUncommonCriterias(self,all_criteria):
        #this returns uncommon criterias
        uncommon_criterias = list(set(all_criteria) - set(self.common_criteria))
        return uncommon_criterias

    # this returns two list of criterias. one is for common criterias. 2nd is the other criterias.
    def getInfo(self):
        self.df1, msg_list = self.update_df1_according_to_match()
        self.df1 = self.send_basic_info()
        all_criteria = self.getAllCriterias()
        uncommon_criterias = self.getUncommonCriterias(all_criteria)
        print('getinfo\n',self.df1)
        return all_criteria, uncommon_criterias, msg_list

    def generate_reg_excel(self):
        from GraphGenerator import dfToDict
        import random 
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("_%d-%m-%Y_%H%M%S.")
        direc = os.path.join(os.path.expanduser("~"), 'Desktop') + '\\THC_output_file'     #declear directory where we want export xlsx file.
        filepath = direc + '\\'+ self.template_filename
        filepath = filepath.split('.')
        filepath = filepath[0]+dt_string+filepath[1]
        print('reg excel saved at path :',filepath)
        
        def find_key_for(input_dict, value):    
            matched = '_'
            for k in input_dict.keys():
                if k == value:
                    matched = input_dict[k]
            return matched

        def rename_loadcase(loadcase):
            loadcase_dict = {
                'Luggage crash': 'LUG',
                'Rear Crash': 'RC',
                'ECE14': 'ECE14',
                'Front Crash': 'FC',
                'FMVSS202a': 'FMVSS202',
                'Lateral Crash': 'LC',
                'Whiplash': 'Whiplash',
                'Z Crash': 'Z Crash',
                'ECE17': 'ECE17',
                'ECE21': 'ECE21',
                'IFX Trans -': 'IFX',
                'IFX Trans +': 'IFX',
                'TopTether': 'IFX',
                }
            loadcase_short = find_key_for(loadcase_dict,loadcase)
            return loadcase_short

        def rename_dummy(dummy):
            dummy_dict = {
                ' D95': '95',
                ' D50': '50',
                ' D05' : '05',
                ' E14': ' ',
                ' IFX' : 'IFX',
                ' BRD' : 'BRD',
                }
            dummy_short = find_key_for(dummy_dict,dummy)
            return dummy_short

        def rename_trkposition(trkposition):
            trkposition_dict = {
                'Tracks:rear most - 1 notch': 'Rm-1n',
                'Tracks:rear most': 'Rm',
                'Tracks:middle': 'Mp',
                'Tracks:front most': 'Fm',
                'Tracks:front most - 1 notch': 'Fm-1n' }
            trkposition_short = find_key_for(trkposition_dict,trkposition)
            return trkposition_short

        def rename_HAposition(HAposition):
            HAposition_dict = {
                ' HA:lower most': 'Dm',
                ' HA:middle': 'Mp',
                ' HA:upper most': 'Um' ,
                ' HA:no_adjm': '' ,
                'Unknown': '' ,}
            HAposition_short = find_key_for(HAposition_dict,HAposition)
            return HAposition_short

        def getLoadcase_full_name(row):
            loadcase_short = rename_loadcase(row['loadcase'])
            dummy_short = rename_dummy(row['dummy'])
            trkposition_short = rename_trkposition(row['TRK_position'])
            HAposition_short = rename_HAposition(row['HA_position'])
            seat_version = row['seatversion']
            loadcase_name_full_short = loadcase_short + dummy_short + ' ' + trkposition_short + HAposition_short
            return loadcase_name_full_short
        
        last_basic_info_column_id = 12

        self.df1.insert(last_basic_info_column_id ,'loadcase_short_name',value='null')
        self.df1['loadcase_short_name'] = self.df1.apply(getLoadcase_full_name, axis=1)

        last_basic_info_column_id += 1  # as we added new column(full loadcase name)
        
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        writer = pd.ExcelWriter(filepath, engine='xlsxwriter') 
        self.df1.to_excel(writer, sheet_name='FEA', index=False,header = True)
        
        # worksheet is instance of Excel sheet "FEA" - used for inserting the table
        worksheet = writer.sheets['FEA']
        # workbook is instance of whole book - used i.e. for cell format assignment 
        workbook = writer.book

        header_cell_format = workbook.add_format()
        header_cell_format.set_rotation(90)
        header_cell_format.set_align('center')
        header_cell_format.set_align('vcenter')

        # create list of dicts for header names 
        #  (columns property accepts {'header': value} as header name)
        col_names = [{'header': col_name} for col_name in self.df1.columns]

        # add table with coordinates: first row, first col, last row, last col; 
        #  header names or formating can be inserted into dict 
        worksheet.add_table(0, 0, self.df1.shape[0], self.df1.shape[1] - 1, {
            'columns': col_names,
            # 'style' = option Format as table value and is case sensitive 
            # (look at the exact name into Excel)
            'style': 'Table Style Medium 10',
            'name': 'FEA'  # name table as 'FEA' for powerBI
        })

        ## create excel sheet for each column
        colors = ['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00']
        count_row = self.df1.shape[0]
        RunID_column_id = self.df1.columns.get_loc("RunID")
        all_columns = self.df1.columns.values.tolist()
        selected_columns = all_columns[last_basic_info_column_id:]

        
        for column in selected_columns :
            # Create a Pandas Excel writer using XlsxWriter as the engine.
            df_basic_info = self.df1.iloc[:,:last_basic_info_column_id].copy()
            # df_basic_info['loadcase_short_name'] = df_basic_info.apply(getLoadcase_full_name, axis=1)
            df_select_column = self.df1[column].copy()
            df_sheet = pd.concat([df_basic_info, df_select_column], axis=1, sort=False)
            
            loadcase_short_name_column_id = df_sheet.columns.get_loc("loadcase_short_name")

            sheet_name = column

            xs, ys = dfToDict(df_sheet,'dummy',column)
            length_xs = len(xs)

            d = { 'dummy_mean': xs, column + ' mean' : ys }
            df_mean = pd.DataFrame(data=d)
            df_sheet_2 = pd.concat([df_sheet, df_mean], axis=1, sort=False)
            df_sheet_2.to_excel(writer, sheet_name=sheet_name,index=False,header = True)

            # Access the XlsxWriter workbook and worksheet objects from the dataframe.
            workbook  = writer.book
            worksheet = writer.sheets[sheet_name]

            # Create a chart object.
            chart = workbook.add_chart({'type': 'column'})

            # Configure the series of the chart from the dataframe data.
            chart.add_series({
                'name':       [sheet_name, 0, last_basic_info_column_id],
                'categories': [sheet_name, 1, loadcase_short_name_column_id, count_row, loadcase_short_name_column_id],
                'values':     [sheet_name, 1, last_basic_info_column_id, count_row, last_basic_info_column_id],
                'fill':       {'color':  random.choice(colors)},
                'overlap':    -5,
            })

            # Configure the chart axes.
            x_axis_name = 'Load case'
            y_axis_name = column
            chart.set_x_axis({'name': x_axis_name})
            chart.set_y_axis({'name': y_axis_name , 'major_gridlines': {'visible': False}})

            # Insert the chart into the worksheet.
            worksheet.insert_chart('O8', chart)

    ##########################################################################33
            ## Create a 2nd chart object.
            chart = workbook.add_chart({'type': 'column'})

            # Configure the series of the chart from the dataframe data.
            chart.add_series({
                'name':       [sheet_name, 0, last_basic_info_column_id],
                'categories': [sheet_name, 1, last_basic_info_column_id + 1, length_xs, last_basic_info_column_id + 1],
                'values':     [sheet_name, 1, last_basic_info_column_id + 2, length_xs, last_basic_info_column_id + 2],
                'fill':       {'color':  random.choice(colors)},
                'overlap':    -5,
            })

            # Configure the chart axes.
            x_axis_name2 = 'dummy'
            y_axis_name2 = column
            chart.set_x_axis({'name': x_axis_name2})
            chart.set_y_axis({'name': y_axis_name2 , 'major_gridlines': {'visible': False}})

            # Insert the chart into the worksheet.
            worksheet.insert_chart('O24', chart)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

        print('temporary file saved at:', filepath)
        
        run_excel(filepath, 'FEA')

        return filepath

