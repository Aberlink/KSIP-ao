import re


def remove_empty_lines(file_path):
    text = ''
    with open(file_path,'r+') as f:
        for line in f:
            if len(line) > 1 or line != '\n':
                text += line
    return text


def split_paragraps(text):
    re.purge()
    text = text.replace(".", "")
    art_remove = re.sub('(?i)(\W*|\w{1})(art|att)(\.|,)?\s*', '\n', text)  #art remove
    kpe_kpc = re.sub('(kpe|kpo)', 'kpc', art_remove)
    ke_kc = re.sub('(ke|kic)', 'kc', kpe_kpc)
    w_zw_z = re.sub('(?i)(\sw|\s)(\s|z)(zw|w)($z|\sz)', ' ', ke_kc)  #w zw. z remove
    w_zw_z = re.sub('(?i)(wzw|zw|wz|wzwz)', ' ', w_zw_z)  #w zw. z remove
    i_oraz = re.sub('(?i)\si\n|\soraz\n', ' ', w_zw_z)
    one_berween_nums = re.sub('(?i)\d\s(1|i|l)\s\d', ' ', i_oraz)
    cap_i_to_one = re.sub('I\s', '', one_berween_nums)
    dollar = re.sub('(?i)\s\$\s(\d*|\w)\s*', ' ', cap_i_to_one)
    dollar_with_num = re.sub('(?i)\$\d', ' ', dollar)
    dollar_solo = re.sub('\$', '', dollar_with_num)
    ust = re.sub('(?i)(ustawy|ust|pkt)\s?\d*', ' ', dollar_solo)
    ust = re.sub('(?i)(ustawy|ust|pkt)\s?\d*', ' ', ust)
    contrario = re.sub('(?i)contrario', ' ', ust)
    single_letter = re.sub('\s([a-zA-Z]|li|il)\s', ' ', contrario)
    single_letter = re.sub('\s([a-zA-Z]|li|il|la)\s', ' ', single_letter)
    interpunctors = re.sub('[!?|,\']', '', single_letter)
    single_num_inside = re.sub('\s\d\s', ' ', interpunctors)
    multi_space = re.sub('\ {2,}', ' ', single_num_inside)
    multi_space = multi_space.lower()
    # print(multi_space)
    
    clean_line = multi_space[1:]
    
    return clean_line

def detect_commons(text):
    # print(text)
    commons = text.replace('\n', ' ')
    commons = re.findall('(\d{1,4}(\ |-\d{0,3}\ |\w\ )\w{2,4}\s)', commons)
    commons_paragraphs = [x[0][:-1] for x in commons]
    return commons_paragraphs


def save_txt_file(text, path):
    with open(path,'w') as f:
        for line in text:
            f.write(line)


def get_exam_questions(path):
    text = remove_empty_lines(path)
    text = split_paragraps(text)          
    commons = detect_commons(text)  
    return commons


if __name__ == '__main__':
    EXAM_2012 = get_exam_questions('txts_manual/2012.txt')
    # print(EXAM_2012)