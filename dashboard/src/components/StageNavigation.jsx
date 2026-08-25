/**
 * Vertical stage dots navigation on the right side
 */
export function StageNavigation({ stages, activeStage, onNavigate }) {
  return (
    <aside className="stage-dots">
      {stages.map((stage, index) => (
        <button
          key={stage.id}
          className={index === activeStage ? "dot-active" : ""}
          onClick={() => onNavigate(index)}
          title={stage.label}
        >
          <span />
          <small>{stage.label}</small>
        </button>
      ))}
    </aside>
  );
}
