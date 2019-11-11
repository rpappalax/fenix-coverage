from PIL import Image, ImageOps
from html import HTML
import os
import re
from github import Github


GITHUB_REPO = 'mozilla-mobile/fenix'
IMG = './images/Settings.png'
IMG_SIZE = 10
PATH_ROBOTS= 'app/src/androidTest/java/org/mozilla/fenix/ui/robots'


#You can write the same at several lines:


screenshot_names = ['Bookmarks', 'Browser', 'FindInPage', 'History', 'HomeScreen', 'Library', 'LibrarySubMenusMultipleSelectionToolbar', 'NavigationToolbar', 'QuickActionBar', 'Search', 'Settings', 'SettingsSubMenuAbout', 'SettingsSubMenuAccessibility', 'SettingsSubMenuDefaultBrowser', 'SettingsSubMenuSearch', 'SettingsSubMenuTheme', 'ThreeDotMenuBookmarks', 'ThreeDotMenuMain']


def add_img_border():
    # 1080 1920
    img = Image.open(IMG)
    img_with_border = ImageOps.expand(img,border=IMG_SIZE,fill='red')
    img_with_border.save('imaged-with-border.png')
    pass

def robot_list():
    g = Github()
    repo = g.get_repo(GITHUB_REPO)
    filenames = repo.get_contents(PATH_ROBOTS)
    for f in filenames:
        print(f.path)
    robots = []
    for f in filenames:
        name_robot = f.path.split(PATH_ROBOTS)[1].split('/')[1].split('.kt')[0]
        robots.append(name_robot)
    return robots 

def border_image():
    for i in list-of-images:
      img = Image.open(i)
      img_with_border = ImageOps.expand(img,border=IMG_SIZE,fill='black')
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

def write_html(num_cols=4):
    rows = num_rows(num_cols) 
    h = HTML('html', 'text')

    t = h.table(border='1')
    count = 0
    print(len(screenshot_names))

    for i in range(rows):
        r = t.tr
        for j in range(num_cols):
            r.td.img(width="100%", src="./images/{0}.png".format(screenshot_names[count]))
            count +=1
    write_file(str(h))
    print(num_rows(num_cols))

write_html(6)
robot_list()
 

