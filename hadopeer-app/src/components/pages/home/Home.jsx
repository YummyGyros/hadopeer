import React from "react";
import "./home.css";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import { Box } from "@mui/material";

export default function Home() {
    return (
        <Container maxWidth="xl" className="home">
            <div className="homeTitle">HadoPeer</div>
            <div className="homeSubTitle">Welcome to our HadoPeer project</div>
            <Divider variant="inset" />
            <Box margin={9}>
                <Typography variant="h4" align="left">
                    Introduction
                </Typography>
                <Typography variant="h6" align="left">
                    Texte de présentation du projet avec une chronologie rapide
                    de la loi et de ses développements (texte rédigé par Marie
                    Puren). Texte de présentation du projetavec une chronologie
                    rapide de la loi et de ses développements (texte rédigé par
                    Marie Puren).
                </Typography>
                <Typography variant="h4" align="left">
                    Données
                </Typography>
                <Typography variant="h6" align="left">
                    Résumé Adoption Loi:
                </Typography>
                <Typography variant="h6" align="left">
                    - Sénat
                </Typography>
                <Typography variant="h6" align="left">
                    - Assemblée Nationale
                </Typography>
                <Typography variant="h6" align="left">
                    Comptes-Rendus des débats:
                </Typography>
                <Typography variant="h6" align="left">
                    - Sénat
                </Typography>
                <Typography variant="h6" align="left">
                    - Assemblée Nationale
                </Typography>
            </Box>
        </Container>
    );
}
