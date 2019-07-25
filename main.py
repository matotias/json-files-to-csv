import json
import os
import csv
from flatten import flatten


def get_all_headers(json_array):
    headers = []

    for row in json_array:
        candidate_headers = row.keys()
        for value in candidate_headers:
            if value not in headers:
                headers.append(value)
    return headers


def merge_json_files(path):
    data = []
    for file in os.listdir(path):
        with open(path+'/'+file, encoding='utf-8') as f:
            json_object = json.load(f)
            for row in json_object:
                data.append(flatten(row))
    return data


def prepare_writer(file, headers):
    writer = csv.DictWriter(file, fieldnames=headers,
                            lineterminator='\n')
    writer.writeheader()
    return writer


def prepare_file(file, data, extra_header):
    headers = get_all_headers(data)
    headers.insert(0, extra_header)
    writer = prepare_writer(file, headers)
    return writer


path = './files'
data = merge_json_files(path)


with open('profiles.csv', 'w', encoding='utf-8') as profiles_file, open(
        'jobs.csv', 'w', encoding='utf-8') as jobs_file, open(
        'skills.csv', 'w', encoding='utf-8') as skills_file:

    profiles_writer = prepare_file(profiles_file, data, 'id')
    jobs_writer = prepare_file(jobs_file, data[0]['jobs'], 'profile_id')
    skills_writer = prepare_file(skills_file, data[0]['skills'], 'profile_id')

    for index, row in enumerate(data, 1):
        row['id'] = index
        profiles_writer.writerow(row)
        for job in (row.get('jobs') or []):
            job['profile_id'] = index
            jobs_writer.writerow(job)
        for skill in (row.get('skills') or []):
            skill['profile_id'] = index
            skills_writer.writerow(skill)
