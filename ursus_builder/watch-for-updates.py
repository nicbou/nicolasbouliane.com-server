#!/usr/bin/env python
# Pulls the latest version of All About Berlin and rebuilds it as needed

from pathlib import Path
from subprocess import run, check_output, STDOUT
from time import sleep
from urllib import request
import json
import logging
import os
import sys


logger = logging.getLogger(__name__)


def purge_cloudflare_cache(cloudflare_zone: str, cloudflare_api_key: str):
    logger.info("Purging Cloudflare cache")
    headers = {
        'Authorization': f'Bearer {cloudflare_api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    data = json.dumps({'purge_everything': True}).encode('utf8')
    req = request.Request(
        f"https://api.cloudflare.com/client/v4/zones/{cloudflare_zone}/purge_cache",
        data=data, headers=headers
    )
    return request.urlopen(req)


def build_site(site_path: Path, cloudflare_zone: str, cloudflare_api_key: str):
    run(['ursus', '-c', site_path / 'ursus_config.py'], check=True, stdout=sys.stdout, stderr=STDOUT)
    if cloudflare_zone and cloudflare_api_key:
        purge_cloudflare_cache(cloudflare_zone, cloudflare_api_key)


def install_ursus(ursus_path: Path):
    logger.info('Installing ursus...')
    run(['pip', 'install', '-e', ursus_path], check=True, stdout=sys.stdout, stderr=STDOUT)


def has_new_commits(repo_path: Path):
    current_branch = check_output(['git', '-C', repo_path, 'branch', '--show-current'], encoding='UTF-8').strip()
    run(['git', '-C', repo_path, 'fetch'], check=True)
    new_commit_count = int(check_output(
        ['git', '-C', repo_path, 'rev-list', f'{current_branch}...origin/{current_branch}', '--count'], encoding='UTF-8'
    ).strip())
    return int(new_commit_count) > 0


def pull(repo_path: Path):
    run(['git', '-C', repo_path, 'pull'], check=True)


if __name__ == '__main__':
    logging.basicConfig(
        datefmt='%Y-%m-%d %H:%M:%S',
        format='[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        level=logging.INFO,
    )

    ursus_repo_url = 'https://github.com/nicbou/ursus.git'
    site_repo_url = os.environ['GIT_REPO_URL']

    cloudflare_zone = os.environ.get('CLOUDFLARE_ZONE')
    cloudflare_api_key = os.environ.get('CLOUDFLARE_API_KEY')

    ursus_path = Path('/usr/lib/ursus')
    site_path = Path('/var/ursus/site')

    if (ursus_path / '.git').exists():
        logger.info("Ursus repo already exists")
    else:
        logger.info("Cloning ursus repo...")
        ursus_path.mkdir(parents=True, exist_ok=True)
        run(['git', 'clone', ursus_repo_url, ursus_path], check=True)

    install_ursus(ursus_path)

    if (site_path / '.git').exists():
        logger.info("Site repo already exists...")
    else:
        logger.info("Cloning site repo...")
        site_path.mkdir(parents=True, exist_ok=True)
        run(['git', 'clone', site_repo_url, site_path], check=True)

    pull(site_path)
    build_site(site_path, cloudflare_zone, cloudflare_api_key)

    while True:
        rebuild_needed = False
        if has_new_commits(ursus_path):
            logger.info("Ursus has changed. Pulling latest version...")
            pull(ursus_path)
            install_ursus(ursus_path)
            rebuild_needed = True

        if has_new_commits(site_path):
            logger.info("Site has changed. Pulling latest version...")
            pull(site_path)
            rebuild_needed = True

        if rebuild_needed:
            build_site(site_path, cloudflare_zone, cloudflare_api_key)

        sleep(60)

