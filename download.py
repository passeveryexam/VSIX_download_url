from generate_vsix_url import (
    generate_vscode_extension_url as generate_vsix_url
)
import requests
from tqdm import tqdm


vsix_info = """
Identifier
ms-vscode.cpptools
Version
1.25.3
"""


def parse_vsix_info(info: str, platform: str = None):
    info_dict = dict(
        zip(
            map(str.lower, info.strip().split('\n')[::2]),
            info.strip().split('\n')[1::2]
        )
    )
    identifier = info_dict['identifier']
    version = info_dict['version']
    if platform:
        return f"{identifier}-{version}-{platform}.vsix"
    return f"{identifier}-{version}.vsix"


def download_file(url: str, filename: str = None):
    if filename is None:
        filename = url.split('/')[-1]

    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))

    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            pbar.update(size)

    return filename


try:
    platform = 'linux-x64'
    url = generate_vsix_url(vsix_info, platform=platform)
    print(f"下载URL为: {url}")
    filename = parse_vsix_info(vsix_info, platform=platform)
    filename = download_file(url, filename)
    print(f"下载完成！文件保存为: {filename}")
except Exception as e:
    print(f"错误: {str(e)}")
