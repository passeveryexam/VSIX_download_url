from generate_vsix_url import generate_vscode_extension_url as gen_vsix_url


if __name__ == '__main__':
    vsix_info = '''
    Identifier
    vue.volar
    Version
    2.2.8
    '''
    print(f"VSIX URL: {gen_vsix_url(vsix_info)}")
