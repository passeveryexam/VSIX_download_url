def parse_vscode_extension_info(raw_info: str):
    """从原始文本中解析VS Code扩展信息

    Args:
        raw_info: 包含identifier和version的原始文本
    Returns:
        标识符和版本号
    Raises:
        ValueError: 当标识符或版本号缺失时
    """
    lines = [line.strip() for line in raw_info.strip().splitlines() if line.strip()]
    info_dict = dict(zip(map(str.lower, lines[::2]), lines[1::2]))

    try:
        identifier = info_dict['identifier']
    except KeyError:
        raise ValueError("未找到标识符")

    try:
        version = info_dict['version']
    except KeyError:
        raise ValueError("未找到版本号")

    return identifier, version



def generate_vscode_extension_url(raw_info: str, platform=None) -> str:
    """从原始文本生成VS Code扩展下载链接

    Args:
        raw_info: 包含identifier和version的原始文本
        platform: 平台信息
    Returns:
        下载URL
    Raises:
        ValueError: 当标识符格式错误或输入数据格式错误时
    """
    identifier, version = parse_vscode_extension_info(raw_info)

    try:
        publisher, name = identifier.split('.')
    except ValueError:
        raise ValueError("标识符格式错误，应为 'Publisher.Name'")

    base_url = "https://marketplace.visualstudio.com/_apis/public/gallery"
    download_url = f"{base_url}/publishers/{publisher}/vsextensions/{name}/{version}/vspackage"

    if platform:
        download_url += f"?targetPlatform={platform}"

    return download_url



def main():
    raw_info = """
Identifier
ms-vscode.cpptools
Version
1.23.6
"""
    try:
        download_url = generate_vscode_extension_url(raw_info, "linux-x64")
        print(download_url)
    except ValueError as e:
        print(f"错误: {str(e)}")


if __name__ == "__main__":
    main()
