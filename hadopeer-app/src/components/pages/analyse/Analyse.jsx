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

const graphe = {
    data: [
        {
            hovertemplate:
                "mots=artiste<br>date=%{x}<br>occurence=%{y}<extra></extra>",
            legendgroup: "artiste",
            line: {
                color: "#636efa",
                dash: "solid",
            },
            marker: {
                symbol: "circle",
            },
            mode: "lines",
            name: "artiste",
            orientation: "v",
            showlegend: true,
            x: ["29/10/08", "02/04/09", "12/05/09", "13/05/09"],
            xaxis: "x",
            y: [0, 2, 0, 2],
            yaxis: "y",
            type: "scatter",
        },
        {
            hovertemplate:
                "mots=ministre<br>date=%{x}<br>occurence=%{y}<extra></extra>",
            legendgroup: "ministre",
            line: {
                color: "#EF553B",
                dash: "solid",
            },
            marker: {
                symbol: "circle",
            },
            mode: "lines",
            name: "ministre",
            orientation: "v",
            showlegend: true,
            x: ["29/10/08", "02/04/09", "12/05/09", "13/05/09"],
            xaxis: "x",
            y: [1, 1, 1, 1],
            yaxis: "y",
            type: "scatter",
        },
        {
            hovertemplate:
                "mots=adopter<br>date=%{x}<br>occurence=%{y}<extra></extra>",
            legendgroup: "adopter",
            line: {
                color: "#00cc96",
                dash: "solid",
            },
            marker: {
                symbol: "circle",
            },
            mode: "lines",
            name: "adopter",
            orientation: "v",
            showlegend: true,
            x: ["29/10/08", "02/04/09", "12/05/09", "13/05/09"],
            xaxis: "x",
            y: [1, 1, 1, 1],
            yaxis: "y",
            type: "scatter",
        },
    ],
    layout: {
        template: {
            data: {
                bar: [
                    {
                        error_x: {
                            color: "#2a3f5f",
                        },
                        error_y: {
                            color: "#2a3f5f",
                        },
                        marker: {
                            line: {
                                color: "#E5ECF6",
                                width: 0.5,
                            },
                            pattern: {
                                fillmode: "overlay",
                                size: 10,
                                solidity: 0.2,
                            },
                        },
                        type: "bar",
                    },
                ],
                barpolar: [
                    {
                        marker: {
                            line: {
                                color: "#E5ECF6",
                                width: 0.5,
                            },
                            pattern: {
                                fillmode: "overlay",
                                size: 10,
                                solidity: 0.2,
                            },
                        },
                        type: "barpolar",
                    },
                ],
                carpet: [
                    {
                        aaxis: {
                            endlinecolor: "#2a3f5f",
                            gridcolor: "white",
                            linecolor: "white",
                            minorgridcolor: "white",
                            startlinecolor: "#2a3f5f",
                        },
                        baxis: {
                            endlinecolor: "#2a3f5f",
                            gridcolor: "white",
                            linecolor: "white",
                            minorgridcolor: "white",
                            startlinecolor: "#2a3f5f",
                        },
                        type: "carpet",
                    },
                ],
                choropleth: [
                    {
                        colorbar: {
                            outlinewidth: 0,
                            ticks: "",
                        },
                        type: "choropleth",
                    },
                ],
                contour: [
                    {
                        colorbar: {
                            outlinewidth: 0,
                            ticks: "",
                        },
                        colorscale: [
                            [0, "#0d0887"],
                            [0.1111111111111111, "#46039f"],
                            [0.2222222222222222, "#7201a8"],
                            [0.3333333333333333, "#9c179e"],
                            [0.4444444444444444, "#bd3786"],
                            [0.5555555555555556, "#d8576b"],
                            [0.6666666666666666, "#ed7953"],
                            [0.7777777777777778, "#fb9f3a"],
                            [0.8888888888888888, "#fdca26"],
                            [1, "#f0f921"],
                        ],
                        type: "contour",
                    },
                ],
                contourcarpet: [
                    {
                        colorbar: {
                            outlinewidth: 0,
                            ticks: "",
                        },
                        type: "contourcarpet",
                    },
                ],
                heatmap: [
                    {
                        colorbar: {
                            outlinewidth: 0,
                            ticks: "",
                        },
                        colorscale: [
                            [0, "#0d0887"],
                            [0.1111111111111111, "#46039f"],
                            [0.2222222222222222, "#7201a8"],
                            [0.3333333333333333, "#9c179e"],
                            [0.4444444444444444, "#bd3786"],
                            [0.5555555555555556, "#d8576b"],
                            [0.6666666666666666, "#ed7953"],
                            [0.7777777777777778, "#fb9f3a"],
                            [0.8888888888888888, "#fdca26"],
                            [1, "#f0f921"],
                        ],
                        type: "heatmap",
                    },
                ],
                heatmapgl: [
                    {
                        colorbar: {
                            outlinewidth: 0,
                            ticks: "",
                        },
                        colorscale: [
                            [0, "#0d0887"],
                            [0.1111111111111111, "#46039f"],
                            [0.2222222222222222, "#7201a8"],
                            [0.3333333333333333, "#9c179e"],
                            [0.4444444444444444, "#bd3786"],
                            [0.5555555555555556, "#d8576b"],
                            [0.6666666666666666, "#ed7953"],
                            [0.7777777777777778, "#fb9f3a"],
                            [0.8888888888888888, "#fdca26"],
                            [1, "#f0f921"],
                        ],
                        type: "heatmapgl",
                    },
                ],
                histogram: [
                    {
                        marker: {
                            pattern: {
                                fillmode: "overlay",
                                size: 10,
                                solidity: 0.2,
                            },
                        },
                        type: "histogram",
                    },
                ],
                histogram2d: [
                    {
                        colorbar: {
                            outlinewidth: 0,
                            ticks: "",
                        },
                        colorscale: [
                            [0, "#0d0887"],
                            [0.1111111111111111, "#46039f"],
                            [0.2222222222222222, "#7201a8"],
                            [0.3333333333333333, "#9c179e"],
                            [0.4444444444444444, "#bd3786"],
                            [0.5555555555555556, "#d8576b"],
                            [0.6666666666666666, "#ed7953"],
                            [0.7777777777777778, "#fb9f3a"],
                            [0.8888888888888888, "#fdca26"],
                            [1, "#f0f921"],
                        ],
                        type: "histogram2d",
                    },
                ],
                histogram2dcontour: [
                    {
                        colorbar: {
                            outlinewidth: 0,
                            ticks: "",
                        },
                        colorscale: [
                            [0, "#0d0887"],
                            [0.1111111111111111, "#46039f"],
                            [0.2222222222222222, "#7201a8"],
                            [0.3333333333333333, "#9c179e"],
                            [0.4444444444444444, "#bd3786"],
                            [0.5555555555555556, "#d8576b"],
                            [0.6666666666666666, "#ed7953"],
                            [0.7777777777777778, "#fb9f3a"],
                            [0.8888888888888888, "#fdca26"],
                            [1, "#f0f921"],
                        ],
                        type: "histogram2dcontour",
                    },
                ],
                mesh3d: [
                    {
                        colorbar: {
                            outlinewidth: 0,
                            ticks: "",
                        },
                        type: "mesh3d",
                    },
                ],
                parcoords: [
                    {
                        line: {
                            colorbar: {
                                outlinewidth: 0,
                                ticks: "",
                            },
                        },
                        type: "parcoords",
                    },
                ],
                pie: [
                    {
                        automargin: true,
                        type: "pie",
                    },
                ],
                scatter: [
                    {
                        marker: {
                            colorbar: {
                                outlinewidth: 0,
                                ticks: "",
                            },
                        },
                        type: "scatter",
                    },
                ],
                scatter3d: [
                    {
                        line: {
                            colorbar: {
                                outlinewidth: 0,
                                ticks: "",
                            },
                        },
                        marker: {
                            colorbar: {
                                outlinewidth: 0,
                                ticks: "",
                            },
                        },
                        type: "scatter3d",
                    },
                ],
                scattercarpet: [
                    {
                        marker: {
                            colorbar: {
                                outlinewidth: 0,
                                ticks: "",
                            },
                        },
                        type: "scattercarpet",
                    },
                ],
                scattergeo: [
                    {
                        marker: {
                            colorbar: {
                                outlinewidth: 0,
                                ticks: "",
                            },
                        },
                        type: "scattergeo",
                    },
                ],
                scattergl: [
                    {
                        marker: {
                            colorbar: {
                                outlinewidth: 0,
                                ticks: "",
                            },
                        },
                        type: "scattergl",
                    },
                ],
                scattermapbox: [
                    {
                        marker: {
                            colorbar: {
                                outlinewidth: 0,
                                ticks: "",
                            },
                        },
                        type: "scattermapbox",
                    },
                ],
                scatterpolar: [
                    {
                        marker: {
                            colorbar: {
                                outlinewidth: 0,
                                ticks: "",
                            },
                        },
                        type: "scatterpolar",
                    },
                ],
                scatterpolargl: [
                    {
                        marker: {
                            colorbar: {
                                outlinewidth: 0,
                                ticks: "",
                            },
                        },
                        type: "scatterpolargl",
                    },
                ],
                scatterternary: [
                    {
                        marker: {
                            colorbar: {
                                outlinewidth: 0,
                                ticks: "",
                            },
                        },
                        type: "scatterternary",
                    },
                ],
                surface: [
                    {
                        colorbar: {
                            outlinewidth: 0,
                            ticks: "",
                        },
                        colorscale: [
                            [0, "#0d0887"],
                            [0.1111111111111111, "#46039f"],
                            [0.2222222222222222, "#7201a8"],
                            [0.3333333333333333, "#9c179e"],
                            [0.4444444444444444, "#bd3786"],
                            [0.5555555555555556, "#d8576b"],
                            [0.6666666666666666, "#ed7953"],
                            [0.7777777777777778, "#fb9f3a"],
                            [0.8888888888888888, "#fdca26"],
                            [1, "#f0f921"],
                        ],
                        type: "surface",
                    },
                ],
                table: [
                    {
                        cells: {
                            fill: {
                                color: "#EBF0F8",
                            },
                            line: {
                                color: "white",
                            },
                        },
                        header: {
                            fill: {
                                color: "#C8D4E3",
                            },
                            line: {
                                color: "white",
                            },
                        },
                        type: "table",
                    },
                ],
            },
            layout: {
                annotationdefaults: {
                    arrowcolor: "#2a3f5f",
                    arrowhead: 0,
                    arrowwidth: 1,
                },
                autotypenumbers: "strict",
                coloraxis: {
                    colorbar: {
                        outlinewidth: 0,
                        ticks: "",
                    },
                },
                colorscale: {
                    diverging: [
                        [0, "#8e0152"],
                        [0.1, "#c51b7d"],
                        [0.2, "#de77ae"],
                        [0.3, "#f1b6da"],
                        [0.4, "#fde0ef"],
                        [0.5, "#f7f7f7"],
                        [0.6, "#e6f5d0"],
                        [0.7, "#b8e186"],
                        [0.8, "#7fbc41"],
                        [0.9, "#4d9221"],
                        [1, "#276419"],
                    ],
                    sequential: [
                        [0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1, "#f0f921"],
                    ],
                    sequentialminus: [
                        [0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1, "#f0f921"],
                    ],
                },
                colorway: [
                    "#636efa",
                    "#EF553B",
                    "#00cc96",
                    "#ab63fa",
                    "#FFA15A",
                    "#19d3f3",
                    "#FF6692",
                    "#B6E880",
                    "#FF97FF",
                    "#FECB52",
                ],
                font: {
                    color: "#2a3f5f",
                },
                geo: {
                    bgcolor: "white",
                    lakecolor: "white",
                    landcolor: "#E5ECF6",
                    showlakes: true,
                    showland: true,
                    subunitcolor: "white",
                },
                hoverlabel: {
                    align: "left",
                },
                hovermode: "closest",
                mapbox: {
                    style: "light",
                },
                paper_bgcolor: "white",
                plot_bgcolor: "#E5ECF6",
                polar: {
                    angularaxis: {
                        gridcolor: "white",
                        linecolor: "white",
                        ticks: "",
                    },
                    bgcolor: "#E5ECF6",
                    radialaxis: {
                        gridcolor: "white",
                        linecolor: "white",
                        ticks: "",
                    },
                },
                scene: {
                    xaxis: {
                        backgroundcolor: "#E5ECF6",
                        gridcolor: "white",
                        gridwidth: 2,
                        linecolor: "white",
                        showbackground: true,
                        ticks: "",
                        zerolinecolor: "white",
                    },
                    yaxis: {
                        backgroundcolor: "#E5ECF6",
                        gridcolor: "white",
                        gridwidth: 2,
                        linecolor: "white",
                        showbackground: true,
                        ticks: "",
                        zerolinecolor: "white",
                    },
                    zaxis: {
                        backgroundcolor: "#E5ECF6",
                        gridcolor: "white",
                        gridwidth: 2,
                        linecolor: "white",
                        showbackground: true,
                        ticks: "",
                        zerolinecolor: "white",
                    },
                },
                shapedefaults: {
                    line: {
                        color: "#2a3f5f",
                    },
                },
                ternary: {
                    aaxis: {
                        gridcolor: "white",
                        linecolor: "white",
                        ticks: "",
                    },
                    baxis: {
                        gridcolor: "white",
                        linecolor: "white",
                        ticks: "",
                    },
                    bgcolor: "#E5ECF6",
                    caxis: {
                        gridcolor: "white",
                        linecolor: "white",
                        ticks: "",
                    },
                },
                title: {
                    x: 0.05,
                },
                xaxis: {
                    automargin: true,
                    gridcolor: "white",
                    linecolor: "white",
                    ticks: "",
                    title: {
                        standoff: 15,
                    },
                    zerolinecolor: "white",
                    zerolinewidth: 2,
                },
                yaxis: {
                    automargin: true,
                    gridcolor: "white",
                    linecolor: "white",
                    ticks: "",
                    title: {
                        standoff: 15,
                    },
                    zerolinecolor: "white",
                    zerolinewidth: 2,
                },
            },
        },
        xaxis: {
            anchor: "y",
            domain: [0, 1],
            title: {
                text: "date",
            },
        },
        yaxis: {
            anchor: "x",
            domain: [0, 1],
            title: {
                text: "occurence",
            },
        },
        legend: {
            title: {
                text: "mots",
            },
            tracegroupgap: 0,
        },
        margin: {
            t: 60,
        },
    },
    sample: "all",
    type: "frequency",
    values: [],
};

