#!/usr/bin/env python3

import os
import sys
import requests
import xml.etree.ElementTree as ET

if len(sys.argv) != 3:
    print(f"Usage:\n\t./{os.path.basename(sys.argv[0])} <vendor-tag> <qssi-tag>")
    sys.exit(1)

vendor_tag, qssi_tag = sys.argv[1], sys.argv[2]

manifests = {
    "audio": "https://git.codelinaro.org/clo/la/techpack/audio/manifest",
    "camera": "https://git.codelinaro.org/clo/la/techpack/camera/manifest",
    "cv": "https://git.codelinaro.org/clo/la/techpack/cv/manifest",
    "display": "https://git.codelinaro.org/clo/la/techpack/display/manifest",
    "graphics": "https://git.codelinaro.org/clo/la/techpack/graphics/manifest",
    "kernel": "https://git.codelinaro.org/clo/la/kernelplatform/manifest",
    "qssi": "https://git.codelinaro.org/clo/la/la/system/manifest",
    "vendor": "https://git.codelinaro.org/clo/la/la/vendor/manifest",
    "video": "https://git.codelinaro.org/clo/la/techpack/video/manifest",
}

def get_vendor_manifest(tag):
    url = f"https://git.codelinaro.org/clo/la/la/vendor/manifest/-/raw/release/{tag}.xml"
    r = requests.get(url)
    if r.status_code != 200:
        print("Vendor tag does not exist!")
        sys.exit(1)
    return ET.fromstring(r.content)

def get_techpack_tag(name, vendor_root):
    refs = vendor_root.find('refs')
    if refs is not None:
        for image in refs:
            project = image.get('project')
            if (name == "kernel" and project == "kernelplatform/manifest") or \
               (project == f"techpack/{name}/manifest"):
                return image.get('tag')
    return None

def resolve_tag(name, vendor_root):
    return qssi_tag if name == "qssi" else vendor_tag if name == "vendor" else get_techpack_tag(name, vendor_root) or vendor_tag

os.makedirs("snippets", exist_ok=True)

vendor_root = get_vendor_manifest(vendor_tag)

for name, base_url in manifests.items():
    resolved_tag = resolve_tag(name, vendor_root)
    url = f"{base_url}/-/raw/release/{resolved_tag}.xml"
    dest = f"{name}.xml" if name == "qssi" else f"snippets/{name}.xml"
    r = requests.get(url)
    if r.status_code != 200:
        url = f"{base_url}/-/raw/refs/tags/{resolved_tag}.xml"
        r = requests.get(url)

    if r.status_code == 200:
        with open(dest, "wb") as f:
            f.write(r.content)
        print(f"{name} updated from: {resolved_tag}")
    else:
        print(f"Failed to update {name} manifest...")
