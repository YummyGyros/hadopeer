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
        console.log(elected_member)
    };

    

    return (
        <Box margin={10} alignItems="center"  marginBottom={30}>
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
            <Stack alignItems={"center"} marginTop={15}>
            <Card
                variant="elevation"
                style={{
                    width: '60vw',
                    backgroundColor:
                        elected_member.job === "sénateur"
                            ? "#d50000"
                            : "#0091ea",
                }}
            >
                <CardContent alignItems="left">
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
                    <Box style={{ backgroundColor: "white" }} margin={2}>
                        <Typography sx={{ mb: 1.5 } }
                        >Département: {elected_member.department}
                        <br />
                        Groupe: {elected_member.group}
                        <br />
                        Mandat: {elected_member.mandate}
                        </Typography>
                        
                        <Typography variant="body2">
                            1er vote: {elected_member.vote_1}
                            <br />
                            {elected_member.vote_2 ?
                            "2ème vote: " + elected_member.vote_2
                            : null}
                        </Typography>
                    </Box>
                </CardContent>
            </Card>
            </Stack>
        </Box>
    );
}
