from typing import List

from domain.parsers import CnabParserInterface
from domain.entities import EntityTransaction


class CnabParser(CnabParserInterface):
    
    def parse(self, content: bytes) -> List[EntityTransaction]:
        lines = content.splitlines()
        transactions = []
        for line in lines:
            transaction = EntityTransaction(
                type=int(line[0:1]),
                date=line[1:9],
                amount=float(line[9:19]) / 100,
                national_id=line[19:30].strip(),
                card_number=line[30:42].strip(),
                hour=line[42:48],
                store_owner=line[48:62].strip(),
                store_name=line[62:81].strip()
            )
            transactions.append(transaction)
        return transactions
