// frontend/src/App.jsx
import React, { useEffect, useState } from "react";
import { fetchSales } from "./services/api";
import "./styles.css"; // keep your existing styling

export default function App() {
  const [sales, setSales] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [limit] = useState(50);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadData = async (p = 1) => {
    setLoading(true);
    setError(null);
    try {
      const resp = await fetchSales({ page: p, limit, sort_field: "date", sort_order: "desc" });
      // resp should be { data: [...], total: N }
      setSales(resp.data || []);
      setTotal(resp.total ?? 0);
    } catch (err) {
      setError(err.message || String(err));
      setSales([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData(page);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page]);

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>TruEstate Retail Sales</h1>
      </header>

      <main className="app-main">
        <section className="controls">
          <div>
            <button onClick={() => loadData(1)}>Reload</button>
            <span style={{ marginLeft: 12 }}>Total: {total.toLocaleString()}</span>
          </div>
        </section>

        <section className="table-section">
          {loading && <div className="status">Loading transactions...</div>}
          {error && <div className="status error">Error: {error}</div>}
          {!loading && !error && sales.length === 0 && <div className="status">No transactions found.</div>}

          {!loading && !error && sales.length > 0 && (
            <div className="table-wrapper">
              <table className="transactions-table">
                <thead>
                  <tr>
                    <th>Transaction ID</th>
                    <th>Date</th>
                    <th>Customer</th>
                    <th>Phone</th>
                    <th>Category</th>
                    <th>Qty</th>
                    <th>Final Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {sales.map((s, idx) => (
                    <tr key={s.transaction_id || s.id || idx}>
                      <td>{s.transaction_id ?? s.id}</td>
                      <td>{s.date ?? ""}</td>
                      <td>{s.customer_name ?? ""}</td>
                      <td>{s.phone_number ?? ""}</td>
                      <td>{s.product_category ?? s.category ?? ""}</td>
                      <td>{s.quantity ?? ""}</td>
                      <td>{s.final_amount ?? s.total_amount ?? ""}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        <footer className="app-footer">
          <div>Page {page}</div>
        </footer>
      </main>
    </div>
  );
}
