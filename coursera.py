from lxml import etree
from bs4 import BeautifulSoup
from openpyxl import Workbook
from collections import OrderedDict
import re
import requests
import random


def get_coursera_courses_list(quantity):
    coursera_sitemap_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    courses_text_response = requests.get(coursera_sitemap_url).text
    courses_xml_data = etree.fromstring(courses_text_response.encode('utf-8'))
    courses_list = [loc_tag_data.text
                    for url_tag_data in courses_xml_data.getchildren()
                    for loc_tag_data in url_tag_data.getchildren()]
    return random.sample(courses_list, quantity)


def get_course_info(course_url):
    course_text_response = requests.get(course_url).content
    course_parser = BeautifulSoup(course_text_response, 'html.parser')
    coursera_course_name = course_parser.find('h1', {'class': 'title'}).text
    coursera_course_language = re.findall('^[a-zA-Z]+', course_parser.find('div', {'class': 'rc-Language'}).text)[0]
    try:
        coursera_course_rating = re.findall('[\d.]+', course_parser.find('div', {'class': 'ratings-text'}).text)[0]
    except AttributeError:
        coursera_course_rating = ''
    try:
        coursera_course_start_date = course_parser.find('div', {'class': 'rc-StartDateString'}).text
    except:
        coursera_course_start_date = ''
    try:
        coursera_course_duration = course_parser.find('td', {'class': 'td-data'}).text
    except:
        coursera_course_duration = ''
    parse_results = OrderedDict([
        ('course_name', coursera_course_name),
        ('course_language', coursera_course_language),
        ('course_rating', coursera_course_rating),
        ('course_start_date', coursera_course_start_date),
        ('course_duration', coursera_course_duration),
        ('courrse_url', course_url)
    ])
    return parse_results


def output_courses_info_to_xlsx(course_data_dicts_list, output_filepath):
    workbook = Workbook(write_only=True)
    worksheet = workbook.create_sheet()
    is_write_title_row = True
    for course_data in course_data_dicts_list:
        if is_write_title_row:
            worksheet.append(list(course_data.keys()))
            is_write_title_row = False
        worksheet.append(list(course_data.values()))
    try:
        workbook.save(output_filepath)
    except PermissionError:
        print('The program can not write a file with courses')


if __name__ == '__main__':
    course_quantity = 5
    result_file_name = 'result_file.xlsx'
    coursera_courses_url_list = get_coursera_courses_list(course_quantity)
    list_with_courses_data = [get_course_info(course_url) for course_url in coursera_courses_url_list]
    output_courses_info_to_xlsx(list_with_courses_data, result_file_name)
    print('The program recorded data from {} random courses on Coursera.org into file {}'.format(course_quantity, result_file_name))
