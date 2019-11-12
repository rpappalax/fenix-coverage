"""Generates Fenix UI Test automation coverage report

Unlike unit tests, it's hard to give a black and white percent coverage for UI test automation.
Hence, we use UI screenshots of each Fenix UI to show what is covered by UI tests and what isn't
Green border - Tests exist
Red border - tests exist, but currently disabled
No border - no test coverage yet
"""
import os
import re
import base64
from PIL import Image, ImageOps
from html import HTML
from github import Github


GITHUB_REPO = 'mozilla-mobile/fenix'
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
IMG_BORDER_SIZE = 10
IMG_BORDER_COLOR_EXISTS = 'green'
IMG_BORDER_COLOR_DOESNT_EXIST = 'white'
IMG_BORDER_COLOR_DISABLED = 'red'
CELL_BGCOLOR_EMPTY = 'grey'
PATH_UI_TESTS = 'app/src/androidTest/java/org/mozilla/fenix/ui'
PATH_ROBOTS = '{0}/robots'.format(PATH_UI_TESTS)


if(GITHUB_TOKEN):
    g = Github(GITHUB_TOKEN)
else:
    g = Github()
repo = g.get_repo(GITHUB_REPO)


def add_img_border(img_name, img_border_color):
    # 1080 1920
    img_path_in = 'screenshots/{0}.png'.format(img_name)
    img_path_out = 'images/{0}.png'.format(img_name)
    img = Image.open(img_path_in)
    img_with_border = ImageOps.expand(img,border=IMG_BORDER_SIZE,fill=img_border_color)
    img_with_border.save(img_path_out)
    pass


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
    contents = repo.get_contents('{0}/BookmarksTest.kt'.format(PATH_UI_TESTS))
    lines = base64.b64decode(contents.content)
    lines = lines.split('\n')
    flag = False
    line_count = 1
    tests = []
    for line in lines: 
        if flag:
            #tests = tests.append([line_count, line])
            #tests = tests.append(line)
            line = line.split('fun ')[1].split('(')[0]
            test = [line_count, line]
            url = test_url(test)
            tests.append(test)
            print(url)
            flag = False
        if '@Test' in line:
            flag = True
        line_count += 1
    print(tests)


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


def img_border_color():
    import random
    border_color = IMG_BORDER_COLOR_DOESNT_EXIST 
    border_color = IMG_BORDER_COLOR_EXISTS
    border_color = IMG_BORDER_COLOR_DISABLED

    border_color = random.choice([IMG_BORDER_COLOR_DOESNT_EXIST , IMG_BORDER_COLOR_EXISTS, IMG_BORDER_COLOR_DISABLED])
    return border_color 


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
                img_name = robots[ui_count]
                img_border = img_border_color()
                add_img_border(img_name, img_border) 
                dummy = 'https://github.com/mozilla-mobile/fenix/blob/master/app/src/androidTest/java/org/mozilla/fenix/ui/BookmarksTest.kt#L97'
                r.td.img(width="100%", src="./images/{0}.png".format(img_name)).br.a('BookmarksTest', href=dummy, target='_blank').br.a('AnotherTest', href=dummy).br.a('YetAnother', href=dummy)
            else:
                r.td(bgcolor=CELL_BGCOLOR_EMPTY)
            ui_count +=1
    write_file(str(h))


if __name__ == "__main__":
    main()
    #test_list()
 

