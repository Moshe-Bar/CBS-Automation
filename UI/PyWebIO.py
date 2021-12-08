import json

from pywebio.input import input, FLOAT, CHECKBOX, input_group, NUMBER, actions, TEXT, PASSWORD, select, checkbox, SELECT
from pywebio.output import put_text, put_code

from Utility.TestUtility import TestUtility


def bmi():
    height = input("Input your height(cm)：", type=FLOAT)
    weight = input("Input your weight(kg)：", type=FLOAT)

    BMI = weight / (height / 100) ** 2

    top_status = [(16, 'Severely underweight'), (18.5, 'Underweight'),
                  (25, 'Normal'), (30, 'Overweight'),
                  (35, 'Moderately obese'), (float('inf'), 'Severely obese')]

    for top, status in top_status:
        if BMI <= top:
            put_text('Your BMI: %.1f. Category: %s' % (BMI, status))
            break


def choose_pages():
    pages = TestUtility.get_he_pages()
    pages_input = []
    # for name in pages:
    #     inp = input(name)
    #     pages_input.append(inp)
    #     put_text(name + '\n')
    # list(map(lambda page: input(page.name,required=False), TestUtility.get_he_pages()))
    info = input_group("Pages",
                       [input(page.name) for page in pages
                        ])
    put_code('info = ' + json.dumps(info))


def save_user(param, param1):
    print('user: {}, password: {}'.format(param, param1))


def add_next():
    pass


def a():
    pages = TestUtility.get_he_pages()
    pages = list(map(lambda page: {'label': page.name, 'value': page.name , "selected": True}, pages))
    # page_list = [
    #     {'label': 'Save and add next', 'value': 'save_and_continue'},
    #     {'label': 'Reset', 'value': 'save_and_continue'},
    #     {'label': 'Cancel','value': 'save_and_continue'},
    # ]

    cb = checkbox('Choose pages to test:', options=pages)
    put_code('pages to test = ' + json.dumps(cb, indent=4,ensure_ascii= True))
    print(len(cb))
    # info = input_group('Add user',
    #                    [,
    #                     actions('actions', [
    #                         {'label': 'Next', 'value': 'save'},
    #                         {'label': 'Save and add next', 'value': 'save_and_continue'},
    #                         {'label': 'Reset', 'type': 'reset', 'color': 'warning'},
    #                         {'label': 'Cancel', 'type': 'cancel', 'color': 'danger'},
    #                     ], name='action', help_text='actions'),
    #                    ])
    # put_code('info = ' + json.dumps(info, indent=4))
    # if info is not None:
    #     save_user(info['username'], info['password'])
    #     if info['action'] == 'save_and_continue':
    #         add_next()


if __name__ == '__main__':
    a()
