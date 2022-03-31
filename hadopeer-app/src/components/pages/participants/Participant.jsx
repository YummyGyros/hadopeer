import * as React from "react";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import axios from "axios";
import { useParams } from "react-router-dom";

function sentenceCase(str) {
    if (str === null || str === "") return false;
    else str = String(str);

    return str.replace(/\w\S*/g, function (txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

export default function Participant() {
    const [elected_member, setElected_member] = React.useState([]);
    let { name } = useParams();

    const getElected_members = async () => {
        if (localStorage.getItem("elected_member" + name) == null)
            await axios
                .get(global.config.apiUrl + "/elected_member?name=" + name)
                .then((res) => {
                    setElected_member(res.data);
                    localStorage.setItem(
                        "elected_member" + name,
                        JSON.stringify(res.data)
                    );
                })
                .catch((err) => console.log(err));
        else
            setElected_member(
                JSON.parse(localStorage.getItem("elected_member" + name))
            );
    };

    window.onclick = function () {
        getElected_members();
    };

    return (
        <Box margin={10} marginBottom={43}>
            <Stack direction="row">
                <Button
                    key="Participants"
                    href={"/Participants"}
                    variant={"contained"}
                    sx={{
                        my: 2,
                        color: "white",
                    }}
                >
                    Retour
                </Button>
            </Stack>
            <Stack alignItems={"center"} marginTop={15}>
                <Card
                    variant="elevation"
                    style={{
                        width: "60vw",
                        backgroundColor:
                            elected_member.job === "sénateur"
                                ? "#FF6666"
                                : "#0091ea",
                    }}
                >
                    <CardContent>
                        <Typography variant="h3" component="div" color="white">
                            {elected_member.name}
                        </Typography>
                        <Typography color="white" variant="h4" gutterBottom>
                            {sentenceCase(elected_member.job)}
                        </Typography>
                        <Stack marginTop={10}>
                            <Typography
                                color="white"
                                variant="h4"
                                marginTop={0}
                                sx={{ mb: 1.5 }}
                            >
                                Département: {elected_member.department}
                                <br />
                                Groupe: {elected_member.group}
                                <br />
                                Mandat: {elected_member.mandate}
                                <br />
                                1er vote: {elected_member.vote_1}
                                <br />
                                {elected_member.vote_2
                                    ? "2ème vote: " + elected_member.vote_2
                                    : null}
                            </Typography>
                        </Stack>
                    </CardContent>
                </Card>
            </Stack>
        </Box>
    );
}
