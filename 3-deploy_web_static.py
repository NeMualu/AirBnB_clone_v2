#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ["104.196.168.90", "35.196.46.172"]


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file_name = f"versions/web_static_{dt.year}{dt.month}{dt.day}{dt.hour}{dt.minute}{dt.second}.tgz"
    if not os.path.isdir("versions"):
        if local("mkdir -p versions").failed:
            return None
    if local(f"tar -cvzf {file_name} web_static").failed:
        return None
    return file_name


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not os.path.isfile(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    name = os.path.splitext(file_name)[0]

    if put(archive_path, f"/tmp/{file_name}").failed:
        return False
    if run(f"rm -rf /data/web_static/releases/{name}").failed:
        return False
    if run(f"mkdir -p /data/web_static/releases/{name}").failed:
        return False
    if run(f"tar -xzf /tmp/{file_name} -C /data/web_static/releases/{name}").failed:
        return False
    if run(f"rm /tmp/{file_name}").failed:
        return False
    if run(f"mv /data/web_static/releases/{name}/web_static/* /data/web_static/releases/{name}/").failed:
        return False
    if run(f"rm -rf /data/web_static/releases/{name}/web_static").failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run(f"ln -s /data/web_static/releases/{name}/ /data/web_static/current").failed:
        return False
    return True


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)