export default function Analyse() {
    const [group, setGroup] = React.useState("");
    const [graph, setGraph] = React.useState("");
    const [graphType, setGraphType] = React.useState([]);
    const [politicalGroups, setPoliticalGroups] = React.useState([]);

    const getPoliticalGroups = async () => {
        await axios
            .get(global.config.apiUrl + "/visualization/samples")
            .then((res) => {
                setPoliticalGroups(res.data);
            })
            .catch((err) => console.log(err));
    };

    const getGraphType = async () => {
        await axios
            .get(global.config.apiUrl + "/visualization/types")
            .then((res) => {
                setGraphType(res.data);
            })
            .catch((err) => console.log(err));
    };

    const handleGroupChange = (event) => {
        setGroup(event.target.value);
    };

    const handleGraphChange = (event) => {
        setGraph(event.target.value);
    };

    window.onload = function () {
        getPoliticalGroups();
        getGraphType();
    };

    return (
        <Container>
            <Box margin={10} alignItems="center" justifyContent="center">
                <Stack direction="row" spacing={5} alignItems="center" justifyContent="center">
                    <FormControl variant="standard">
                        <InputLabel id="status_dropdown_label">
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
                        <InputLabel id="status_dropdown_label">
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
                <Plot data={graphe.data} layout={graphe.layout} />
            </Box>
        </Container>
    );
}
