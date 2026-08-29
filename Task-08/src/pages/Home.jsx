import { useEffect, useState } from "react";
import { discoverByGenre, getGenres, getTrending } from "../api/tmdb";
import { MovieGrid } from "../components/MovieGrid";
import { Loader, ErrorMessage } from "../components/Loader";

export function Home() {
  const [movies, setMovies] = useState([]);
  const [genres, setGenres] = useState([]);
  const [activeGenre, setActiveGenre] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getGenres()
      .then((data) => setGenres(data.genres))
      .catch(() => {});
  }, []);

  useEffect(() => {
    setLoading(true);
    setError(null);
    const request = activeGenre ? discoverByGenre(activeGenre) : getTrending();

    request
      .then((data) => setMovies(data.results))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [activeGenre]);

  return (
    <div className="mx-auto max-w-6xl px-4 py-8">
      <h1 className="mb-1 text-2xl font-semibold text-white">
        {activeGenre ? "Browse" : "Trending this week"}
      </h1>
      <p className="mb-6 text-zinc-500">Discover movies to add to your watchlist.</p>

      <div className="mb-6 flex flex-wrap gap-2">
        <button
          onClick={() => setActiveGenre(null)}
          className={`rounded-full px-3 py-1 text-sm ${
            !activeGenre ? "bg-teal-500 text-white" : "bg-white/5 text-zinc-400 hover:text-white"
          }`}
        >
          Trending
        </button>
        {genres.map((genre) => (
          <button
            key={genre.id}
            onClick={() => setActiveGenre(genre.id)}
            className={`rounded-full px-3 py-1 text-sm ${
              activeGenre === genre.id
                ? "bg-teal-500 text-white"
                : "bg-white/5 text-zinc-400 hover:text-white"
            }`}
          >
            {genre.name}
          </button>
        ))}
      </div>

      {loading && <Loader />}
      {error && <ErrorMessage message={error} />}
      {!loading && !error && <MovieGrid movies={movies} />}
    </div>
  );
}
