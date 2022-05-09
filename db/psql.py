import psycopg2
import logging

from config import (
    DB_HOST,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

conn = psycopg2.connect(
    dbname=DB_NAME,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD
)


logger = logging.getLogger(__name__)


async def add_company(company_name: str = None):
    if not company_name:
        return 400

    with conn.cursor() as cursor:
        insert = f"INSERT INTO score (company_name, score) VALUES ('{company_name}', 80)"
        cursor.execute(insert)
        conn.commit()

    logger.info(f'Добавили в базу компанию {company_name}')


async def get_score(company_name: str = None):
    logger.info(f'Хотим получить score из базы.'
                 f'Company_name: "{company_name}"')

    if not company_name:
        return 400, 'Не правильное использование команды'

    with conn.cursor() as cursor:
        select = f"SELECT score FROM score WHERE company_name = '{company_name}'"
        cursor.execute(select)

        result = cursor.fetchone()

        if not result:
            return 404, 'Компания не найдена'

        return 200, result[0]


if __name__ == "__main__":
    add_company('company')
    get_score('company')
