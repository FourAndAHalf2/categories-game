import { useState } from 'react';

export default function Category({ name, onToggle }) {
  const [isActive, setIsActive] = useState(false);

  return (
    <button
      className={`btn ${isActive ? "btn-orange" : "btn-white"}`}
      style={{ width: "100%", borderRadius: "0px" }}
      onClick={() => {
        setIsActive(!isActive)
        onToggle()
      }}
    >
      {name}
    </button>
  );
}
