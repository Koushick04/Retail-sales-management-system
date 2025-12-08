import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export async function fetchSales(filters) {
  const {
    search,
    regions,
    genders,
    categories,
    paymentMethods,
    startDate,
    endDate,
    sortField,
    sortOrder,
    page,
    limit,
  } = filters;

  const params = {
    search: search || undefined,
    page,
    limit,
    sort_field: sortField,
    sort_order: sortOrder,
    // Convert arrays to comma-separated strings only if they have values
    regions: regions.length ? regions.join(",") : undefined,
    gender: genders.length ? genders.join(",") : undefined,
    categories: categories.length ? categories.join(",") : undefined,
    payment_methods: paymentMethods.length
      ? paymentMethods.join(",")
      : undefined,
    start_date: startDate || undefined,
    end_date: endDate || undefined,
  };
  if (filters.tags && filters.tags.length) {
  params.set("tags", filters.tags.join(","));
}


  const response = await axios.get(`${API_BASE_URL}/sales`, { params });
  return response.data; // { data: [...], total: N }
}
