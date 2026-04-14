from typing import List
from datetime import datetime

from domain.exceptions import InvalidFileContentException
from domain.parsers import CnabParserInterface
from domain.entities import EntityTransaction

import logging
logger = logging.getLogger(__name__)


class Cnab80Parser(CnabParserInterface):

    def parse(self, content: bytes) -> List[EntityTransaction]:
        logger.info(
            f"Starting CNAB parsing, content size: {len(content)} bytes")
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            raise InvalidFileContentException("File encoding must be UTF-8")

        lines = text.strip().splitlines()
        if not lines:
            raise InvalidFileContentException("CNAB file is empty")

        transactions = []
        for i, line in enumerate(lines, start=1):
            if len(line) < 80:
                raise InvalidFileContentException(
                    f"Line {i} has {len(line)} chars, expected at least 80"
                )
            try:
                transaction = EntityTransaction(
                    type=int(line[0:1]),
                    date=datetime.strptime(line[1:9], "%Y%m%d").date(),
                    amount=float(line[9:19]) / 100,
                    national_id=line[19:30].strip(),
                    card_number=line[30:42].strip(),
                    hour=datetime.strptime(line[42:48], "%H%M%S").time(),
                    store_owner=line[48:62].strip(),
                    store_name=line[62:81].strip(),
                )
                transactions.append(transaction)
            except (ValueError, KeyError) as e:
                raise InvalidFileContentException(
                    f"Error parsing line {i}: {e}"
                )
        logger.info(f"Parsed {len(transactions)} transactions successfully")
        return transactions
