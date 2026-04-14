import { useState, useEffect, useCallback } from "react";
import type { Route } from "./+types/home";
import { cnabService } from "../../services/cnab.service";
import { transactionsService, type UIStoreGroup } from "../../services/transactions.service";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Dashboard CNAB" },
    { name: "description", content: "Dashboard de Operações CNAB." },
  ];
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "danger"; text: string } | null>(null);

  const [storeGroups, setStoreGroups] = useState<UIStoreGroup[]>([]);
  const [isLoadingData, setIsLoadingData] = useState(true);

  const fetchTransactions = useCallback(async () => {
    try {
      setIsLoadingData(true);
      const data = await transactionsService.getTransactionsGroupedByStore();
      setStoreGroups(data);
    } catch (err) {
      console.error("Erro ao buscar transações:", err);
    } finally {
      setIsLoadingData(false);
    }
  }, []);

  useEffect(() => {
    fetchTransactions();
  }, [fetchTransactions]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!file) {
      setMessage({ type: "danger", text: "Por favor, selecione um arquivo." });
      return;
    }

    setIsUploading(true);
    setMessage(null);

    try {
      await cnabService.uploadCnab(file);
      setMessage({ type: "success", text: "Upload realizado com sucesso!" });
      setFile(null);
      await fetchTransactions();
    } catch (error) {
      console.error(error);
      setMessage({ type: "danger", text: "Ocorreu um erro ao realizar o upload do arquivo." });
    } finally {
      setIsUploading(false);
    }
  };

  const formatCurrency = (val: number) => 
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);

  const formatDate = (date: string) => 
    new Date(date).toLocaleDateString('pt-BR');

  return (
    <div className="bg-light min-vh-100 py-5">
      <div className="container">
        <header className="mb-5 d-flex justify-content-between align-items-center">
          <div>
            <h1 className="h3 text-primary fw-bold mb-1">Visão Geral</h1>
            <p className="text-secondary mb-0">Visualize as operações e importe novos arquivos</p>
          </div>
        </header>

        <div className="row g-4">

          <div className="col-12 col-lg-4">
            <div className="card shadow-sm border-0">
              <div className="card-header bg-white border-0 pt-4 pb-2 px-4">
                <h2 className="h5 fw-bold text-dark mb-0">
                  <i className="bi bi-upload me-2 text-primary"></i> 
                  Importar Arquivo
                </h2>
              </div>
              <div className="card-body p-4 bg-white">
                {message && (
                  <div className={`alert alert-${message.type} py-2 small`} role="alert">
                    {message.text}
                  </div>
                )}
                <form onSubmit={handleSubmit}>
                  <div className="mb-4">
                    <label htmlFor="cnabFile" className="form-label text-secondary small fw-semibold">
                      Selecione o arquivo formato (.txt)
                    </label>
                    <input
                      type="file"
                      className="form-control"
                      id="cnabFile"
                      accept=".txt"
                      onChange={handleFileChange}
                      disabled={isUploading}
                    />
                  </div>
                  <button
                    type="submit"
                    className="btn btn-primary w-100 fw-bold shadow-sm"
                    disabled={!file || isUploading}
                  >
                    {isUploading ? "Enviando..." : "Enviar e Processar CNAB"}
                  </button>
                </form>
              </div>
            </div>
          </div>

          <div className="col-12 col-lg-8">
            <div className="card shadow-sm border-0">
              <div className="card-header bg-white border-0 pt-4 pb-2 px-4">
                <h2 className="h5 fw-bold text-dark mb-0">
                  Lojas e Operações
                </h2>
              </div>
              
              <div className="card-body p-0">
                {isLoadingData ? (
                  <div className="p-5 text-center text-secondary">
                    <div className="spinner-border spinner-border-sm me-2" role="status">
                      <span className="visually-hidden">Loading...</span>
                    </div>
                    Carregando transações...
                  </div>
                ) : storeGroups.length === 0 ? (
                  <div className="p-5 text-center text-secondary">
                    Nenhuma operação importada ainda.
                  </div>
                ) : (
                  storeGroups.map(store => (
                    <div key={store.id} className="border-bottom p-4">
                      <div className="d-flex justify-content-between align-items-end mb-3">
                        <div>
                          <h3 className="h6 text-uppercase fw-bold text-muted mb-1">{store.name}</h3>
                        </div>
                        <div className="text-end">
                          <small className="text-secondary d-block">Saldo de Operações</small>
                          <strong className={`fs-5 ${store.balance >= 0 ? "text-success" : "text-danger"}`}>
                            {formatCurrency(store.balance)}
                          </strong>
                        </div>
                      </div>

                      <div className="table-responsive">
                        <table className="table table-sm table-borderless table-striped mb-0 small">
                          <thead>
                            <tr>
                              <th className="text-secondary">Data</th>
                              <th className="text-secondary">Tipo</th>
                              <th className="text-secondary text-end">Valor</th>
                            </tr>
                          </thead>
                          <tbody>
                            {store.operations.map(op => (
                              <tr key={op.id}>
                                <td className="align-middle">{formatDate(op.date)}</td>
                                <td className="align-middle">{op.typeLabel}</td>
                                <td className={`align-middle text-end fw-semibold ${op.kind === 'credit' ? 'text-success' : 'text-danger'}`}>
                                  {op.kind === 'credit' ? '+' : ''} {formatCurrency(op.value)}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
