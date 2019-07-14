import os
os.chdir('C:\\Users\\fchristoffer\\Desktop\\CSV_to_CQL\\final')

"""-------------------------------------------------------------------------"""
"""Provide Data"""
"""-------------------------------------------------------------------------"""
files_csv = []
files_names = ['firehd_category_predict_reviewed.csv', 
         'firehd_tag_predict_reviewed.csv',
         'ipad_category_predict_reviewed.csv',
         'ipad_tag_predict_reviewed.csv',
         'samsung_category_predict_reviewed.csv',
         'samsung_tag_predict_reviewed.csv']

for i, line in enumerate(files_names):
    with open(line, 'r', encoding='utf-8') as f:
        x = f.readlines()
        files_csv.append(x)

firehd_category_predict_reviewed_csv = files_csv[0]
firehd_tag_predict_reviewed_csv = files_csv[1]
ipad_category_predict_reviewed_csv = files_csv[2]
ipad_tag_predict_reviewed_csv = files_csv[3]
samsung_category_predict_reviewed_csv = files_csv[4]
samsung_tag_predict_reviewed_csv = files_csv[5]

firehd_category_predict_reviewed_csv_split = []
firehd_tag_predict_reviewed_csv_split = []
ipad_category_predict_reviewed_csv_split = []
ipad_tag_predict_reviewed_csv_split = []
samsung_category_predict_reviewed_csv_split = []
samsung_tag_predict_reviewed_csv_split = []

for i, line in enumerate(firehd_category_predict_reviewed_csv):
    x = line.split(';')
    x[1] = x[1].replace('\n','')
    firehd_category_predict_reviewed_csv_split.append(x)
    
    
for i, line in enumerate(firehd_tag_predict_reviewed_csv):
    x = line.split(';')
    x[1] = x[1].replace('\n','')
    firehd_tag_predict_reviewed_csv_split.append(x)
    
for i, line in enumerate(ipad_category_predict_reviewed_csv):
    x = line.split(';')
    x[1] = x[1].replace('\n','')
    ipad_category_predict_reviewed_csv_split.append(x)
    
for i, line in enumerate(ipad_tag_predict_reviewed_csv):
    x = line.split(';')
    x[1] = x[1].replace('\n','')
    ipad_tag_predict_reviewed_csv_split.append(x)
    
for i, line in enumerate(samsung_category_predict_reviewed_csv):
    x = line.split(';')
    x[1] = x[1].replace('\n','')
    samsung_category_predict_reviewed_csv_split.append(x)
    
for i, line in enumerate(samsung_tag_predict_reviewed_csv):
    x = line.split(';')
    x[1] = x[1].replace('\n','')
    samsung_tag_predict_reviewed_csv_split.append(x)
   
del files_csv
del firehd_category_predict_reviewed_csv
del firehd_tag_predict_reviewed_csv
del ipad_category_predict_reviewed_csv
del ipad_tag_predict_reviewed_csv
del samsung_category_predict_reviewed_csv
del samsung_tag_predict_reviewed_csv

# This function changes the id of each device life follows:
# Firehd: need_id:10000
# ipad: need_id:20000
# samsung: need_id:30000

def idchangefordevice(input_list, manufacturer):
    if manufacturer == 'apple':
        need_id = '2'
    elif manufacturer == 'samsung':
        need_id = '3'
        
    output_list = []
    for i, line in enumerate(input_list):
        if line[0].startswith('id:'):
            line[0] = line[0].replace('id:1', 'id:'+need_id)
            output_list.append(line)
        else:
            output_list.append(line)
        
    return output_list;

ipad_category_predict_reviewed_csv_split = idchangefordevice(ipad_category_predict_reviewed_csv_split,'apple')
ipad_tag_predict_reviewed_csv_split = idchangefordevice(ipad_tag_predict_reviewed_csv_split,'apple')
samung_category_predict_reviewed_csv_split = idchangefordevice(samsung_category_predict_reviewed_csv_split,'samsung')
samsung_tag_predict_reviewed_csv_split = idchangefordevice(samsung_tag_predict_reviewed_csv_split,'samsung')
        

"""-------------------------------------------------------------------------"""
"""Create need nodes (Original Needs)"""
"""-------------------------------------------------------------------------"""
#Creation of [need_id,need_text] Matrix
def csv_to_id_need(input_list):
    X = []
    for i, line in enumerate(input_list):
       h = ''.join(input_list[i][0])
       X.append(h)       
    X = ' '.join(X)   
    X = X.split('id:')   
    del X[0]  

    Y = []
    for i, line in enumerate(X):
        need_id=line[0:5]
        need_id = 'id:' + need_id
        line = line[6:]
        line = line.replace('"', '')
        newline = [need_id , line]
        Y.append(newline)
    
    return Y

