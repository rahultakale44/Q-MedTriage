/**
 * Auto-run toggle button for automatic pipeline progression
 */
export function AutoRunButton({ isRunning, onToggle }) {
  return (
    <button
      className={`auto-run ${isRunning ? "running" : ""}`}
      onClick={onToggle}
    >
      <span className="auto-dot" />

      {isRunning ? "AUTO RUNNING" : "AUTO RUN"}
    </button>
  );
}
