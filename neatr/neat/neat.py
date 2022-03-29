import logging

from dataclasses import dataclass
from typing import List
from pathlib import Path
from datetime import datetime, date, timezone
from uuid import UUID
from pathlib import Path
import traceback
from os import utime
from calendar import timegm
import re

from pdfrw import PdfReader, PdfWriter   
import sqlite3

from neatr.neat.queries import DOCUMENTS, RECEIPTS, IMAGES
from neatr.neat.constants import TAG_MAPPING

DATABASE: Path = Path('/tmp/neatr/neat.db')
OUTPUT: Path = Path('/tmp/neatr')
DEFAULT_DATE: date = datetime.strptime('1970-01-01', '%Y-%m-%d').date()
DEFAULT_STRING: str = ''
DEFAULT_TAG: str = 'ZZ'
COUNT: int = 7582

@dataclass(frozen=True)
class Environment:
    database: Path
    path: Path

    @staticmethod
    def default() -> 'Environment':
        database = DATABASE
        path = OUTPUT

        return Environment(
            database,
            path
        )

    @staticmethod
    def create(
        database: Path,
        path: Path
    ) -> 'Environment':
        return Environment(
            database,
            path
        )


@dataclass(frozen=True)
class Page:
    id: UUID
    image: bytes


class Processor():

    def __init__(
        self,
    ) -> None:
        self._environment = Environment.default()

    def set_environment(
        self,
        environment: Environment
    ) -> None:
        self._environment = environment

    def extract_documents(
        self
    ) -> None:

        connection = sqlite3.connect(self._environment.database)
        try:
            documents = connection.execute(DOCUMENTS).fetchall()
            for row in documents:
                id = UUID(row[0])
                self._save( id, self._pages(id, connection))
        finally:
            connection.close()

    def extract_receipts(
        self
    ) -> None:

        connection = sqlite3.connect(self._environment.database)
        try:
            receipts = connection.execute(RECEIPTS).fetchall()
            for row in receipts:
                id = UUID(row[0])
                self._save( id, self._pages(id, connection))
        finally:
            connection.close()

    def process_documents(
        self
    ) -> None:

        connection = sqlite3.connect(self._environment.database)
        try:
            documents = connection.execute(DOCUMENTS).fetchall()

            count = 0

            for row in documents:
                id = UUID(row[0])
                date = self._default_date(row[1])
                author = self._default_string(row[2])
                title = self._default_string(row[3])
                tag = self._default_tag(row[4])
                count = count + 1
                name = "{}_{}_{}_{}.pdf".format(date.strftime('%Y%m%d'), tag, author, f'{count + COUNT:08}')

                self._process(id, date, author, title, name)

            logging.info('Processed {} documents'.format(count))
        finally:
            connection.close()

    def process_receipts(
        self
    ) -> None:

        connection = sqlite3.connect(self._environment.database)
        try:
            receipts = connection.execute(RECEIPTS).fetchall()

            count = 0

            for row in receipts:
                id = UUID(row[0])
                date = self._default_date(row[1])
                author = self._default_string(row[2])
                title = self._receipt_title(author, row[3])
                tag = self._default_tag(row[4])
                count = count + 1
                name = "{}_{}_{}_{}.pdf".format(date.strftime('%Y%m%d'), tag, author, f'{count + COUNT:08}')

                self._process(id, date, author, title, name)

            logging.info('Processed {} receipts'.format(count))
        finally:
            connection.close()


    def _process(
        self,
        id: UUID,
        date: date,
        author: str,
        title: str,
        name: str
    ) -> None:
        pdf_file = self._environment.path.joinpath(str(id) + ".pdf")
        if pdf_file.is_file():
            pdf = PdfReader(pdf_file)
            pdf.Info.Author = author
            pdf.Info.Producer = "Neat 5.7.1_474"
            pdf.Info.Title = title
            pdf.Info.Subject = str(id)
            pdf.Info.CreationDate = "D:{}000000Z".format(date.strftime('%Y%m%d'))
                        
            renamed = self._environment.path.joinpath(name)
            PdfWriter(renamed, trailer=pdf).write()
            created = timegm(date.timetuple())
            utime(renamed, (created, created))
            pdf_file.unlink()

    def _pages(
        self,
        id: UUID,
        connection: sqlite3.Connection
    ) -> List[Page]:

        return [Page(UUID(image[0]), image[1]) for image in connection.execute(IMAGES, (str(id),)).fetchall()]

    def _save(
        self,
        id: UUID,
        pages: List[Page]
    ) -> None:
        if not pages:
            logging.warn('Target {} has no pages'.format(str(id)))
            return

        index_file = self._environment.path.joinpath(str(id) + ".txt")
        if index_file.is_file():
            logging.warn('Target {} already exists'.format(index_file))
            return
        
        image_list = []
        for page in pages:
            image_file = self._environment.path.joinpath(str(page.id))
            with open(image_file, 'wb') as file:
                file.write(page.image)
                image_list.append(str(page.id))
        
        with open(index_file, 'w') as file:
            for image_file in image_list:
                print(f"{image_file}", file=file)
    
    @staticmethod
    def _default_date(
        date: str
    ) -> date:
        if date:
            return datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f").date()
        return DEFAULT_DATE

    @staticmethod
    def _default_string(
        value: str
    ) -> str:
        if value:
            return re.sub('\?|\_|\!|\/|\;|\:', ' ', value)
        return DEFAULT_STRING

    @staticmethod
    def _receipt_title(
        author: str,
        value: str
    ) -> str:
        if author:
            if value:
                return "Receipt from " + author + " for " + str(value)
            return "Receipt from " + author
        return "Receipt"

    @staticmethod
    def _default_tag(
        value: str
    ) -> str:
        if not value:
            return DEFAULT_TAG
        return TAG_MAPPING.get(value, DEFAULT_TAG)
