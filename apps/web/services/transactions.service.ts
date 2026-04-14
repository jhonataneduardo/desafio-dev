import api from '../lib/api';

export interface ApiTransaction {
  id: number;
  type: number;
  date: string;
  amount: number;
  store_name: string;
  store_owner: string;
  national_id: string; 
  hour: string;
}

export interface UIStoreTransaction {
  id: number;
  typeLabel: string;
  date: string;
  value: number;
  kind: 'credit' | 'debit';
}

export interface UIStoreGroup {
  id: string;
  name: string;
  document: string;
  balance: number;
  operations: UIStoreTransaction[];
}

const TYPE_MAP: Record<number, { label: string; kind: 'credit' | 'debit' }> = {
  1: { label: 'Débito', kind: 'credit' },
  2: { label: 'Boleto', kind: 'debit' },
  3: { label: 'Financiamento', kind: 'debit' },
  4: { label: 'Crédito', kind: 'credit' },
  5: { label: 'Recebimento Empréstimo', kind: 'credit' },
  6: { label: 'Vendas', kind: 'credit' },
  7: { label: 'Recebimento TED', kind: 'credit' },
  8: { label: 'Recebimento DOC', kind: 'credit' },
  9: { label: 'Aluguel', kind: 'debit' },
};

export const transactionsService = {
  async getTransactionsGroupedByStore(): Promise<UIStoreGroup[]> {
    const response = await api.get('/transactions?group_by=store');
    
    // The backend groups data returning an object like: { "Store A": [...transactions], "Store B": [...] }
    const groupedData: Record<string, ApiTransaction[]> = response.data?.data || {};
    const uiGroups: UIStoreGroup[] = [];

    for (const [storeName, transactions] of Object.entries(groupedData)) {
      let balance = 0;
      const operations: UIStoreTransaction[] = [];
      let document = "";

      for (const trx of transactions) {
        if (!document) document = trx.national_id; // Capture store document

        const typeInfo = TYPE_MAP[trx.type] || { label: 'Desconhecido', kind: 'credit' };
        const absValue = Math.abs(trx.amount);
        const val = typeInfo.kind === 'debit' ? -absValue : absValue;

        balance += val;
        operations.push({
          id: trx.id,
          typeLabel: typeInfo.label,
          date: trx.date,
          value: val,
          kind: typeInfo.kind
        });
      }

      uiGroups.push({
        id: storeName,
        name: storeName,
        document: document,
        balance: balance,
        operations: operations
      });
    }

    return uiGroups;
  }
};
