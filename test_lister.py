import os
import re
import base64
from PIL import Image, ImageOps
from html import HTML
from github import Github


GITHUB_REPO = 'mozilla-mobile/fenix'
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
PATH_UI_TESTS = 'app/src/androidTest/java/org/mozilla/fenix/ui'
PATH_ROBOTS = '{0}/robots'.format(PATH_UI_TESTS)


if(GITHUB_TOKEN):
    g = Github(GITHUB_TOKEN)
else:
    g = Github()
repo = g.get_repo(GITHUB_REPO)


def robot_list():
    filenames = repo.get_contents(PATH_ROBOTS)
    #for f in filenames:
    #    print(f.path)
    robots = []
    for f in filenames:
        name_robot = f.path.split(PATH_ROBOTS)[1].split('/')[1]
        name_robot = name_robot.split('.kt')[0].split('Robot')[0]
        robots.append(name_robot)
    return robots 


def test_list():
    filenames = repo.get_contents(PATH_UI_TESTS)
    tests = []
    for f in filenames:
        if f.type == 'file':
            name_test = f.path.split(PATH_UI_TESTS)[1].split('/')[1]
            t =test_parser_get_transitions(name_test)
            #print(t)
            name_test = name_test.split('.kt')[0].split('Test')[0]
            tests.append([name_test, t])
    return tests 


def test_parser_get_testnames(test_name):
    contents = repo.get_contents('{0}/BookmarksTest.kt'.format(PATH_UI_TESTS))
    tests = []
    try:
        lines = base64.b64decode(contents.content)
        lines = lines.split('\n')
        flag = False
        line_count = 1
        tests = []
        for line in lines: 
            if flag:
                line = line.split('fun ')[1].split('(')[0]
                test = [line_count, line]
                url = test_url(test)
                tests.append(test)
                print(url)
                flag = False
            if '@Test' in line:
                flag = True
            line_count += 1
    except AttributeError:
        pass
    return tests

def test_parser_get_transitions(test_name):
    contents = repo.get_contents('{0}/{1}'.format(PATH_UI_TESTS, test_name))
    sorted_transitions = []
    try:
        lines = base64.b64decode(contents.content)
        lines = lines.split('\n')
        tests = []
        for line in lines: 
            match = re.findall("(^\s*\}\.)(\w+)( \{)", line)

            if match:
                if len(match) > 0:
                    tests.append(match[0][1])
        sorted_transitions = sorted(set(tests), reverse=True)
    except AttributeError:
        return []

    print('---------')
    print('TEST NAME: {0}'.format(test_name))
    print(sorted_transitions)
    print('---------')
    return sorted_transitions 


def create_robot_test_links():
    # robot_list = [ROBOT_NAME, [list_of_test_names]] 
    # need list of robots
    # test_list = [ test_name, [transition_names]]
    pass

def test_url(test):
    line_num, test_name = test[0], test[1]
    return 'https://github.com/{0}/blob/master/{1}/{2}.kt#{3}'.format(GITHUB_REPO, PATH_UI_TESTS, test_name, line_num)


def tests_for_robot(robot_name):
    pass


def border_image():
    for i in list-of-images:
      img = Image.open(i)
      img_with_border = ImageOps.expand(img,border=IMG_BORDER_SIZE,fill='black')
      img_with_border.save('bordered-%s' % i)


def num_rows(num_cols):
    robots = robot_list()
    num_screenshots = len(robots)

    num_rows = num_screenshots / num_cols
    extra_cols = num_screenshots - (num_rows * num_cols)
    if extra_cols > 0:
        num_rows += 1
    return num_rows 


def write_file(html_content, out_filename='report.html'):
    with open(out_filename, 'w') as out_file:
        out_file.write(html_content)


def main(num_cols=4):
    robots = robot_list()
    rows = num_rows(num_cols) 
    h = HTML('html', 'text')
    t = h.table(border='2')

    ui_count = 0
    num_robots = len(robots)
    for i in range(rows):
        # image row
        r = t.tr
        for j in range(num_cols):
            if ui_count < num_robots:
                ui_count +=1

if __name__ == "__main__":
    #main()
    #test_parser_get_transitions()
    #test_parser_get_testnames()
    t = test_list()
    print(t)
    
    #test_list_transitions()
 

