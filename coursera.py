from lxml import etree
from bs4 import BeautifulSoup
import re
import requests



def get_coursera_courses_list():
    courses_text_response = requests.get('https://www.coursera.org/sitemap~www~courses.xml').text
    courses_xml_data = etree.fromstring(courses_text_response.encode('utf-8'))
    courses_list = []
    for url_tag_data in courses_xml_data.getchildren():
        for loc_tag_data in url_tag_data.getchildren():
            courses_list.append(loc_tag_data.text)
    return courses_list[:20]


# Зайти на страницу курса и вытащить оттуда
# название, язык, ближайшую дату начала, количество недель и среднюю оценку
def get_course_info(course_url):
    parse_results = []
    course_text_response = requests.get(course_url).content
    course_bs_parser = BeautifulSoup(course_text_response, 'html.parser')
    coursera_course_name = course_bs_parser.find('h1', {'class': 'title'}).text
    coursera_course_language = re.findall('^[a-zA-Z]+', course_bs_parser.find('div', {'class': 'rc-Language'}).text)[0]
    try:
        coursera_course_rating = re.findall('[\d.]+', course_bs_parser.find('div', {'class': 'ratings-text'}).text)[0]
    except AttributeError:
        coursera_course_rating = ''
    try:
        coursera_course_start_date = course_bs_parser.find('div', {'class': 'rc-StartDateString'}).text        
    except:
        coursera_course_start_date = ''
    try:
        coursera_course_duration = course_bs_parser.find('td', {'class': 'td-data'}).text
    except:
        coursera_course_duration = ''
    parse_results.append({
            'course_name': coursera_course_name,
            'course_language': coursera_course_language,
            'course_rating': coursera_course_rating,
            'course_start_date': coursera_course_start_date,
            'course_duration': coursera_course_duration
        })
    return parse_results


def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    # course_info = requests.get('https://www.coursera.org/learn/protools')
    # soup = BeautifulSoup(course_info.text, "html.parser")
    # coursera_xml_data = requests.get('{}/sitemap~www~courses.xml'.format(COURSERA_URL)).text
    # xml_data = etree.parse(coursera_xml_data)
    # print(etree.fromstring(coursera_xml_data))
    # xml_data = etree.fromstring(coursera_xml_data.encode('utf-8'))
    # print(xml_data.find('loc').tag)
    # parseXML(coursera_xml_data)
    # coursera_course_list = get_coursera_courses_list()
    courses_list = get_coursera_courses_list()
    course_info = [ get_course_info(course) for course in courses_list ]

