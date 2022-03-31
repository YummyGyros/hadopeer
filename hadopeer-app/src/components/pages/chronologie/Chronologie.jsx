import React from "react";
import "./chronologie.css";
import Button from "@mui/material/Button";
import axios from "axios";
import Container from "@mui/material/Container";



function getAsembly(href) {
    return (href.search('senat') !== -1 ? "du senat" : "de l'Assemblée nationale");
}

export default function Chronologie() {
    const [date, setDate] = React.useState([])

    const getDate = async () => {
        if (localStorage.getItem("dates") == null)
            await axios
                    .get(global.config.apiUrl + "/dates")
                    .then((res) => {
                        setDate(res.data)
                        localStorage.setItem("dates", JSON.stringify(res.data));
                    })
                    .catch((err) => console.log(err));
        else setDate(JSON.parse(localStorage.getItem("dates")));
    };

    window.onload = function() {
        getDate();
      };

    return (
        <Container maxWidth="xl" className="page">
            <div className="timeline">
                <div className="timeline__group">
                    <div className="timeline__cards">
                        {date.map((date) => (
                            <div key={date} className="timeline__card card">
                                <header className="card__header">
                                    <time className="time" dateTime="2008-08-18">
                                        <span className="time__day">{date[0]}</span>
                                    </time>
                                </header>
                                <div className="card__content">
                                <Button
                                    color={getAsembly(date[1]) === "du senat" ? "error" : "primary" }
                                    variant="contained"
                                    href={date[1]}>
                                    lien vers la séance {getAsembly(date[1])}
                                </Button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </Container>
    );
}
