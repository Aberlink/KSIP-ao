import re


def remove_empty_lines(file_path):
    text = ''
    with open(file_path,'r+') as f:
        for line in f:
            if len(line) > 1 or line != '\n':
                text += line
    return text


def split_paragraps(text):
    text = text.replace(".", "")
    art_remove = re.sub('(?i)(\W*|\w{1})art\s*', '\n', text)  #art remove
    w_zw_z = re.sub('(?i)(\sw|\s)(\s|z)(zw|w)($z|\sz|)', '', art_remove)  #w zw. z remove
    i_oraz = re.sub('(?i)\si\n|\soraz\n', '', w_zw_z)
    one_berween_nums = re.sub('(?i)\d\s(1|i|l)\s\d', '\n', i_oraz)
    cap_i_to_one = re.sub('I\s', '', one_berween_nums)
    dollar = re.sub(r'(?i)\s\$\s(\d*|\w)\s*', ' ', cap_i_to_one)
    ust = re.sub(r'(?i)\s(ust|pkt)\s?\d*\s', ' ', dollar)
    ust = re.sub(r'(?i)\s(ust|pkt)\s?\d*\s', ' ', ust)
    l = re.sub(r'\sl\s', ' ', ust)
    
    clean_line = l[1:]
    
    return clean_line

def detect_commons(text):
    commons = text.replace('\n', ' ')
    commons = re.findall(r'(\d{1,4}(\ |-\d{0,3}\ |\w\ )\w{2,4}\s)', commons)
    return commons


def save_txt_file(text, path):
    with open(path,'w') as f:
        for line in text:
            f.write(line)



path = 'txts_manual/2009.txt'
# path = 'txts_readed/2017.txt'

text = remove_empty_lines(path)
text = split_paragraps(text)          
commons = detect_commons(text)
# print(commons[5][0])
[print(x[0]) for x in commons]
save_txt_file(text, f'{path[:-4]}_clean.txt')    


txt = '454 l kc'
# print(re.search(r'\d{1,4}(\ |-\d{0,3}\ |\w\ )\w{2,4}\s', text))