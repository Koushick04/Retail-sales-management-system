// src/components/Pagination.jsx
function Pagination({ page, total, limit, onPageChange }) {
  const totalPages = Math.max(1, Math.ceil(total / limit));

  return (
    <div className="pagination">
      <button
        type="button"
        className="secondary-button"
        onClick={() => onPageChange(page - 1)}
        disabled={page <= 1}
      >
        Prev
      </button>
      <span className="pagination-text">
        Page {page} of {totalPages}
      </span>
      <button
        type="button"
        className="secondary-button"
        onClick={() => onPageChange(page + 1)}
        disabled={page >= totalPages}
      >
        Next
      </button>
    </div>
  );
}

export default Pagination;
