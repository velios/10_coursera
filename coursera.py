from lxml import etree
from bs4 import BeautifulSoup
from openpyxl import Workbook
from collections import OrderedDict
import re
import requests
import random
import logging
import argparse


logging.basicConfig(level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger()


def configurate_cmd_parser():
    parser_description = ('Script save N courses data to Excel file\n')
    cmd_arguments = argparse.ArgumentParser(description=parser_description)
    cmd_arguments.add_argument('--number_of_courses', '-n', type=int, default=20)
    cmd_arguments.add_argument('--filepath', '-f', type=str, default='result_file.xlsx')
    return cmd_arguments.parse_args()

def get_coursera_courses_list(quantity):
    coursera_sitemap_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    courses_text_response = requests.get(coursera_sitemap_url).text
    courses_xml_data = etree.fromstring(courses_text_response.encode('utf-8'))
    courses_list = [loc_tag_data.text
                    for url_tag_data in courses_xml_data.getchildren()
                    for loc_tag_data in url_tag_data.getchildren()]
    return random.sample(courses_list, quantity)


def get_course_info(course_url):
    logger.info('fetching {} ...'.format(course_url))
    course_text_response = requests.get(course_url).content
    course_parser = BeautifulSoup(course_text_response, 'html.parser')
    tags_processing_data = {
        'course_name': [course_parser.find('h1', class_='title'), None],
        'course_language': [course_parser.find('div', class_='rc-Language'), re.compile(r'^[a-zA-Z]+')],
        'course_start_date': [course_parser.find('div', class_='rc-StartDateString'), None],
        'course_rating': [course_parser.find('div', class_='ratings-text'), re.compile(r'[\d.]+')],
        'course_duration': [course_parser.find('td', class_='td-data'), None]
    }
    parse_course_results = OrderedDict()
    for tag_name, processing_content in tags_processing_data.items():
        tag_content = processing_content[0]
        regexp_expression = processing_content[1]
        if regexp_expression:
            parse_course_results[tag_name] = regexp_expression.search(tag_content.get_text())[0]\
                if tag_content else None
        else:
            parse_course_results[tag_name] = tag_content.get_text()\
                if tag_content else None
    parse_course_results['course_url'] = course_url
    return parse_course_results


def output_courses_info_to_xlsx(course_data_dicts_list, output_filepath):
    if not course_data_dicts_list:
        raise ValueError('Error: There must be at least one course to save')
    workbook = Workbook(write_only=True)
    worksheet = workbook.create_sheet()
    worksheet.append(list(course_data_dicts_list[0].keys()))
    for course_data in course_data_dicts_list:
        worksheet.append(list(course_data.values()))
    workbook.save(output_filepath)


if __name__ == '__main__':
    cmd_arguments = configurate_cmd_parser()
    course_quantity = cmd_arguments.number_of_courses
    result_file_name = cmd_arguments.filepath
    try:
        logger.info('Script start fetch data from {} courses ... '.format(course_quantity))
        coursera_courses_url_list = get_coursera_courses_list(course_quantity)
        list_with_courses_data = [get_course_info(course_url)
                                  for course_url in coursera_courses_url_list]
        output_courses_info_to_xlsx(list_with_courses_data, result_file_name)
        print('The program recorded data from {} '
              'random courses on Coursera.org into file {}'.format(course_quantity, result_file_name))
    except ValueError as error:
        print(error.args[0])
    except PermissionError:
        print('Error: The program can not write a file with courses')
