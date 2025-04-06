import lxml.etree as ET
import argparse
from pathlib import Path

MSBUILD_NAMESPACE = '{http://schemas.microsoft.com/developer/msbuild/2003}'

tag_ProjectReference = MSBUILD_NAMESPACE + 'ProjectReference'
tag_LinkLibraryDependencies = MSBUILD_NAMESPACE + 'LinkLibraryDependencies'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', type=Path)
    parser.add_argument('project', type=Path)
    args = parser.parse_args()
    if not args.output:
        args.output = args.project
    modified = False

    tree = ET.parse(args.project)
    for pr in [e for e in tree.iter() if e.tag == tag_ProjectReference]:
        if (lld := pr.find(tag_LinkLibraryDependencies)) is not None:
            if lld.text == 'true':
                continue
        else:
            lld = ET.Element(tag_LinkLibraryDependencies)
            pr.append(lld)
        lld.text = 'true'
        modified = True

    if modified:
        buf = ET.tostring(tree, pretty_print=True, encoding='utf-8').decode('utf-8').replace('/>', ' />')
        with args.output.open('wt', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write(buf)

if __name__ == '__main__':
    main()
