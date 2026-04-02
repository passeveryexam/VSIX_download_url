from generate_vsix_url import (
    generate_vscode_extension_url as generate_vsix_url,
    parse_vscode_extension_info,
)
import requests
from tqdm import tqdm


vsix_info = """
Identifier
ms-vscode.cpptools
Version
1.25.3
"""



def build_vsix_filename(info: str, platform: str = None):
    identifier, version = parse_vscode_extension_info(info)
    if platform:
        return f"{identifier}-{version}-{platform}.vsix"
    return f"{identifier}-{version}.vsix"



def download_file(url: str, filename: str = None, session: requests.Session = None):
    if filename is None:
        filename = url.rsplit('/', 1)[-1]

    close_session = session is None
    if close_session:
        session = requests.Session()

    try:
        with session.get(url, stream=True, timeout=(5, 60)) as response:
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))

            with open(filename, 'wb') as file, tqdm(
                desc=filename,
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as pbar:
                for data in response.iter_content(chunk_size=64 * 1024):
                    if not data:
                        continue
                    size = file.write(data)
                    pbar.update(size)
    finally:
        if close_session:
            session.close()

    return filename


try:
    platform = 'linux-x64'
    url = generate_vsix_url(vsix_info, platform=platform)
    print(f"下载URL为: {url}")
    filename = build_vsix_filename(vsix_info, platform=platform)
    with requests.Session() as session:
        filename = download_file(url, filename, session=session)
    print(f"下载完成！文件保存为: {filename}")
except Exception as e:
    print(f"错误: {str(e)}")
