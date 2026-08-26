import { Link } from "react-router-dom";
import { imageUrl } from "../api/tmdb";
import { useWatchlist } from "../context/WatchlistContext";
import { WatchlistButton } from "./WatchlistButton";

export function MovieCard({ movie }) {
  const { toggleWatchlist, isInWatchlist } = useWatchlist();
  const year = movie.release_date ? movie.release_date.slice(0, 4) : "—";

  return (
    <div className="group relative overflow-hidden rounded-lg bg-white/5 transition-transform hover:-translate-y-1">
      <Link to={`/movie/${movie.id}`}>
        <div className="aspect-[2/3] w-full overflow-hidden bg-zinc-800">
          {movie.poster_path ? (
            <img
              src={imageUrl(movie.poster_path)}
              alt={movie.title}
              loading="lazy"
              className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
            />
          ) : (
            <div className="flex h-full items-center justify-center text-sm text-zinc-500">
              No image
            </div>
          )}
        </div>
      </Link>

      <WatchlistButton
        active={isInWatchlist(movie.id)}
        onClick={() => toggleWatchlist(movie)}
        className="absolute right-2 top-2"
      />

      <div className="p-3">
        <Link to={`/movie/${movie.id}`} className="line-clamp-1 font-medium text-white hover:underline">
          {movie.title}
        </Link>
        <div className="mt-1 flex items-center justify-between text-xs text-zinc-400">
          <span>{year}</span>
          <span className="flex items-center gap-1 text-amber-400">
            ★ {movie.vote_average ? movie.vote_average.toFixed(1) : "N/A"}
          </span>
        </div>
      </div>
    </div>
  );
}
