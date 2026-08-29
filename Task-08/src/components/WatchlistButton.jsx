export function WatchlistButton({ active, onClick, className = "" }) {
  return (
    <button
      type="button"
      onClick={(e) => {
        e.preventDefault();
        e.stopPropagation();
        onClick();
      }}
      title={active ? "Remove from watchlist" : "Add to watchlist"}
      className={`flex h-8 w-8 items-center justify-center rounded-full text-lg shadow transition-colors ${
        active ? "bg-teal-500 text-white" : "bg-black/60 text-white hover:bg-black/80"
      } ${className}`}
    >
      {active ? "✓" : "+"}
    </button>
  );
}
