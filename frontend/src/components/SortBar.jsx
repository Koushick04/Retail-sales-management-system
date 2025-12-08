// src/components/SortBar.jsx

// Added customer_name options here 👇
const SORT_OPTIONS = [
  { label: "Date · Newest first", field: "date", order: "desc" },
  { label: "Date · Oldest first", field: "date", order: "asc" },

  { label: "Customer name · A → Z", field: "customer_name", order: "asc" },
  { label: "Customer name · Z → A", field: "customer_name", order: "desc" },

  { label: "Final Amount · High → Low", field: "final_amount", order: "desc" },
  { label: "Final Amount · Low → High", field: "final_amount", order: "asc" },
  { label: "Quantity · High → Low", field: "quantity", order: "desc" },
  { label: "Quantity · Low → High", field: "quantity", order: "asc" },
];

function SortBar({ sortField, sortOrder, onSortChange }) {
  const currentKey = `${sortField}:${sortOrder}`;

  return (
    <div className="sort-bar">
      <div className="sort-left">
        <span className="label">Transactions</span>
        <span className="sort-subtitle">
          View customer activity across TruEstate stores
        </span>
      </div>
      <div className="sort-right">
        <label className="small-label">Sort by</label>
        <select
          className="select"
          value={currentKey}
          onChange={(e) => {
            const [field, order] = e.target.value.split(":");
            onSortChange({ sortField: field, sortOrder: order });
          }}
        >
          {SORT_OPTIONS.map((opt) => (
            <option
              key={`${opt.field}:${opt.order}`}
              value={`${opt.field}:${opt.order}`}
            >
              {opt.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

export default SortBar;
