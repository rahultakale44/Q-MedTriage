import { Activity } from "lucide-react";

/**
 * Top navigation bar with branding, navigation links, and system status
 */
export function Navbar({ activeStage, onNavigate }) {
  const navItems = [
    { label: "OVERVIEW", stageIndex: 0 },
    { label: "PIPELINE", stageIndex: 2 },
    { label: "QUANTUM", stageIndex: 4 },
    { label: "EVIDENCE", stageIndex: 5 },
    { label: "TRIAGE", stageIndex: 7 },
  ];

  return (
    <header className="topbar">
      <div className="brand">
        <div className="brand-mark">
          <Activity size={20} />
        </div>

        <div>
          <div className="brand-name">Q-MEDTRIAGE</div>

          <div className="brand-sub">QUANTUM MEDICAL INTELLIGENCE</div>
        </div>
      </div>

      <nav className="nav-links">
        {navItems.map((item) => (
          <button
            key={item.label}
            onClick={() => onNavigate(item.stageIndex)}
            className={activeStage >= item.stageIndex ? "nav-active" : ""}
          >
            {item.label}
          </button>
        ))}
      </nav>

      <div className="system-status">
        <span className="status-dot" />
        SYSTEM ONLINE
      </div>
    </header>
  );
}
