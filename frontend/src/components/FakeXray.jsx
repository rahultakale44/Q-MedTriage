/**
 * Stylized fake chest X-ray visualization
 * Used as placeholder when no real image is uploaded
 */
export function FakeXray() {
  return (
    <div className="fake-xray">
      <div className="lung left" />
      <div className="lung right" />
      <div className="spine" />

      <div className="rib rib-1" />
      <div className="rib rib-2" />
      <div className="rib rib-3" />
      <div className="rib rib-4" />
      <div className="rib rib-5" />
      <div className="rib rib-6" />
    </div>
  );
}
