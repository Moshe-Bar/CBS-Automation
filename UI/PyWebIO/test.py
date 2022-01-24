from pywebio.input import checkbox

from Utility.TestUtility import TestUtility

total_pages = TestUtility.get_he_pages()
pages = list(map(lambda page: {'label': page.name, 'value': page.id, 'selected': True}, total_pages))
pages = checkbox(name='ChoosePages', label='Chose_pages', options=pages)
chosen_pages = list(filter(lambda x: x.id in pages, total_pages))
print(chosen_pages)