firehd_category_need_id_need_text = csv_to_id_need(firehd_category_predict_reviewed_csv_split)    
ipad_category_need_id_need_text = csv_to_id_need(ipad_category_predict_reviewed_csv_split)
samsung_category_need_id_need_text = csv_to_id_need(samsung_category_predict_reviewed_csv_split)

# Create CQL Code (Only subneeds (categories) taken, because they contain all sentences) 
# Firehd: need_id:10000
# ipad: need_id:20000
# samsung: need_id:30000

def createCQLneeds(input_list, manufacturer):
    CQL_needs = []
    if manufacturer == 'amazon':
        need_id = 10000
    elif manufacturer == 'apple':
        need_id = 20000
    elif manufacturer == 'samsung':
        need_id = 30000
        
    for i, line in enumerate(input_list):
        x = 'CREATE (need'+ input_list[i][0]+ ':OriginalText{'+input_list[i][0] +', content:"'+input_list[i][1]+'"})'
        x = x.replace('needid:' , 'need')
        CQL_needs.append(x)
    
    return CQL_needs

CQL_firehd_needs = createCQLneeds(firehd_category_need_id_need_text,'amazon')
CQL_ipad_needs = createCQLneeds(ipad_category_need_id_need_text ,'apple')
CQL_samsung_needs = createCQLneeds(samsung_category_need_id_need_text ,'samsung')



"""-------------------------------------------------------------------------"""
"""Create TAG nodes"""
"""-------------------------------------------------------------------------"""

#Creation of [need_id,tag_text] Matrix
def csv_to_id_tag(input_list):
    
    tag_list = []
    for i, line in enumerate(input_list):
        
        if line[0].startswith('id:'):
            sentence_id = line[0]
            
        elif line[1].endswith('B-TG'):
            b_tag_line = sentence_id + line[0]
            tag_list.append(b_tag_line)
        
        elif line[1].endswith('I-TG'):
            i_tag_line = line[0]
            tag_list.append(i_tag_line)
            
    tag_list = ' '.join(tag_list)
    tag_list = tag_list.split('id:')
    del tag_list[0]
    
    result111 = []
    for i, line in enumerate(tag_list):
            x = line[0:5]
            line = line.split(x)
            line[0] = 'id:' + x
            result111.append(line)
         
    return result111;

firehd_needid_tagtext = csv_to_id_tag(firehd_tag_predict_reviewed_csv_split)
ipad_needid_tagtext = csv_to_id_tag(ipad_tag_predict_reviewed_csv_split)
samsung_needid_tagtext = csv_to_id_tag(samsung_tag_predict_reviewed_csv_split)

tag_all = firehd_needid_tagtext + ipad_needid_tagtext + samsung_needid_tagtext

# Make sure not to create double Tag nodes:

tag_list_1 = []
for i, line in enumerate(tag_all):
    X = line[1]
    tag_list_1.append(X)
    
tag_list_1 = list(set(tag_list_1))

tag_list = []
for i, line in enumerate(tag_list_1):
    line = [i,line]
    tag_list.append(line)


       

 # Create CQL Code
CQL_tags = []
for i, line in enumerate(tag_list):    
    x = 'CREATE (tag'+ str(tag_list[i][0]) + ':Tag{tag_id:' + str(tag_list[i][0]) + ', tag_name:"'+tag_list[i][1]+'"})'
    CQL_tags.append(x)
 
    
