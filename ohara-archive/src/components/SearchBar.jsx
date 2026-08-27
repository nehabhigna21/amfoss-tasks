export function SearchBar({ value, onChange, placeholder = "Search movies..." }) {
  return (
    <input
      type="text"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      className="w-full rounded-md border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-zinc-500 outline-none focus:border-teal-400"
    />
  );
}
