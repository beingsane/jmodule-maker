"""
Import library
"""
import datetime
import calendar
import os
import shutil

from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from django.http import JsonResponse
from django.conf import settings

"""
Index Main page
"""
def index(request):
    template = loader.get_template('app/index.html')
    context = {
        'author': 'ITS HOBS Enterprise',
        'header': 'JModule Creator Service'
    }
    return HttpResponse(template.render(context, request))

"""
Get current date
"""
def get_currentdate():
    now = datetime.datetime.now()
    datenow = {}
    datenow['year'] = str(now.year)
    datenow['month'] = str(calendar.month_name[now.month])
    datenow['day'] = str(now.day)
    datenow['time'] = str(now.time)

    return datenow

"""
Generate manifest
"""
def gen_manifest(data):
    STORAGE_TMP = settings.BASE_DIR + '/storage/template'
    STORAGE_MODULE = settings.BASE_DIR + '/storage/module'
    FILE = STORAGE_TMP + '/mod_template.xml'
    date = get_currentdate()
    editable_data = {
        'mod_tmp': 'mod_' + data['module_name'].lower(),
        'author_tmp': data['author'],
        'description_tmp': data['description'],
        'version_tmp': data['version'],
        'name_tmp': data['module_name'].title(),
        'year_tmp': date['year'],
        'datecreated_tmp': date['month'] + " " + date['year']
    }

    with open(FILE) as infile, open(STORAGE_MODULE + '/mod_'+ data['module_name'].lower() +'.xml', 'w') as outfile:
        for line in infile:
            for src, target in editable_data.items():
                line = line.replace(src, target)
            outfile.write(line)

    return True

"""
Generate root
"""
def gen_root(data):
    STORAGE_TMP = settings.BASE_DIR + '/storage/template'
    STORAGE_MODULE = settings.BASE_DIR + '/storage/module'
    FILE = STORAGE_TMP + '/mod_template.php'
    date = get_currentdate()
    editable_data = {
        'mod_tmp': 'mod_' + data['module_name'].lower(),
        'author_tmp': data['author'],
        'version_tmp': data['version'],
        'NameTmp': data['module_name'].title(),
        'year_tmp': date['year']
    }

    with open(FILE) as infile, open(STORAGE_MODULE + '/mod_'+ data['module_name'].lower() +'.php', 'w') as outfile:
        for line in infile:
            for src, target in editable_data.items():
                line = line.replace(src, target)
            outfile.write(line)

    return True

"""
Generate helper
"""
def gen_helper(data):
    STORAGE_TMP = settings.BASE_DIR + '/storage/template'
    STORAGE_MODULE = settings.BASE_DIR + '/storage/module'
    FILE = STORAGE_TMP + '/helper.php'
    date = get_currentdate()
    editable_data = {
        'mod_tmp': 'mod_' + data['module_name'].lower(),
        'author_tmp': data['author'],
        'version_tmp': data['version'],
        'NameTmp': data['module_name'].title(),
        'year_tmp': date['year']
    }

    with open(FILE) as infile, open(STORAGE_MODULE + '/helper.php', 'w') as outfile:
        for line in infile:
            for src, target in editable_data.items():
                line = line.replace(src, target)
            outfile.write(line)

    return True

"""
Generate default
"""
def gen_default(data):   
    STORAGE_TMP = settings.BASE_DIR + '/storage/template/tmpl'
    STORAGE_MODULE = settings.BASE_DIR + '/storage/module/tmpl'
    FILE = STORAGE_TMP + '/default.php'
    date = get_currentdate()

    if not os.path.exists(STORAGE_MODULE):
        os.makedirs(STORAGE_MODULE)

    editable_data = {
        'mod_tmp': 'mod_' + data['module_name'].lower(),
        'author_tmp': data['author'],
        'version_tmp': data['version'],
        'year_tmp': date['year']
    }

    with open(FILE) as infile, open(STORAGE_MODULE + '/default.php', 'w') as outfile:
        for line in infile:
            for src, target in editable_data.items():
                line = line.replace(src, target)
            outfile.write(line)

    return True

"""
Copy remaining files
"""
def gen_remaining():
    STORAGE_TMP = settings.BASE_DIR + '/storage/template'
    STORAGE_MODULE = settings.BASE_DIR + '/storage/module'

    # Index
    shutil.copyfile(STORAGE_TMP + '/index.php', STORAGE_MODULE + '/index.php')
    shutil.copyfile(STORAGE_TMP + '/tmpl/index.php', STORAGE_MODULE + '/tmpl/index.php')
    return True

"""
Generate  Loop
"""
def start_gen(data):
    MEDIA_URL = '/media/download'
    MEDIA_PATH = settings.BASE_DIR + MEDIA_URL
    STORAGE_MODULE = settings.BASE_DIR + '/storage/module'

    """
    Reset Module directory
    """
    if os.path.exists(STORAGE_MODULE):
        shutil.rmtree(STORAGE_MODULE)
        os.makedirs(STORAGE_MODULE)

    """
    Reset Download directory
    """
    for filename in os.listdir(MEDIA_PATH):
        filepath = MEDIA_PATH + "/" + filename
        os.remove(filepath)

    files = ['manifest', 'root', 'helper', 'default', 'index']
    result = {}
    for case in files:
        if case == "manifest":
            gen_manifest(data)
        elif case == "root":
            gen_root(data)
        elif case == "helper":
            gen_helper(data)
        elif case == "default":
            gen_default(data)
        else:
            gen_remaining()

    # Archive folder
    generated_filename = "/mod_" + data['module_name'].lower()
    shutil.make_archive(MEDIA_PATH +  generated_filename, 'zip', STORAGE_MODULE)

    # Download URL
    result['url'] = MEDIA_URL + generated_filename + '.zip'

    return JsonResponse(result)

"""
Generate request
"""
def generate(request):
    # Filter Request Method
    if request.method == 'GET':
        # Access Forbidden
        return HttpResponseForbidden('Access Denied')
    else:
        data = {}
        module_name = request.POST['module_name']
        data['module_name'] = module_name.replace(' ', '')
        data['author'] = request.POST['author']
        data['description'] = request.POST['description']
        data['version'] = request.POST['version']
        return start_gen(data)