"""-------------------------------------------------------------------------"""
"""Create Subneeds Notes"""
"""-------------------------------------------------------------------------"""
#Creation of [need_id,subneed_class,subneed_text] Matrix
def csv_to_id_class(input_list):
    tag_list = []
    for i, line in enumerate(input_list):
    
        if line[0].startswith('id:'):
            sentence_id = line[0]

        elif line[1] == 'B-HS' or line[1] == 'B-H' or line[1] == 'B-S' or line[1] == 'B-O':
            b_tag_line = sentence_id + line [0] + line [1]
            tag_list.append(b_tag_line)
        
        elif line[1] == 'I-HS' or line[1] == 'I-H' or line[1] == 'I-S' or line[1] == 'I-O':
            i_tag_line = line [0] + line [1]
            tag_list.append(i_tag_line)
        
    tag_list = ' '.join(tag_list)
    tag_list = tag_list.split('id:')
    del tag_list[0]
    
    result111 = []
    for i, line in enumerate(tag_list):
            x = line[0:5]
            line = line.split(x)
            line[0] = 'id:' + x
            
            if line[1].endswith('I-HS ') or line[1].endswith('B-HS '):
                    classify = 'HS'
            elif line[1].endswith('H ') or line[1].endswith('B-H '):
                    classify = 'H'
            elif line[1].endswith('S ') or line[1].endswith('B-S '):
                    classify = 'S'
            elif line[1].endswith('O ') or line[1].endswith('B-O '):
                    classify = 'O'

          
            line[1] = line[1] +';'+ classify     
            result111.append(line)
         
            result111[i][1] = result111[i][1].replace('I-HS','')
            result111[i][1] = result111[i][1].replace('I-H','')
            result111[i][1] = result111[i][1].replace('I-S','')
            result111[i][1] = result111[i][1].replace('I-O','')
            result111[i][1] = result111[i][1].replace('B-HS','')
            result111[i][1] = result111[i][1].replace('B-H','')
            result111[i][1] = result111[i][1].replace('B-S','')
            result111[i][1] = result111[i][1].replace('B-O','')
            
    return result111;

A = csv_to_id_class(samung_category_predict_reviewed_csv_split)
B = csv_to_id_class(ipad_category_predict_reviewed_csv_split)
C = csv_to_id_class(firehd_category_predict_reviewed_csv_split)
class_all = A + B + C

# Make sure not to create double Classify nodes:

class_list_1 = []
for i, line in enumerate(class_all):
    X = line[1]
    class_list_1.append(X)
    
class_list_1 = list(set(class_list_1))

class_list = []
for i, line in enumerate(class_list_1):
    line = line.split(';')
    line = [i] + line
    class_list.append(line)

X = []
for i, line in enumerate(class_all):
    line[1] = line[1].replace(';HS', '')
    line[1] = line[1].replace(';H', '')
    line[1] = line[1].replace(';S', '')
    line[1] = line[1].replace(';O', '')
    
    X.append(line)

class_all = X
del class_list_1

 # Create CQL Code
CQL_subneeds = []
for i, line in enumerate(class_list):    
    x = 'CREATE (subneed'+ str(class_list[i][0]) + ':'+str(class_list[i][2])+'{subneed_text:"' + str(class_list[i][1]) + '", class_id:'+str(class_list[i][0])+'})'
    CQL_subneeds.append(x)
    

"""-------------------------------------------------------------------------"""
"""Create NEEDS TO TAG Relationship"""
"""-------------------------------------------------------------------------"""
CQL_tags_to_needs = []
for i, i_line in enumerate(tag_all):
    for j, j_line in enumerate(tag_list):
        if i_line[1] == j_line[1]:          
            x = 'CREATE ('+ str(tag_all[i][0])+')-[r'+str(int(i+10000))+':Tag]->('+ 'tag'+str(tag_list[j][0]) +')'
            x = x.replace('id:','need')
            CQL_tags_to_needs.append(x)


"""-------------------------------------------------------------------------"""
"""Create NEEDS TO SUBNEEDS Relationship"""
"""-------------------------------------------------------------------------"""
CQL_needs_to_subneeds = []
for i, i_line in enumerate(class_all):
    for j, j_line in enumerate(class_list):
        if i_line[1] == j_line[1]:          
            x = 'CREATE ('+ str(class_all[i][0])+')-[r'+str(int(i+20000))+':Sub]->('+ 'subneed'+str(class_list[j][0]) +')'
            x = x.replace('id:','need')
            CQL_needs_to_subneeds.append(x)

"""-------------------------------------------------------------------------"""
"""Write text file"""
"""-------------------------------------------------------------------------"""
CQL_needs = CQL_firehd_needs + CQL_ipad_needs + CQL_samsung_needs
CQL_total = CQL_needs + CQL_tags + CQL_subneeds + CQL_tags_to_needs + CQL_needs_to_subneeds


with open('CQL_input.txt', 'w') as f:
    for item in CQL_total:
        f.write("%s\n" % item)


"""-------------------------------------------------------------------------"""
"""Delete variables which are not used"""
"""-------------------------------------------------------------------------"""
del i
del line
del x
del X
del item
del j
del j_line
del files_names
del CQL_firehd_needs
del CQL_ipad_needs
del CQL_samsung_needs
del tag_list_1
del A
del B
del C