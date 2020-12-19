import React, { useState, useEffect,useRef } from "react";
import axios from "axios";
import { Autocomplete, Row, Col, TextInput, Button } from "react-materialize";
import "./prediction.css";
let url="http://6cdbedcc50f5.ngrok.io";

function dict_null(d){
  let dic={}
  for (var key in d){
    dic[key]=null
  }
  return dic;
}

const Prediction = () => {
  //year,genre,director,budget,country,runtime,mc1,mc2
  const [rating, setRating] = useState(0.0);
  const [yearAutoComplete, setYearAC] = useState({ 2017: null });
  const [genreAutoComplete, setGenreAC] = useState({});
  const [genreAutoComplete2, setGenreAC2] = useState({});
  const [directorAutoComplete, setDirectorAC] = useState({});
  const [directorAutoComplete2, setDirectorAC2] = useState({});
  const [countryAutoComplete, setCountryAC] = useState({});
  const [countryAutoComplete2, setCountryAC2] = useState({});
  const [mc1AutoComplete, setMc1AC] = useState({});
  const [mc2AutoComplete, setMc2AC] = useState({});
  const [mc3AutoComplete, setMc3AC] = useState({});
  const [mc1AutoComplete2, setMc1AC2] = useState({});
  const [mc2AutoComplete2, setMc2AC2] = useState({});
  const [mc3AutoComplete2, setMc3AC2] = useState({});
 const nameForm = useRef(null);
  useEffect(() => {
    let dict = {};
    for (var i = 1874; i <= 2021; i++) {
      dict[i] = null;
    }
    setYearAC(dict);
    axios
      .post(url+"?type=dropdowns", {})
      .then((res) => {
        setCountryAC(res.data.countries);
        setCountryAC2(dict_null(res.data.countries));
        setDirectorAC(res.data.directors);
        setDirectorAC2(dict_null(res.data.directors));
        setGenreAC(res.data.genres);
        setGenreAC2(dict_null(res.data.genres));
        setMc1AC(res.data.main_cast_1);
        setMc2AC(res.data.main_cast_2);
        setMc3AC(res.data.main_cast_3);
        setMc1AC2(dict_null(res.data.main_cast_1));
        setMc2AC2(dict_null(res.data.main_cast_2));
        setMc3AC2(dict_null(res.data.main_cast_3));
        console.log(res.status);
      })
      .catch((err) => console.log(err));
  }, []);
  const handleSubmit = (e) => {
    const form=nameForm.current;
    e.preventDefault();
    let data = {
      year: Number(form['year'].value),
      genre: genreAutoComplete[form['genre'].value],
      director: directorAutoComplete[form['director'].value],
      main_cast_1: mc1AutoComplete[form['mc1'].value],
      main_cast_2: mc2AutoComplete[form['mc2'].value],
      main_cast_3: mc3AutoComplete[form['mc3'].value],
      budget: +form['budget'].value,
      country: countryAutoComplete[form['country'].value],
      runtime: +form['runtime'].value,
    };
    console.log(data);
    axios
      .post(url, data)
      .then((res) => {
        setRating(res.data.prediction);
      })
      .catch((err) => console.log(err));
  };
  return (
    <div>
      <Row>
        <Col l={8}>
          <h1 className="project-title">Proyecto Big Data</h1>
          <form onSubmit={handleSubmit} ref={nameForm}>
            <Row>
              <Col l={4} className="offset-l2">
                <Row>
                  <Autocomplete
                    id="year-textinput"
                    title="Year"
                    name={'year'}
                    options={{
                      data: yearAutoComplete,
                    }}
                  />
                </Row>
                <Row>
                  <Autocomplete
                    id="genre-textinput"
                    title="Genre"
                    name={'genre'}
                    options={{
                      data: genreAutoComplete2,
                    }}
                  />
                </Row>
              </Col>
              <Col l={4}>
                <Row>
                  <Autocomplete
                    id="director-textinput"
                    title="Director"
                    name={'director'}
                    options={{
                      data: directorAutoComplete2,
                    }}
                  />
                </Row>
                <Row>
                  <TextInput
                    id="budget-textinput"
                    label="Budget"
                    name={'budget'}
                  />
                </Row>
              </Col>
            </Row>
            <Row>
              <Col l={4} className="offset-l2">
                <Row>
                  <Autocomplete
                    id="country-textinput"
                    title="Country"
                    name={'country'}
                    options={{
                      data: countryAutoComplete2,
                    }}
                  />
                </Row>
                <Row>
                  <TextInput
                    id="runtime-textinput"
                    label="Runtime"
                    name={'runtime'}
                  />
                </Row>
              </Col>
              <Col l={4}>
                <Row>
                  <Autocomplete
                    id="mc1-textinput"
                    name={'mc1'}
                    title="Main Character 1"
                    options={{
                      data: mc1AutoComplete2,
                    }}
                  />
                </Row>
                <Row>
                  <Autocomplete
                    id="mc2-textinput"
                    title="Main Character 2"
                    name={'mc2'}
                    options={{
                      data: mc2AutoComplete2,
                    }}
                  />
                </Row>
                <Row>
                  <Autocomplete
                    id="mc3-textinput"
                    title="Main Character 3"
                    name={'mc3'}
                    options={{
                      data: mc3AutoComplete2,
                    }}
                  />
                </Row>
              </Col>
            </Row>
            <Row>
              <Col l={4} className="offset-l5 button-col">
                <Button
                  node="button"
                  type="submit"
                  waves="light"
                  className="button"
                >
                  Predict
                </Button>
              </Col>
            </Row>
          </form>
        </Col>
        <Col l={3}>
          <h1 className="rating-header">¿Qué Rating tendrá?</h1>
          <h2 className="rating-number">{rating.toFixed(2)}</h2>
        </Col>
      </Row>
    </div>
  );
};

export default Prediction;
