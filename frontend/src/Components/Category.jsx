export default function Category({ name, isActive = false, onToggle }) {
  return (
    <button
      type="button"
      className={`btn ${isActive ? "btn-orange" : "btn-white"}`}
      style={{ width: "100%", borderRadius: "0px" }}
      onClick={onToggle}
    >
      {name}
    </button>
  );
}
