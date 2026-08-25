import { motion } from "framer-motion";

/**
 * Top scroll progress bar
 */
export function ScrollProgress({ progressWidth }) {
  return (
    <motion.div
      className="top-progress"
      style={{
        width: progressWidth,
      }}
    />
  );
}
