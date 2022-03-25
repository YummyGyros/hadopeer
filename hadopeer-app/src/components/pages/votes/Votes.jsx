import * as React from "react";
import Container from "@mui/material/Container";
import { Box } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import InputLabel from "@mui/material/InputLabel";
import FormControl from "@mui/material/FormControl";
import MenuItem from "@mui/material/MenuItem";
import Stack from "@mui/material/Stack";
import Select from "@mui/material/Select";

const columns = [
    { field: "fullName", headerName: "Full name", width: 200 },
    { field: "assembly", headerName: "Assembly", width: 200 },
    { field: "group", headerName: "Group Politique", width: 200 },
    { field: "departement", headerName: "Departement", width: 200 },
];

const statut_list = [
    { statut: "sénateurs" },
    { statut: "députés" },
    { statut: "ministres" },
];

const rows = [
    {
        id: 1,
        fullName: "Arnaud Robinet",
        assembly: "député",
        group: "SOC",
        departement: "Yvelines",
    },
];

export default function Votes() {
    const [statut, setStatut] = React.useState("");
    const [departement, setDepartement] = React.useState("");
    const [group, setGroup] = React.useState("");

    const handleChange = (event) => {
        setStatut(event.target.value);
    };

    return (
        <Container>
            <Box margin={10} style={{ height: 650, width: 1100 }}>
                <Stack direction="row" spacing={10}>
                    <FormControl fullWidth variant="standard">
                        <InputLabel id="status_dropdown_label">
                            Statut
                        </InputLabel>
                        <Select
                            labelId="status_dropdown_label"
                            id="status_dropdown_select"
                            value={statut}
                            label="Statut"
                            onChange={handleChange}
                        >
                            {statut_list.map((statut_list) => (
                                <MenuItem value={statut_list.statut}>
                                    {statut_list.statut}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <FormControl fullWidth variant="standard">
                        <InputLabel id="status_dropdown_label">
                            Statut
                        </InputLabel>
                        <Select
                            labelId="status_dropdown_label"
                            id="status_dropdown_select"
                            value={statut}
                            label="Statut"
                            onChange={handleChange}
                        >
                            {statut_list.map((statut_list) => (
                                <MenuItem value={statut_list.statut}>
                                    {statut_list.statut}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <FormControl fullWidth variant="standard">
                        <InputLabel id="group_dropdown_label">
                            Group Politique
                        </InputLabel>
                        <Select
                            labelId="group_dropdown_label"
                            id="group_dropdown_select"
                            value={group}
                            label="Group Politique"
                            onChange={handleChange}
                        >
                            {statut_list.map((statut_list) => (
                                <MenuItem value={statut_list.statut}>
                                    {statut_list.statut}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </Stack>
                <DataGrid
                    rows={rows}
                    columns={columns}
                    pageSize={10}
                    rowsPerPageOptions={[10]}
                />
            </Box>
        </Container>
    );
}
