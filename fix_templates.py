import glob, re

def update_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new = re.sub(
        r'templates\.TemplateResponse\(\s*([\"\'][^\"\']+[\"\'])\s*,\s*(\{.*?\})\s*\)',
        r'templates.TemplateResponse(request=request, name=\1, context=\2)',
        content,
        flags=re.DOTALL
    )
    
    if new != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        print(f'Updated {path}')

for p in glob.glob('src/janseva/admin/routes/*.py'):
    update_file(p)
