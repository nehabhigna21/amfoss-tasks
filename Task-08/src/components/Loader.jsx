export function Loader() {
  return (
    <div className="flex justify-center py-16">
      <div className="h-8 w-8 animate-spin rounded-full border-2 border-white/20 border-t-teal-400" />
    </div>
  );
}

export function ErrorMessage({ message }) {
  return (
    <div className="rounded-md border border-red-500/30 bg-red-500/10 p-4 text-center text-red-300">
      {message}
    </div>
  );
}
