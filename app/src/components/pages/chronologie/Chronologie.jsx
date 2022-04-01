import React from "react";
import "./chronologie.css";
import Button from "@mui/material/Button";
import axios from "axios";
import Container from "@mui/material/Container";

function getAsembly(href) {
    return (href.search('senat') !== -1 ? "senat" : "Assemblée nationale");
}

export default function Chronologie() {
    const [date, setDate] = React.useState([])

    const getDate = async () => {
        if (localStorage.getItem("dates") == null)
            await axios
                    .get(global.config.apiUrl + "/dates")
                    .then((res) => {
                        for (let i = 0; i < res.data.length; i++)
                            if (res.data[i + 1]) {
                                let j = 1;
                                while (true) {
                                    if (res.data[i + 1][0] === res.data[i][0]) {
                                        res.data[i][j + 1] = res.data[i + 1][1]
                                        res.data.splice(i + 1, 1)
                                        j++
                                    }
                                    else
                                        break
                                }
                            }

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
                                        <span className="time__day">{getAsembly(date[1])} - {date[0]}</span>
                                    </time>
                                </header>
                                <div className="card__content">
                                    {date.map((dat) => (
                                        dat.search('http') !== -1 ?
                                        <Button
                                            target="_blank"
                                            rel="noreferrer noopener"
                                            color={getAsembly(dat) === "senat" ? "error" : "primary" }
                                            variant="contained"
                                            href={dat}>
                                            séance {date.indexOf(dat)}
                                        </Button>
                                        : null
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </Container>
    );
}
