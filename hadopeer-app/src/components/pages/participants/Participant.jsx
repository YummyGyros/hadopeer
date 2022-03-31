import * as React from "react";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import axios from "axios";
import { useParams } from "react-router-dom";


export default function Participant() {
    const [elected_member, setElected_member] = React.useState([]);
    let { name } = useParams();

    const getElected_members = async () => {
        if (localStorage.getItem("elected_member" + name) == null)
            await axios
                .get(global.config.apiUrl + "/elected_member?name=" + name)
                .then((res) => {
                    setElected_member(res.data);
                    localStorage.setItem("elected_member" + name, JSON.stringify(res.data));
                })
                .catch((err) => console.log(err));
        else setElected_member(JSON.parse(localStorage.getItem("elected_member" + name)));
    };

    window.onclick = function () {
        getElected_members();
    };

    

    return (
        <Box margin={10} alignItems="center" justifyContent="center">
            <Stack direction="row" >
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
            <Card
                variant="elevation"
                style={{
                    backgroundColor:
                        elected_member.job === "sénateur"
                            ? "#d50000"
                            : "#0091ea",
                }}
            >
                <CardContent>
                    <Typography variant="h5" component="div" color="white">
                        {elected_member.name}
                    </Typography>
                    <Typography
                        sx={{ fontSize: 14 }}
                        color="white"
                        gutterBottom
                    >
                        {elected_member.job}
                    </Typography>
                    <Box style={{ backgroundColor: "white" }}>
                        <Typography sx={{ mb: 1.5 }}>adjective</Typography>
                        <Typography variant="body2">
                            well meaning and kindly.
                            <br />
                            {'"a benevolent smile"'}
                        </Typography>
                    </Box>
                </CardContent>
            </Card>
        </Box>
    );
}
