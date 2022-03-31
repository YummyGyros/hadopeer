import * as React from "react";
import Container from "@mui/material/Container";
import { Box } from "@mui/material";
import InputLabel from "@mui/material/InputLabel";
import FormControl from "@mui/material/FormControl";
import MenuItem from "@mui/material/MenuItem";
import axios from "axios";
import Stack from "@mui/material/Stack";
import Select from "@mui/material/Select";
import Plot from "react-plotly.js";

export default function Analyse() {
    const [group, setGroup] = React.useState("");
    const [graph, setGraph] = React.useState("");
    const [graphType, setGraphType] = React.useState([]);
    const [politicalGroups, setPoliticalGroups] = React.useState([]);
    const [visualization, setVisualization] = React.useState([]);

    const getPoliticalGroups = async () => {
        await axios
            .get(global.config.apiUrl + "/visualization/samples")
            .then((res) => {
                setPoliticalGroups(res.data);
                setGroup(res.data[0]);
            })
            .catch((err) => console.log(err));
    };

    const getGraphType = async () => {
        await axios
            .get(global.config.apiUrl + "/visualization/types")
            .then((res) => {
                setGraphType(res.data);
                setGraph(res.data[0])
            })
            .catch((err) => console.log(err));
    };


    const getVisualization = async (gra = graph, gro = group) => {
        if (localStorage.getItem("visualization" + gra + gro) == null) {
            await axios
                .get(
                    global.config.apiUrl +
                        "/visualization?type=" +
                        gra +
                        "&sample=" +
                        gro
                )
                .then((res) => {
                    setVisualization(res.data);
                    localStorage.setItem(
                        "visualization" + gra + gro,
                        JSON.stringify(res.data)
                    );
                })
                .catch((err) => console.log(err));
        } else
            setVisualization(
                JSON.parse(
                    localStorage.getItem("visualization" + gra + gro)
                )
            );
    };

    
    const handleGroupChange = (event) => {
        setGroup(event.target.value);
        getVisualization(graph, event.target.value);
    };

    const handleGraphChange = (event) => {
        setGraph(event.target.value);
        getVisualization(event.target.value);
    };

    window.onload = function () {
        getPoliticalGroups();
        getGraphType();
    };

    return (
        <Container>
            <Box margin={10} alignItems="center" justifyContent="center">
                <Stack
                    direction="row"
                    spacing={5}
                    alignItems="center"
                    justifyContent="center"
                >
                    <FormControl variant="standard">
                        <InputLabel id="graph_dropdown_label">
                            Graph Type
                        </InputLabel>
                        <Select
                            sx={{
                                width: 150,
                            }}
                            labelId="graph_dropdown_label"
                            id="graph_dropdown_select"
                            defaultValue={graphType[0]}
                            value={graph}
                            label="Graph Type"
                            onChange={handleGraphChange}
                        >
                            {graphType.map((graphType) => (
                                <MenuItem key={graphType} value={graphType}>
                                    {graphType}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <FormControl variant="standard">
                        <InputLabel id="Group_dropdown_label">
                            Sample
                        </InputLabel>
                        <Select
                            sx={{
                                width: 150,
                            }}
                            labelId="Group_dropdown_label"
                            id="Group_dropdown_select"
                            defaultValue={politicalGroups[0]}
                            value={group}
                            label="Group"
                            onChange={handleGroupChange}
                        >
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
                    data={visualization.graph ? visualization.graph.data : []}
                    layout={
                        visualization.graph ? visualization.graph.layout : {}
                    }
                />
            </Box>
        </Container>
    );
}
