import React from "react";
import "./home.css";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import IconeButton from '@mui/material/IconButton';
import GitHubIcon from '@mui/icons-material/GitHub';
import { Box } from "@mui/material";

export default function Home() {
    return (
        <Container maxWidth="xl" className="home">
            <div className="homeTitle">HadoPeer</div>
            <Divider variant="inset" />
            <Box marginTop={9}>
                <Typography variant="h4" align="left">
                    Introduction
                </Typography>
                <Typography variant="h6" align="left">
                    Texte de présentation du projet avec une chronologie rapide
                    de la loi et de ses développements (texte rédigé par Marie
                    Puren). 
                </Typography>
                <Typography marginTop={5} variant="h4" align="left">
                    Données
                </Typography>
                <Typography marginTop={2} variant="h6" align="left">
                    Résumé Adoption Loi:
                    <br/>
                    <IconeButton href="http://www.senat.fr/dossier-legislatif/pjl07-405.html">
                        Sénat
                    </IconeButton>
                    <br/>
                    <IconeButton href="https://www.assemblee-nationale.fr/13/dossiers/internet.asp">
                        Assemblée Nationale
                    </IconeButton>
                </Typography>
                <Typography marginTop={5} variant="h4" align="left">
                    Equipe
                </Typography>
                <Typography marginTop={2} variant="h6" align="left">
                    Organisatrice: Marie Puren, historienne du LabResearch d’Epitech Paris
                    <br/>
                    Développeurs Epitech Paris promo 2024:
                    <br/>
                    <IconeButton href="https://github.com/jack-a-dit">
                    Adrien Mallet
                    </IconeButton>
                    <br/>
                    <IconeButton href="https://github.com/MTheboul">
                    Matteo Theboul
                    </IconeButton>
                    <br/>
                    <IconeButton href="https://github.com/YummyGyros">
                    Robin Levavasseur
                    </IconeButton>
                </Typography>
                <Typography marginTop={5} variant="h4" align="left">
                    Liens 
                </Typography>
                <Typography marginTop={2} variant="h6" align="left">
                <IconeButton href='https://github.com/YummyGyros/hadopeer-scrapped-data'>
                     Données scrapping pour NLP
                </IconeButton>
                    <br/>
                    <IconeButton href='https://github.com/YummyGyros/hadopeer'>GitHub<GitHubIcon/></IconeButton>
                </Typography>
            </Box>
        </Container>
    );
}
