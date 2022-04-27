import requests

"""
request_links = ["link1", "link2", "link3"]

returned result
{'Anime': [['Lupin III Part III', 'Hyōga Senshi Gaislugger', 'Phanton Thief Reinya']], 'City': [['Ar Rutba', 'Port Loko', 'Port Mathurin']]}

"""

def request_user_recommendation(links, i):
    request_json = {"request_links": links, "user": i}
    response = requests.post('http://127.0.0.1:5000/user_recommendation', json=request_json)
    recommendation_dict = {}
    print(response)
    if response.status_code == 200:
        recommendation_dict = response.json()

    return recommendation_dict


request_links1 = ['https://www.investopedia.com/terms/c/cryptocurrency.asp',
                 'https://en.wikipedia.org/wiki/Lionel_Messi',
                 'https://en.wikipedia.org/wiki/Elon_Musk',
                 'https://en.wikipedia.org/wiki/Barack_Obama',
                 'https://en.wikipedia.org/wiki/Ukraine',
                 'https://en.wikipedia.org/wiki/Pacific_Ocean']

request_links2 = ['https://en.wikipedia.org/wiki/Tesla,_Inc.',
                  'https://en.wikipedia.org/wiki/Croissant',
                  'https://en.wikipedia.org/wiki/Republican',
                  'https://en.wikipedia.org/wiki/Elon_Musk',
                  'https://en.wikipedia.org/wiki/Eiffel_Tower',
                  'https://en.wikipedia.org/wiki/Christmas']

request_links3 = ['https://towardsdatascience.com/knowledge-data-science-with-semantics-technologies-ff54e4fe306c',
                  'https://medium.com/starts-with-a-bang/the-simplest-explanation-of-global-warming-ever-2b365aff0c2f',
                  'https://medium.com/starts-with-a-bang/tagged/black-holes',
                  'https://www.investopedia.com/terms/c/cryptocurrency.asp',
                  'https://towardsdatascience.com/tagged/python']

request_links4 = ['https://en.wikipedia.org/wiki/List_of_presidents_of_France',
                  'https://en.wikipedia.org/wiki/Serial_Experiments_Lain',
                  'https://en.wikipedia.org/wiki/Sokuon',
                  'https://en.wikipedia.org/wiki/Katakana',
                  'https://en.wikipedia.org/wiki/Misha_Collins']

request_links5 = ['https://en.wikipedia.org/wiki/Honey,_I_Shrunk_the_Kids_(franchise)',
                  'https://en.wikipedia.org/wiki/Lucius_Fox',
                  'https://en.wikipedia.org/wiki/Mary_Poppins_Returns',
                  'https://en.wikipedia.org/wiki/Josh_Groban',
                  'https://en.wikipedia.org/wiki/71st_Tony_Awards']

request_links6 = ['https://en.wikipedia.org/wiki/Christopher_Plummer',
                  'https://en.wikipedia.org/wiki/Hadestown',
                  'https://en.wikipedia.org/wiki/LaVar_Ball',
                  'https://en.wikipedia.org/wiki/Carvana',
                  'https://en.wikipedia.org/wiki/Brett_Favre']

request_links = [request_links1, request_links2, request_links3, request_links4, request_links5, request_links6]

print(request_user_recommendation(request_links, 4))