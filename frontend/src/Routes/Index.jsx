import Category from "../Components/Category";
import { useState } from "react";

function App() {
  const categories = ["countries", "cities", "animals", "fruits", "car brands"];

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
        <h1 className=" text-center">Categories Game</h1>
        <div className="col">
          <h3>Select categories</h3>

          <ul className="list-group list-group-horizontal">
            {categories.map((category) => (
              <Category
                key={category}
                name={category}
                onToggle={() => toggleCategory(category)}
              />
            ))}
          </ul>

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
              (document.location = `practice?categories=${selectedCategories.map((cat) => cat.replace(" ", "-")).join(",")}`)
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
