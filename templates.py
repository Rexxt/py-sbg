from typing import Any


def HTML5(lang='en', header='', body=''):
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {header}
</head>
<body>
    {body}
</body>
</html>'''

class CommonHTML5:
    def __init__(self, stylesheets=[]):
        """Generate new HTML5-based template with common files.
        """
        self.stylesheets = stylesheets
    
    def generate_styles(self):
        s = ''
        for style in self.stylesheets:
            s += f'<link rel="stylesheet" href="{style}">'
        return s
    
    def __call__(self, lang='en', header='', body=''):
        return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {self.generate_styles()}
    {header}
</head>
<body>
    {body}
</body>
</html>'''