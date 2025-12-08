// src/components/TransactionsTable.jsx

function TransactionsTable({ data, loading }) {
  const handleCopyPhone = async (phone) => {
    if (!phone) return;
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(phone);
      } else {
        // Fallback for older browsers
        const el = document.createElement("textarea");
        el.value = phone;
        document.body.appendChild(el);
        el.select();
        document.execCommand("copy");
        document.body.removeChild(el);
      }
      console.log("Copied:", phone);
    } catch (e) {
      console.error("Failed to copy phone:", e);
    }
  };

  if (loading) {
    return (
      <div className="card table-card">
        <div className="table-empty">Loading transactions…</div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="card table-card">
        <div className="table-empty">No transactions found.</div>
      </div>
    );
  }

  return (
    <div className="card table-card">
      {/* Scroll wrapper for both directions */}
      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>Transaction ID</th>
              <th>Date</th>
              <th>Customer ID</th>
              <th>Customer name</th>
              <th>Phone Number</th>
              <th>Gender</th>
              <th>Age</th>
              <th>Product Category</th>
              <th>Quantity</th>
              <th>Total Amount</th>
              <th>Final Amount</th>
              <th>Customer region</th>
              <th>Product ID</th>
              <th>Employee name</th>
            </tr>
          </thead>
          <tbody>
            {data.map((s) => (
              <tr key={s.id ?? s.transaction_id}>
                <td>{s.transaction_id || "-"}</td>
                <td>{s.date || "-"}</td>
                <td>{s.customer_id || "-"}</td>
                <td>{s.customer_name || "-"}</td>

                <td className="phone-cell">
                  <span>{s.phone_number || "-"}</span>
                  {s.phone_number && (
                    <button
                      type="button"
                      className="icon-button"
                      onClick={() => handleCopyPhone(s.phone_number)}
                      title="Copy phone number"
                    >
                      ⧉
                    </button>
                  )}
                </td>

                <td>{s.gender || "-"}</td>
                <td>{s.age ?? "-"}</td>
                <td>{s.product_category || "-"}</td>
                <td>{s.quantity ?? "-"}</td>
                <td>{s.total_amount ?? "-"}</td>
                <td>{s.final_amount ?? "-"}</td>
                <td>{s.customer_region || "-"}</td>
                <td>{s.product_id || "-"}</td>
                <td>{s.employee_name || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default TransactionsTable;
