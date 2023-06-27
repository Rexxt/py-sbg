from argparse import ArgumentParser
import markdown as md
from rich import print
import os, json, datetime, dorf
from sys import exit # required for pyinstaller builds

ap = ArgumentParser()
ap.add_argument('-f', '--folder', help='Folder to generate from', required=True)
args = ap.parse_args()

SBG_VERSION = [0, 1, 0, 'alpha']
SBG_VERSION_STR = '.'.join([str(x) for x in SBG_VERSION[:3]]) + ' ' + SBG_VERSION[3]

print(':page_facing_up:', 'SBG version', SBG_VERSION_STR)
if not os.path.isdir(args.folder):
    print(':x:', f'Folder "{args.folder}" does not exist. Generating a blog folder...')
    os.makedirs(f'{args.folder}/public')
    os.makedirs(f'{args.folder}/posts')
    os.makedirs(f'{args.folder}/components/posts')
    with open(f'{args.folder}/sbg.json', 'w') as f:
        f.write('''{
  "import": ["components/header", "components/smallpost"],
  "home": "components/index",
  "directory": "public"
}''')
    print(':white_check_mark:', 'New blog folder ready!')

if not os.path.isfile(f'{args.folder}/sbg.json'):
    print(':x:', f'Folder "{args.folder}" does not have an associated metafile. Generating a metafile...')
    with open(f'{args.folder}/sbg.json', 'w') as f:
        f.write('''{
  "import": ["components/header", "components/smallpost"],
  "home": "components/index",
  "directory": "public"
}''')
    print(':white_check_mark:', 'New metafile ready!')

if not os.listdir(f'{args.folder}/posts'):
    print(':x:', f'Folder "{args.folder}" does not contain any posts. Generating a dummy post...')
    with open(f'{args.folder}/posts/_post_template.md', 'w') as f:
        f.write('---\n'+json.dumps({
            'date': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'title': 'Post template',
            'author': 'SBG',
        })+'\n---')
    print(':white_check_mark:', 'Created post template!')
    print('Write some posts and run this command again to generate a static site.')
    exit()

print(':white_check_mark:', 'Ready to generate posts!')

renderer = dorf.Renderer()

with open(f'{args.folder}/sbg.json') as f:
    config: dict = json.loads(f.read())

for file in config['import']:
    with open(f'{args.folder}/{file}.html') as f:
        renderer.import_components(f.read())

files = []
for f in os.listdir(f'{args.folder}/posts'):
    if not f.startswith('_') and f.endswith('.md') and os.path.isfile(f'{args.folder}/posts/{f}'):
        files.append(f)
sorted_posts = sorted(files, key=lambda t: -os.stat(f'{args.folder}/posts/{t}').st_mtime)

def parse_post(markdown_string):
    header_stat = 0
    header = ''
    file = ''
    for line in markdown_string.split('\n'):
        if header_stat == 0 and line.startswith('---'):
            header_stat = 1
        elif header_stat == 1 and line.startswith('---'):
            header_stat = 2

        elif header_stat == 1:
            header += line
        else:
            file += line + '\n'

    return json.loads(header), md.markdown(file)

posts = {}

with open(f'{args.folder}/components/postpage.html', 'r') as f:
    html_template = f.read()

for file in sorted_posts:
    full_path = f'{args.folder}/posts/{file}'

    with open(full_path, 'r') as f:
        converted_post = parse_post(f.read())
        posts[file] = converted_post
        
        html_file_path = f'{args.folder}/public/posts/' + file.rstrip('.md') + '.html'
        with open(html_file_path, 'w') as f:
            f.write(html_template.format(
                date=datetime.datetime.strptime(converted_post[0]['date'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                title=converted_post[0]['title'],
                author=converted_post[0]['author'],
                content=converted_post[1]
            ))