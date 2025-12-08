// src/components/FiltersPanel.jsx

const REGION_OPTIONS = ["North", "South", "East", "West", "Central"];
const GENDER_OPTIONS = ["Male", "Female", "Other"];
const CATEGORY_OPTIONS = [
  "Electronics",
  "Clothing",
  "Groceries",
  "Home & Kitchen",
  "Other",
];
const TAG_OPTIONS = [
  "Discounted",
  "Loyal Customer",
  "New Customer",
  "Bulk Order",
];

const PAYMENT_OPTIONS = ["Cash", "Credit Card", "UPI", "Net Banking", "Wallet"];

function FiltersPanel({
  isOpen,
  activeCount,
  draft,
  onToggle,
  onDraftChange,
  onApply,
  onClearAll,
}) {
  const { regions, genders, categories, paymentMethods, startDate, endDate } =
    draft;

  const toggleInArray = (value, array, key) => {
    const next = array.includes(value)
      ? array.filter((v) => v !== value)
      : [...array, value];
    onDraftChange({ [key]: next });
  };

  if (!isOpen) {
    // Collapsed "Filters" pill
    return (
      <div className="filters-collapsed">
        <button type="button" className="filter-pill" onClick={onToggle}>
          <span className="filter-icon">⚙️</span>
          <span>Filters</span>
          {activeCount > 0 && (
            <span className="filter-count">{activeCount}</span>
          )}
        </button>
      </div>
    );
  }

  return (
    <div className="card filters-panel">
      <div className="filters-header">
        <span className="label">Filters</span>
        <div className="filters-header-actions">
          <button type="button" className="link-button" onClick={onClearAll}>
            Clear all
          </button>
          <button type="button" className="link-button" onClick={onToggle}>
            Close
          </button>
        </div>
      </div>

      <div className="filters-grid">
        {/* Regions */}
        <div className="filter-group">
          <div className="filter-title">Region</div>
          {REGION_OPTIONS.map((opt) => (
            <label key={opt} className="checkbox-label">
              <input
                type="checkbox"
                checked={regions.includes(opt)}
                onChange={() => toggleInArray(opt, regions, "regions")}
              />
              <span>{opt}</span>
            </label>
          ))}
        </div>

        {/* Gender */}
        <div className="filter-group">
          <div className="filter-title">Gender</div>
          {GENDER_OPTIONS.map((opt) => (
            <label key={opt} className="checkbox-label">
              <input
                type="checkbox"
                checked={genders.includes(opt)}
                onChange={() => toggleInArray(opt, genders, "genders")}
              />
              <span>{opt}</span>
            </label>
          ))}
        </div>

        {/* Category */}
        <div className="filter-group">
          <div className="filter-title">Product Category</div>
          {CATEGORY_OPTIONS.map((opt) => (
            <label key={opt} className="checkbox-label">
              <input
                type="checkbox"
                checked={categories.includes(opt)}
                onChange={() => toggleInArray(opt, categories, "categories")}
              />
              <span>{opt}</span>
            </label>
          ))}
        </div>
        
        <div className="filter-group">
  <div className="filter-title">Tags</div>
  {TAG_OPTIONS.map((tag) => {
    const checked = draft.tags?.includes(tag);
    return (
      <label key={tag} className="checkbox-label">
        <input
          type="checkbox"
          checked={checked}
          onChange={(e) => {
            const next = new Set(draft.tags || []);
            if (e.target.checked) {
              next.add(tag);
            } else {
              next.delete(tag);
            }
            onDraftChange({ tags: Array.from(next) });
          }}
        />
        <span>{tag}</span>
      </label>
    );
  })}
</div>


        {/* Payment Method */}
        <div className="filter-group">
          <div className="filter-title">Payment Method</div>
          {PAYMENT_OPTIONS.map((opt) => (
            <label key={opt} className="checkbox-label">
              <input
                type="checkbox"
                checked={paymentMethods.includes(opt)}
                onChange={() =>
                  toggleInArray(opt, paymentMethods, "paymentMethods")
                }
              />
              <span>{opt}</span>
            </label>
          ))}
        </div>

        {/* Date Range */}
        <div className="filter-group date-range-group">
          <div className="filter-title">Date Range</div>
          <div className="date-range-row">
            <div>
              <div className="small-label">From</div>
              <input
                type="date"
                value={startDate}
                onChange={(e) =>
                  onDraftChange({ startDate: e.target.value })
                }
                className="input"
              />
            </div>
            <div>
              <div className="small-label">To</div>
              <input
                type="date"
                value={endDate}
                onChange={(e) => onDraftChange({ endDate: e.target.value })}
                className="input"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="filters-footer">
        <button
          type="button"
          className="primary-button full-width"
          onClick={onApply}
        >
          Apply filters
        </button>
      </div>
    </div>
  );
}

export default FiltersPanel;
