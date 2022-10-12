import PyPDF2
import re
 

def extract_source_text(path, code):
    with open(path,'rb') as pdffileobj:
        pdfreader = PyPDF2.PdfFileReader(pdffileobj)
        pages = pdfreader.numPages
    for page in range(pages): 
        pageobj=pdfreader.getPage(page)
        text=pageobj.extractText()
        text = text.lower()
    with open(f"soruce/{code}.txt","a") as f:
        f.writelines(text)


def extract_paragraphs_numbers(act_text):
    with open(act_text, 'r') as f:
        text = f.read()
        paragraphs = re.findall('(?i)\n\s?art\.?\ \d*\w*\d?', text)
    paragraphs_nums = [re.search('\d{1,}\w*\d*', paragraph)[0] for paragraph in paragraphs if paragraph != '\n']
    # print(paragraphs_nums)
    return paragraphs_nums


def split_numbers(start, end, digits, paragraphs_nums):
    splited_numbers = []
    for i in range(start, end):
        if len(paragraphs_nums[i]) == digits:
            splited_numbers.append(paragraphs_nums[i])
        else:
            splited = f'{paragraphs_nums[i][:digits]}-{paragraphs_nums[i][digits:]}'
            splited_numbers.append(splited)
    return splited_numbers


def split_nested_paragraphs(paragraphs_nums):
    one_digit = paragraphs_nums.index('10')
    two_digit = paragraphs_nums.index('100')
    try:
        three_digit = paragraphs_nums.index('1000')
    except:
        three_digit = len(paragraphs_nums)
    splited_numbers = []
    splited_numbers.extend(split_numbers(0, one_digit, 1, paragraphs_nums))
    splited_numbers.extend(split_numbers(one_digit, two_digit, 2, paragraphs_nums))
    splited_numbers.extend(split_numbers(two_digit, three_digit, 3, paragraphs_nums))
    splited_numbers.extend(split_numbers(three_digit, len(paragraphs_nums), 4, paragraphs_nums))

    return splited_numbers


def append_code_type(splited_numbers, code):
    paragraphs_type = [f'{x} {code}' for x in splited_numbers]
    return paragraphs_type


def get_code_paragraphs(path, code):
    paragraphs = extract_paragraphs_numbers(path)
    splited_numbers = split_nested_paragraphs(paragraphs)
    typed = append_code_type(splited_numbers, code)
    typed_dict = {}
    for paragraph in typed:
        typed_dict[paragraph] = typed_dict.get(paragraph, 0)
    return typed_dict


if __name__ == '__main__':
    extract_source_text('soruce/D20021270Lj.pdf', 'kpk')


