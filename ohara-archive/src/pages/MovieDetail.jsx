import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getMovieDetails, imageUrl } from "../api/tmdb";
import { Loader, ErrorMessage } from "../components/Loader";
import { WatchlistButton } from "../components/WatchlistButton";
import { useWatchlist } from "../context/WatchlistContext";

export function MovieDetail() {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { toggleWatchlist, isInWatchlist } = useWatchlist();

  useEffect(() => {
    setLoading(true);
    setError(null);
    getMovieDetails(id)
      .then(setMovie)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <Loader />;
  if (error) return <div className="mx-auto max-w-6xl px-4 py-8"><ErrorMessage message={error} /></div>;
  if (!movie) return null;

  const cast = movie.credits?.cast?.slice(0, 8) ?? [];
  const year = movie.release_date ? movie.release_date.slice(0, 4) : "—";
  const watchlistEntry = {
    id: movie.id,
    title: movie.title,
    poster_path: movie.poster_path,
    release_date: movie.release_date,
    vote_average: movie.vote_average,
  };

  return (
    <div>
      <div
        className="relative h-[360px] bg-cover bg-center"
        style={{
          backgroundImage: movie.backdrop_path
            ? `linear-gradient(to top, #0f1014, rgba(15,16,20,0.6)), url(${imageUrl(movie.backdrop_path, "original")})`
            : undefined,
        }}
      />

      <div className="mx-auto max-w-6xl px-4 py-8 -mt-32 relative">
        <div className="flex flex-col gap-6 sm:flex-row">
          <img
            src={imageUrl(movie.poster_path) ?? undefined}
            alt={movie.title}
            className="w-40 shrink-0 rounded-lg shadow-lg sm:w-56"
          />

          <div className="flex-1">
            <Link to="/" className="text-sm text-zinc-400 hover:text-white">
              ← Back
            </Link>
            <div className="mt-2 flex items-start justify-between gap-4">
              <h1 className="text-3xl font-semibold text-white">{movie.title}</h1>
              <WatchlistButton
                active={isInWatchlist(movie.id)}
                onClick={() => toggleWatchlist(watchlistEntry)}
              />
            </div>

            <div className="mt-2 flex flex-wrap items-center gap-3 text-sm text-zinc-400">
              <span>{year}</span>
              {movie.runtime ? <span>{movie.runtime} min</span> : null}
              <span className="text-amber-400">★ {movie.vote_average?.toFixed(1)}</span>
            </div>

            <div className="mt-3 flex flex-wrap gap-2">
              {movie.genres?.map((g) => (
                <span key={g.id} className="rounded-full bg-white/10 px-3 py-1 text-xs text-zinc-300">
                  {g.name}
                </span>
              ))}
            </div>

            <p className="mt-4 max-w-2xl leading-relaxed text-zinc-300">{movie.overview}</p>
          </div>
        </div>

        {cast.length > 0 && (
          <div className="mt-10">
            <h2 className="mb-4 text-lg font-semibold text-white">Cast</h2>
            <div className="flex gap-4 overflow-x-auto pb-2">
              {cast.map((person) => (
                <div key={person.id} className="w-24 shrink-0 text-center">
                  <div className="mb-2 aspect-square overflow-hidden rounded-full bg-zinc-800">
                    {person.profile_path && (
                      <img
                        src={imageUrl(person.profile_path, "w185")}
                        alt={person.name}
                        className="h-full w-full object-cover"
                      />
                    )}
                  </div>
                  <p className="line-clamp-1 text-xs text-white">{person.name}</p>
                  <p className="line-clamp-1 text-xs text-zinc-500">{person.character}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
