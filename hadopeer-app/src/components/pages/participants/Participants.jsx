import * as React from "react";
import Container from "@mui/material/Container";
import { Box } from "@mui/material";
import axios from "axios";
import { DataGrid } from "@mui/x-data-grid";
import { useNavigate } from "react-router-dom";

const columns = [
    { field: "fullName", headerName: "Full name", width: 250 },
    { field: "statut", headerName: "Statut", width: 250 },
    { field: "group", headerName: "Group Politique", width: 250 },
    { field: "departement", headerName: "Departement", width: 250 },
];

export default function Participants() {
    const [elected_members, setElected_members] = React.useState([]);
    const navigate = useNavigate();

    const getElected_members = async () => {
        if (localStorage.getItem("elected_members") == null)
            await axios
                .get(global.config.apiUrl + "/elected_members")
                .then((res) => {
                    var tmp = [];
                    for (var i in res.data) {
                        tmp[i] = {
                            id: i,
                            fullName: res.data[i][0],
                            statut: res.data[i][1],
                            group: res.data[i][2],
                            departement: res.data[i][3],
                        };
                    }
                    setElected_members(tmp);
                    localStorage.setItem("elected_members", JSON.stringify(tmp));
                })
                .catch((err) => console.log(err));
        else setElected_members(JSON.parse(localStorage.getItem("elected_members")));
    };

    window.onload = function () {
        getElected_members();
    };

    return (
        <Container>
            <Box margin={10} alignItems="center" justifyContent="center">
                <DataGrid
                    style={{ height: 650, width: 1002 }}
                    rows={elected_members}
                    columns={columns}
                    onRowClick={(newSelection) => {
                        navigate("/Participant" + newSelection.row.fullName);
                    }}
                    pageSize={10}
                    rowsPerPageOptions={[10]}
                />
            </Box>
        </Container>
    );
}
