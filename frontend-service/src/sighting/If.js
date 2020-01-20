export function If({ condition, children }) {
  if (condition) {
    return children;
  }
  return null;
}
