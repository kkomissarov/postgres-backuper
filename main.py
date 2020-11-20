import os
import uuid
import datetime
import logging.config
import logging
from typing import List

from dotenv import load_dotenv

from logger_config import LOGGER_CONFIG

DEFAULT_BACKUPS_LIMIT = 10

load_dotenv()
logger = logging.getLogger('main')
logging.config.dictConfig(LOGGER_CONFIG)


def get_full_backup_path(db_name):
    current_datetime = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    filename = f'{current_datetime}-{db_name}-{uuid.uuid4()}.backup'
    storage = os.getenv('BACKUP_STORAGE')
    full_path = os.path.join(storage, filename)
    return full_path


def create_backup(user, password, host, port, db_name):
    backup_path = get_full_backup_path(db_name)
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    os.system(f'pg_dump --dbname=postgresql://{user}:{password}@{host}:{port}/{db_name} > {backup_path}')
    logger.info(f'New backup was created: {backup_path}')


def get_files_to_modtimes_map(file_path_list: List[str]) -> List[dict]:
    files_to_modtimes_map = []
    for filepath in file_path_list:
        file_to_mtime = {
            'path': filepath,
            'modtime': os.stat(filepath).st_mtime
        }
        files_to_modtimes_map.append(file_to_mtime)
    files_to_modtimes_map.sort(key=lambda x: -x['modtime'])
    return files_to_modtimes_map


def get_backup_count_limit():
    try:
        backup_count_limit = int(os.getenv('BACKUP_COUNT_LIMIT'))
    except:
        backup_count_limit = DEFAULT_BACKUPS_LIMIT
    return backup_count_limit


def remove_old_backups():
    storage_path = os.getenv('BACKUP_STORAGE')
    all_backups = [os.path.join(storage_path, filename) for filename in next(os.walk(storage_path))[-1]]
    backup_count_limit = get_backup_count_limit()
    if len(all_backups) > backup_count_limit:
        files_to_modtimes_map = get_files_to_modtimes_map(all_backups)
        for element in files_to_modtimes_map[backup_count_limit:]:
            os.remove(os.path.join(storage_path, element['path']))
            logger.info(f'Old backup was removed: {element["path"]}')


if __name__ == '__main__':
    create_backup(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        db_name=os.getenv('DB_NAME')
    )

    remove_old_backups()
