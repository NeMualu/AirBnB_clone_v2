#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env, put, run

env.hosts = ["104.196.168.90", "35.196.46.172"]

def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not os.path.isfile(archive_path):
        return False

    file = os.path.basename(archive_path)
    name = os.path.splitext(file)[0]

    if put(archive_path, f"/tmp/{file}").failed:
        return False
    if run(f"rm -rf /data/web_static/releases/{name}/").failed:
        return False
    if run(f"mkdir -p /data/web_static/releases/{name}/").failed:
        return False
    if run(f"tar -xzf /tmp/{file} -C /data/web_static/releases/{name}/").failed:
        return False
    if run(f"rm /tmp/{file}").failed:
        return False
    if run(f"mv /data/web_static/releases/{name}/web_static/* "
           f"/data/web_static/releases/{name}/").failed:
        return False
    if run(f"rm -rf /data/web_static/releases/{name}/web_static").failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run(f"ln -s /data/web_static/releases/{name}/ /data/web_static/current").failed:
        return False
    return True

