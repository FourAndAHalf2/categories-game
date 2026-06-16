import { useEffect, useState } from "react";

function CapitalizeFirstLetter(string) {
  return string[0].toUpperCase() + string.slice(1);
}

function GetRandomLetter() {
  return String.fromCharCode(Math.round(Math.random() * 25) + 65);
}
function Choice(x) {
  return x[Math.floor(Math.random() * x.length)];
}

export default function Practice() {
  const url = location.toString();
  const selectedCategories = new URLSearchParams(
    url.substring(url.lastIndexOf("?") + 1, url.length),
  )
    .get("categories")
    .split(",");

  const [randomLetter, setRandomLetter] = useState(GetRandomLetter());

  const [listOfCorrectAnswers, _] = useState({});

  useEffect(() => {
    selectedCategories.forEach((cat) => {
      fetch(`/api/${cat}`)
        .then((res) => res.json())
        .then((data) => (listOfCorrectAnswers[cat] = data));
    });
  }, [selectedCategories, listOfCorrectAnswers]);

  const [isSubmited, setIsSubmited] = useState(false);
  const [userAnswers, setUserAnswers] = useState({});

  return (
    <>
      <div className="container">
        <div className="row">
          <div className="col-3 bg-orange">
            <h2>Write categories strarting on:</h2>
            <h3>{randomLetter}</h3>
          </div>

          <ul className="col-9 list-group">
            {selectedCategories.map((cat) => (
              <li className="list-group-item" key={cat}>
                <h3>{CapitalizeFirstLetter(cat.replace("-"," "))}</h3>

                <input
                  onChange={(e) => {
                    if (
                      e.target.value[0].toLowerCase() !=
                      randomLetter.toLowerCase()
                    ) {
                      e.target.value = "";
                    }

                    setUserAnswers((prev) => ({
                      ...prev,
                      [cat]: e.target.value,
                    }));
                  }}
                  placeholder={`${randomLetter}...`}
                  value={userAnswers[cat]}
                ></input>
                {isSubmited && (
                  <span>
                    {listOfCorrectAnswers[cat]?.some(
                      (x) =>
                        x.toLowerCase() === userAnswers[cat]?.toLowerCase(),
                    )
                      ? "Correct"
                      : `Incorrect or that anwser isn't in the database, correct is e.g ${Choice(listOfCorrectAnswers[cat].filter((x) => x[0] == randomLetter)) || "no answer found in the database"}`}
                  </span>
                )}
                <hr />
              </li>
            ))}
          </ul>

          <button
            onClick={() => setIsSubmited(true)}
            className="btn btn-orange mt-2"
          >
            <h2>Submit</h2>
          </button>
          {isSubmited && (
            <button
              className="btn btn-orange mt-2"
              style={{ width: "auto" }}
              onClick={() => {
                setRandomLetter(GetRandomLetter());
                setIsSubmited(false);
                selectedCategories.forEach((cat) => {
                  userAnswers[cat] = "";
                });
              }}
            >
              Play again
            </button>
          )}
        </div>
      </div>
    </>
  );
}
