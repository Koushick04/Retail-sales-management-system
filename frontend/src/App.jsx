// src/App.jsx
import { useEffect, useState } from "react";
import { fetchSales } from "./services/api";
import SearchBar from "./components/SearchBar";
import FiltersPanel from "./components/FiltersPanel";
import SortBar from "./components/SortBar";
import TransactionsTable from "./components/TransactionsTable";
import Pagination from "./components/Pagination";
import "./styles.css";

const DEFAULT_LIMIT = 50; // show more rows per page so table looks taller

function App() {
  // Filters actually sent to backend
  const [filters, setFilters] = useState({
    search: "",
    regions: [],
    genders: [],
    categories: [],
    paymentMethods: [],
    tags:[],
    startDate: "",
    endDate: "",
    sortField: "date",
    sortOrder: "desc",
    page: 1,
    limit: DEFAULT_LIMIT,
  });

  // Draft UI state for search + filters
  const [searchDraft, setSearchDraft] = useState("");
  const [filterDraft, setFilterDraft] = useState({
    regions: [],
    genders: [],
    categories: [],
    paymentMethods: [],
    tags:[],
    startDate: "",
    endDate: "",
  });

  const [isFilterOpen, setIsFilterOpen] = useState(false);

  const [sales, setSales] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);

  // Search suggestions
  const [suggestions, setSuggestions] = useState([]);

  // Fetch data whenever applied filters change
  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        setLoading(true);
        const result = await fetchSales(filters);
        if (!cancelled) {
          setSales(result.data || []);
          setTotal(result.total || 0);
        }
      } catch (err) {
        console.error("Failed to load sales:", err);
        if (!cancelled) {
          setSales([]);
          setTotal(0);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    load();

    return () => {
      cancelled = true;
    };
  }, [filters]);

  // 🔍 Suggestions effect – call backend with small limit
  useEffect(() => {
    const text = searchDraft.trim();
    if (!text || text.length < 2) {
      setSuggestions([]);
      return;
    }

    let cancelled = false;
    const timer = setTimeout(async () => {
      try {
        const result = await fetchSales({
          ...filters,
          search: text,
          page: 1,
          limit: 5,
        });
        if (!cancelled) {
          const names = (result.data || [])
            .map((r) => r.customer_name)
            .filter(Boolean);
          const unique = [...new Set(names)].slice(0, 5);
          setSuggestions(unique);
        }
      } catch (e) {
        if (!cancelled) setSuggestions([]);
      }
    }, 300); // debounce 300ms

    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
    // we intentionally only depend on searchDraft so suggestions
    // don't spam on every filter change
  }, [searchDraft]);

  // Search button
  const handleSearchSubmit = () => {
    const text = searchDraft.trim();
    setFilters((prev) => ({
      ...prev,
      search: text,
      page: 1,
    }));
    setSuggestions([]);
  };

  // When a suggestion is clicked
  const handleSelectSuggestion = (text) => {
    setSearchDraft(text);
    setFilters((prev) => ({
      ...prev,
      search: text,
      page: 1,
    }));
    setSuggestions([]);
  };

  // Apply filters button
  const handleFiltersApply = () => {
    setFilters((prev) => ({
      ...prev,
      ...filterDraft,
      page: 1,
    }));
    setIsFilterOpen(false);
  };

  // Clear everything
  const handleClearAll = () => {
    const clearedFilters = {
      search: "",
      regions: [],
      genders: [],
      categories: [],
      paymentMethods: [],
      startDate: "",
      endDate: "",
      page: 1,
    };

    setFilters((prev) => ({ ...prev, ...clearedFilters }));
    setFilterDraft({
      regions: [],
      genders: [],
      categories: [],
      paymentMethods: [],
      startDate: "",
      endDate: "",
    });
    setSearchDraft("");
    setSuggestions([]);
  };

  // Sorting dropdown change
  const handleSortChange = ({ sortField, sortOrder }) => {
    setFilters((prev) => ({
      ...prev,
      sortField,
      sortOrder,
      page: 1,
    }));
  };

  // Pagination change
  const handlePageChange = (page) => {
    if (page < 1) return;
    setFilters((prev) => ({
      ...prev,
      page,
    }));
  };

  // Count active filters
  const activeFilterCount =
    (filters.regions.length ? 1 : 0) +
    (filters.genders.length ? 1 : 0) +
    (filters.categories.length ? 1 : 0) +
    (filters.paymentMethods.length ? 1 : 0) +
    (filters.tags.length ? 1 : 0) +
    (filters.startDate || filters.endDate ? 1 : 0);

  return (
    <div className="app-shell">
      {/* Centered header content */}
<header className="app-header">
  <div className="header-inner">

    {/* TOP BAR */}
    <div className="app-header-top">
      {/* LEFT: Logo + Name */}
      <div className="brand">
        <div className="brand-logo">
          <span className="brand-logo-mark" />
        </div>
        <div className="brand-text">
          <div className="brand-name">TruEstate</div>
          <div className="brand-tagline">Retail & Customer Analytics</div>
        </div>
      </div>

      {/* CENTER NAV */}
      <nav className="nav-links">
        <span className="nav-link nav-link-active">Dashboard</span>
        <span className="nav-link">Stores</span>
        <span className="nav-link">Customers</span>
        <span className="nav-link">Reports</span>
      </nav>

      {/* RIGHT SIDE — EMPTY NOW */}
      <div className="header-right-empty"></div>
    </div>

    {/* HERO — ONLY LEFT SIDE TEXT */}
    <div className="app-hero hero-left">
  <div className="hero-text">
    <h1 className="hero-title">Retail sales across TruEstate stores</h1>
    <p className="hero-subtitle">
      Track transactions, understand customer behaviour, and slice data
      by region, product, and payment method.
    </p>
  </div>
</div>


  </div>
</header>


      {/* Main content centered under header */}
      <main className="app-main">
        <div className="main-inner">
          {/* LEFT: search + filters */}
          <section className="left-column">
            <SearchBar
              value={searchDraft}
              onChange={setSearchDraft}
              onSearch={handleSearchSubmit}
              suggestions={suggestions}
              onSelectSuggestion={handleSelectSuggestion}
            />

            <FiltersPanel
              isOpen={isFilterOpen}
              activeCount={activeFilterCount}
              draft={filterDraft}
              onToggle={() => setIsFilterOpen((open) => !open)}
              onDraftChange={(patch) =>
                setFilterDraft((prev) => ({ ...prev, ...patch }))
              }
              onApply={handleFiltersApply}
              onClearAll={handleClearAll}
            />
          </section>

          {/* RIGHT: sort + table + pagination */}
          <section className="right-column">
            <SortBar
              sortField={filters.sortField}
              sortOrder={filters.sortOrder}
              onSortChange={handleSortChange}
            />

            <TransactionsTable data={sales} loading={loading} />

            <Pagination
              page={filters.page}
              total={total}
              limit={filters.limit}
              onPageChange={handlePageChange}
            />
          </section>
        </div>
      </main>

      {/* Simple footer */}
      <footer className="app-footer">
        <div className="footer-inner">
          <div className="footer-title">About TruEstate Retail Sales</div>
          <div className="footer-text">
            Internal analytics dashboard built as part of the TruEstate
            assignment. It visualizes large-scale retail transactions with
            search, filters, sorting and pagination.
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
