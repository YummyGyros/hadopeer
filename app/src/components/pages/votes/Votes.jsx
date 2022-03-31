import * as React from "react";
import Container from "@mui/material/Container";
import { Box, Typography } from "@mui/material";
import InputLabel from "@mui/material/InputLabel";
import FormControl from "@mui/material/FormControl";
import MenuItem from "@mui/material/MenuItem";
import axios from "axios";
import Stack from "@mui/material/Stack";
import Select from "@mui/material/Select";
import Plot from "react-plotly.js";

export default function Votes() {
    const [politicalGroup, setPoliticalGroup] = React.useState("");
    const [scrutin, setScrutin] = React.useState("");
    const [scrutins, setScrutins] = React.useState([]);
    const [politicalGroups, setPoliticalGroups] = React.useState([]);
    const [votes, setVotes] = React.useState([]);

    const getScrutins = async () => {
        await axios
            .get(global.config.apiUrl + "/votes/context")
            .then((res) => {
                setScrutins(res.data);
                setScrutin(res.data[0]);
                getVotes(res.data[0]);
            })
            .catch((err) => console.log(err));
    };

    const getPoliticalGroups = async () => {
        await axios
            .get(global.config.apiUrl + "/political_groups")
            .then((res) => {
                setPoliticalGroups(res.data);
            })
            .catch((err) => console.log(err));
    };

    const getVotes = async (s = scrutin, p = politicalGroup) => {
        if (localStorage.getItem("votes" + s + p) == null) {
            await axios
                .get(
                    global.config.apiUrl +
                        "/votes?assembly=" +
                        s[1] +
                        "&vote_number=" +
                        s[2] +
                        "&group=" +
                        p
                )
                .then((res) => {
                    setVotes(res.data);
                    localStorage.setItem(
                        "votes" + s + p,
                        JSON.stringify(res.data)
                    );
                })
                .catch((err) => console.log(err));
        } else setVotes(JSON.parse(localStorage.getItem("votes" + s + p)));
    };

    const handlePoliticalGroupChange = (event) => {
        setPoliticalGroup(event.target.value);
        getVotes(scrutin, event.target.value);
    };

    const handleScrutinChange = (event) => {
        setScrutin(event.target.value);
        getVotes(event.target.value);
    };

    window.onload = function () {
        getPoliticalGroups();
        getScrutins();
    };

    return (
        <Container>
            <Stack
                direction="row"
                spacing={10}
                alignItems="left"
                justifyContent="left"
            >
                <Box marginTop={15} alignItems="left" justifyContent="left">
                    <Stack
                        direction="row"
                        spacing={5}
                        alignItems="left"
                        justifyContent="left"
                    >
                        <FormControl variant="standard">
                            <InputLabel id="Scrutin_dropdown_label">
                                Scrutin
                            </InputLabel>
                            <Select
                                sx={{
                                    width: 275,
                                }}
                                labelId="Scrutin_dropdown_label"
                                id="Scrutin_dropdown_select"
                                defaultValue={scrutin}
                                value={scrutin}
                                label="Scrutin"
                                onChange={handleScrutinChange}
                            >
                                {scrutins.map((scrutins) => (
                                    <MenuItem key={scrutins} value={scrutins}>
                                        {scrutins[1]} - {scrutins[0]}
                                    </MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                        <FormControl variant="standard">
                            <InputLabel id="PoliticalGroup_dropdown_label">
                                Groupe Politique
                            </InputLabel>
                            <Select
                                sx={{
                                    width: 150,
                                }}
                                labelId="PoliticalGroup_dropdown_label"
                                id="PoliticalGroup_dropdown_select"
                                defaultValue={politicalGroups[0]}
                                value={politicalGroup}
                                label="PoliticalGroup"
                                onChange={handlePoliticalGroupChange}
                            >
                                <MenuItem value="">None</MenuItem>
                                {politicalGroups.map((politicalGroups) => (
                                    <MenuItem
                                        key={politicalGroups}
                                        value={politicalGroups}
                                    >
                                        {politicalGroups}
                                    </MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </Stack>
                    <Plot
                        data={[
                            {
                                values: [
                                    votes.contre,
                                    votes.pour,
                                    votes.none + votes.absent,
                                ],
                                labels: ["contre", "pour", "sans opinion"],
                                textposition: "inside",
                                domain: { column: 1 },
                                hoverinfo: "label+percent",
                                hole: 0.4,
                                marker: {
                                    colors: [
                                        "rgb(175, 25, 25)",
                                        "rgb(25,175,25)",
                                        "rgb(200,200,200)",
                                    ],
                                },
                                type: "pie",
                            },
                        ]}
                        layout={{
                            annotations: [
                                {
                                    font: {
                                        size: 30,
                                    },
                                    showarrow: false,
                                    text:
                                        votes.pour +
                                            votes.contre +
                                            votes.none +
                                            votes.absent !==
                                        0
                                            ? "Votes"
                                            : "No votes",
                                    x: 0.5,
                                    y: 0.5,
                                },
                            ],
                            height: 800,
                            width: 800,
                        }}
                    />
                </Box>
                    <Stack  style={{ marginTop: 300}} spacing={2}>
                        <Typography variant="h3" color="text.secondary" gutterBottom>
                            TOTAL:{" "}
                            {votes.pour + votes.contre + votes.none + votes.absent}
                        </Typography>
                        <Typography variant="h4" color="text.secondary" gutterBottom>
                            Pour:{" "}
                            {votes.pour}
                        </Typography>
                        <Typography variant="h4" color="text.secondary" gutterBottom>
                            Contre:{" "}
                            {votes.contre}
                        </Typography>
                        <Typography variant="h4" color="text.secondary" gutterBottom>
                            S.O:{" "}
                            {votes.none + votes.absent}
                        </Typography>
                    </Stack>
            </Stack>
        </Container>
    );
}
