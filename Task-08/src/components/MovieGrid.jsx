import { MovieCard } from "./MovieCard";

export function MovieGrid({ movies }) {
  if (!movies?.length) {
    return <p className="py-12 text-center text-zinc-500">No movies to show.</p>;
  }

  return (
    <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
      {movies.map((movie) => (
        <MovieCard key={movie.id} movie={movie} />
      ))}
    </div>
  );
}
