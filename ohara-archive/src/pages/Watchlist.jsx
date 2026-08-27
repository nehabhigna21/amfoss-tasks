import { useWatchlist } from "../context/WatchlistContext";
import { MovieGrid } from "../components/MovieGrid";

export function Watchlist() {
  const { watchlist } = useWatchlist();

  return (
    <div className="mx-auto max-w-6xl px-4 py-8">
      <h1 className="mb-1 text-2xl font-semibold text-white">Your Watchlist</h1>
      <p className="mb-6 text-zinc-500">
        {watchlist.length} movie{watchlist.length === 1 ? "" : "s"} saved.
      </p>

      {watchlist.length === 0 ? (
        <p className="py-12 text-center text-zinc-500">
          Your watchlist is empty. Add movies from Discover or Search.
        </p>
      ) : (
        <MovieGrid movies={watchlist} />
      )}
    </div>
  );
}
