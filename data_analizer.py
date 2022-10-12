import numpy as np
import matplotlib.pyplot as plt

from data_cleaner import get_exam_questions
from source_reader import get_code_paragraphs  


# KC = get_code_paragraphs('soruce/kc.txt', 'kc')
# KK = get_code_paragraphs('soruce/kk.txt', 'kk')
# KSH = get_code_paragraphs('soruce/ksh.txt', 'ksh')
KPC = get_code_paragraphs('soruce/kpc.txt', 'kpc')
PPSA = get_code_paragraphs('soruce/ppsa.txt', 'ppsa')
KPK = get_code_paragraphs('soruce/kpk.txt', 'kpk')

# print(KPK)

exams = {
"EXAM_2009": get_exam_questions('txts_manual/2009.txt'),
"EXAM_2010": get_exam_questions('txts_manual/2010.txt'),
"EXAM_2012": get_exam_questions('txts_manual/2012.txt'),
"EXAM_2013": get_exam_questions('txts_manual/2013.txt'),
"EXAM_2014": get_exam_questions('txts_manual/2014.txt'),
"EXAM_2015": get_exam_questions('txts_manual/2015.txt'),
"EXAM_2016": get_exam_questions('txts_manual/2016.txt'),
"EXAM_2017": get_exam_questions('txts_manual/2017.txt'),
"EXAM_2018": get_exam_questions('txts_manual/2018.txt'),
"EXAM_2019": get_exam_questions('txts_manual/2019.txt'),
"EXAM_2020": get_exam_questions('txts_manual/2020.txt'),
"EXAM_2021": get_exam_questions('txts_manual/2021.txt'),
}

# print(exams['EXAM_2015'])

def get_common_values(a, b):   
    a_set = set(a)
    b_set = set(b)
    return(a_set.intersection(b_set)) 

def count_paragraphs(code, exam_answers):
    for task in exam_answers:
        code[task] = code.get(task, 0) + 1
    return code


def prepare_cross_years_by_code(code, exams):
    exams_on_code = code.copy()
    for exam in exams.values():
        code_year = get_common_values(exams_on_code.keys(), exam)
        exams_on_code = count_paragraphs(exams_on_code, code_year)
    return exams_on_code




def plot_code_chart(answers_on_code):
    plt.figure(figsize = (20, 8))
    plt.bar(list(answers_on_code.keys()), list(answers_on_code.values()), color ='maroon',
            width = 0.9)
    plt.xticks(np.arange(0, len(answers_on_code), 100))
    plt.yticks(np.arange(0, 10, 1))
    plt.show()



KC_cross_years = prepare_cross_years_by_code(PPSA, exams)
plot_code_chart(KC_cross_years)