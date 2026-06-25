import Category from "../Components/Category";
import { useEffect, useState } from "react";

function App() {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetch("/api/all-categories")
      .then((res) => res.json())
      .then((data) => setCategories(data));
  });

  const [selectedCategories, setSelectedCategories] = useState([]);

  const toggleCategory = (category) => {
    setSelectedCategories((prev) =>
      prev.includes(category)
        ? prev.filter((c) => c !== category)
        : [...prev, category],
    );
  };

  return (
    <div className="container">
      <div className="row">
        <h1 className="text-center">Categories Game</h1>
        <div className="col">
          <h3>Select categories</h3>

          <ul className="list-group list-group-horizontal">
            {categories.map((category) => (
              <Category
                key={category}
                name={category}
                isActive={selectedCategories.includes(category)}
                onToggle={() => toggleCategory(category)}
              />
            ))}
          </ul>

          <button
            type="button"
            className="btn btn-orange rounded-0"
            onClick={() => {
              setSelectedCategories(categories);
            }}
          >
            <b>Select all</b>
          </button>

          {selectedCategories.length < 3 && (
            <p className="text-danger">
              at least 3 categories must be selected
            </p>
          )}
          <button
            type="button"
            style={{ width: "100%" }}
            className="btn btn-orange mt-5"
            onClick={() =>
              (document.location = `practice?categories=${categories
                .filter((cat) => selectedCategories.includes(cat)) // keeps defined order of categories
                .map((cat) => cat.replace(" ", "-"))
                .join(",")}`)
            }
            disabled={selectedCategories.length < 3}
          >
            <h3>practice </h3>
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
