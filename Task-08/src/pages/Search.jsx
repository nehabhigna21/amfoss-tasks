import { useEffect, useState } from "react";
import { searchMovies } from "../api/tmdb";
import { SearchBar } from "../components/SearchBar";
import { MovieGrid } from "../components/MovieGrid";
import { Loader, ErrorMessage } from "../components/Loader";
import { useDebounce } from "../hooks/useDebounce";

export function Search() {
  const [query, setQuery] = useState("");
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const debouncedQuery = useDebounce(query, 400);

  useEffect(() => {
    if (!debouncedQuery.trim()) {
      setMovies([]);
      return;
    }

    setLoading(true);
    setError(null);

    searchMovies(debouncedQuery)
      .then((data) => setMovies(data.results))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [debouncedQuery]);

  return (
    <div className="mx-auto max-w-6xl px-4 py-8">
      <h1 className="mb-6 text-2xl font-semibold text-white">Search</h1>
      <div className="mb-8 max-w-md">
        <SearchBar value={query} onChange={setQuery} />
      </div>

      {loading && <Loader />}
      {error && <ErrorMessage message={error} />}
      {!loading && !error && debouncedQuery && <MovieGrid movies={movies} />}
      {!debouncedQuery && (
        <p className="text-center text-zinc-500">Start typing to search for movies.</p>
      )}
    </div>
  );
}
