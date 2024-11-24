export default function toLabel(str) {
  // converts snake_case to Title Case
  return str
    .replace(/_/g, " ")
    .replace(/^./, function (txt) {
      return txt.toUpperCase();
    })
    .toLowerCase();
}
