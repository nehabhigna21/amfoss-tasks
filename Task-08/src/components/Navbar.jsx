import { NavLink } from "react-router-dom";

const linkClass = ({ isActive }) =>
  `px-3 py-2 text-sm font-medium rounded-md transition-colors ${
    isActive ? "text-white bg-white/10" : "text-zinc-400 hover:text-white"
  }`;

export function Navbar() {
  return (
    <header className="sticky top-0 z-20 border-b border-white/10 bg-[#0f1014]/90 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <NavLink to="/" className="flex items-center gap-2 text-lg font-semibold text-white">
          <span className="text-teal-400">Ohara</span> Archive
        </NavLink>
        <nav className="flex items-center gap-1">
          <NavLink to="/" className={linkClass} end>
            Discover
          </NavLink>
          <NavLink to="/search" className={linkClass}>
            Search
          </NavLink>
          <NavLink to="/watchlist" className={linkClass}>
            Watchlist
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
