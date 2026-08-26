const BASE_URL = "https://api.themoviedb.org/3";
const TOKEN = import.meta.env.VITE_TMDB_ACCESS_TOKEN;

async function request(path, params = {}) {
  const url = new URL(`${BASE_URL}${path}`);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.set(key, value);
    }
  });

  const res = await fetch(url, {
    headers: {
      Authorization: `Bearer ${TOKEN}`,
      accept: "application/json",
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.status_message || `TMDB request failed (${res.status})`);
  }

  return res.json();
}

export function imageUrl(path, size = "w500") {
  if (!path) return null;
  return `https://image.tmdb.org/t/p/${size}${path}`;
}

export function getTrending(timeWindow = "week") {
  return request(`/trending/movie/${timeWindow}`);
}

export function getPopular(page = 1) {
  return request("/movie/popular", { page });
}

export function getTopRated(page = 1) {
  return request("/movie/top_rated", { page });
}

export function searchMovies(query, page = 1) {
  return request("/search/movie", { query, page });
}

export function discoverByGenre(genreId, page = 1) {
  return request("/discover/movie", { with_genres: genreId, page, sort_by: "popularity.desc" });
}

export function getGenres() {
  return request("/genre/movie/list");
}

export function getMovieDetails(id) {
  return request(`/movie/${id}`, { append_to_response: "credits,videos,similar" });
}
